from django.shortcuts import render
from django.http import HttpResponse
from .forms import WorkFlowManualForm, WorkFlowProgStep1Form, WorkFlowProgStep2Form
import json, urllib
import uuid, os
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.conf import settings

def check_json(workflowFile, form=None):
    # Function that checks json, limits size to 64K
    # input param workflowFile is a  FileField

    if not workflowFile.name.endswith('.json'):
        form.add_error('jsonFileName', 'File is not JSON type')
        return True

    # chunk default size is 64KB
    if workflowFile.multiple_chunks():
        form.add_error('jsonFileName', 'Uploaded file is too big (%.2f KB).'
                       % (workflowFile.size / (1024)))
        return True

    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def workflow_add_manually(request):
    # form with all the fields including file upload. For non programatic use
    if request.method == 'POST':# and request.FILES['workflowFile']:
        form = WorkFlowManualForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():

            workflowFile = form.cleaned_data["json"]
            if not check_json(workflowFile, form):

                ''' Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                ''' End reCAPTCHA validation '''

                if result['success']:
                    file_data = workflowFile.read().decode("utf-8")
                    # modify object json value
                    form.instance.json = file_data
                    # set delete hash
                    # save it also as session variable
                    jsonFileName = str(uuid.uuid4()) + ".json"
                    form.instance.hash = jsonFileName
                    request.session[jsonFileName] = jsonFileName
                    # get client ip
                    form.instance.client_ip = get_client_ip(request)
                    # Save the new workflow to the database.
                    workflow = form.save(commit=True)

                    # Acknowledge user upload.
                    _dict = {'workflow': workflow,
                             'result': True,
                             'error': "",
                             'deleteOn': True,
                             }
                    return render(request,
                                  'upload/success.html', _dict)
                else:
                    form.add_error('json', 'Please check captcha')
                    print("HORROR")
        else:
            # The supplied form contained errors - just print them to the terminal.
            print ("Invalid Form:", form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = WorkFlowManualForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'upload/workflow_add_manually.html', {'form': form,
                                                        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
                                                        'workflowAction': 'upload:workflow_add_manually'})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt # disable csrf check
def workflowProgStep1_add(request):
    # upload programatically a file and a version string
    # called usually by scipion. Save uploaded file name in server side
    # return json used y scipion to call workflowModel_add
    if request.method == 'POST':
        form = WorkFlowProgStep1Form(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():
            workflowFile = form.cleaned_data["json"]
            jsonFileName = str(uuid.uuid4()) + ".json"
            if not check_json(workflowFile, form):
                fs = FileSystemStorage()
                fs.save(jsonFileName, workflowFile, max_length=64 * 1024)
                # Acknowledge user upload.
                _dict = {'result': True,
                         'error': "",
                         'jsonFileName':jsonFileName
                         }
                return HttpResponse(json.dumps(_dict),
                                    content_type="application/json")
        else:
            _dict = {'result': False,
                     'error': "Invalid Form:" +  str(form.errors)}
            print ("Invalid Form:", form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        # this is usefull for testing but scipion calls should never end here
        form = WorkFlowProgStep1Form()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    #return render(request, 'upload/workflow_add_manually.html', {'form': form,
    #                       'workflowAction': 'upload:workflowFile_add'})

def workflowProgStep2_add(request):
    # GET: conection from scipion client, upload workflow file and version
    # in most cases scipion first calls workflowFile_add, upload the file
    # and then make a get call to this funcion passing the file name.
    # this get call returns a post call that open the upload form
    #
    # POST: assume the file is already uploaded and the serverside name of the file
    # is in jsonFileName
    if request.method == 'POST': #conection from browser
        form = WorkFlowProgStep2Form(request.POST)
        if form.is_valid():
            # get jsonfilename uploaded by scipion client
            jsonFileName = request.session['jsonFileName']
            fs = FileSystemStorage()
            file_data = fs.open(jsonFileName).read().decode("utf-8")
            # assign json to workflow model
            form.instance.json = file_data
            # set delete hash
            # save it also as session variable
            form.instance.hash = jsonFileName
            request.session[jsonFileName] = jsonFileName
            form.instance.client_ip = get_client_ip(request)
            #save it.
            workflow = form.save(commit=True)
            #delete temporary file
            fs.delete(jsonFileName)
            # Acknowledge user upload.
            _dict = {'workflow': workflow,
                     'result': True,
                     'error': "",
                     'deleteOn': True,
                     }
            return render(request,
                          'upload/success.html', _dict)

    elif request.method == 'GET': # conection from scipion client
                                  # using no form
        if 'jsonFileName' in request.GET:
            jsonFileName = request.GET['jsonFileName']
            versionInit = request.GET['versionInit']
            # store server side name of the json file
            request.session['jsonFileName'] = jsonFileName
            # pass version through form, in this way users may change it
            # is this good? It should not but scipion is quite unreliable
            # about version mantenance. For exable the devel version is always called devel
            # regardeless of the last released version :-(
            form = WorkFlowProgStep2Form(initial={'versionInit':versionInit})
            # read json workflow file
            fs = FileSystemStorage()
            file_data = fs.open(jsonFileName).read().decode("utf-8")

            return render(request, 'upload/workflow_add_manually.html',
                          {'form': form,
                           'workflowAction': 'upload:workflowProgStep2_add',
                           'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
                           'json_workflow': file_data})

    return HttpResponse("""Cannot render workflow upload form from Scipion.
    You may connect to URL <a href='%s'> here </a> and upload the workflow manually"""%reverse(
            'upload:workflow_add_manually'))
