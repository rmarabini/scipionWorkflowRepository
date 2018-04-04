from django.shortcuts import render
from django.http import HttpResponse
from .forms import WorkFlowForm, WorkFlowFileForm, WorkFlowFileModelForm
import json
import uuid
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

#Function that checks json
# workflowFile is a  FileField
def check_json(workflowFile, form=None):

    if not workflowFile.name.endswith('.json'):
        form.add_error('jsonFileName', 'File is not JSON type')
        return True

    # chunk default size is 64KB
    if workflowFile.multiple_chunks():
        form.add_error('jsonFileName', 'Uploaded file is too big (%.2f KB).' % (workflowFile.size / (1024)))
        return True

    return False

def workflowModel_add(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = WorkFlowForm(request.POST)
        if form.is_valid():
            pass
            # get jsonfilename
            # read file
            # assign json to workflow model
            form.instance.json = file_data
            #save it.
            workflow = form.save(commit=True)
            # Acknowledge user upload.
            _dict = {'workflow': workflow,
                     'result': True,
                     'error': "",
                     }
            return render(request,
                          'upload/success.html', _dict)
    elif request.method == 'GET':
        if 'jsonFileName' in request.GET:
            jsonFileName = request.GET['jsonFileName']
            form = WorkFlowFileModelForm(initial={'jsonFileName':jsonFileName})
            return render(request, 'upload/workflow_add.html', {'form': form})

    return HttpResponse("""Cannot render workflow upload form from SCipion.
    You may connect to URL %s and upload the workflow manually"""%reverse(
            'upload:workflow_add'))

def workflow_add(request):
    # A HTTP POST?
    if request.method == 'POST':# and request.FILES['workflowFile']:
        form = WorkFlowForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():

            workflowFile = form.cleaned_data["json"]
            if not check_json(workflowFile, form):
                file_data = workflowFile.read().decode("utf-8")
                # modify object json value
                form.instance.json = file_data
                # Save the new workflow to the database.
                workflow = form.save(commit=True)
                # Acknowledge user upload.
                _dict = {'workflow': workflow,
                         'result': True,
                         'error': "",
                         }
                return render(request,
                              'upload/success.html', _dict)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print ("Invalid Form:", form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = WorkFlowForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'upload/workflow_add.html', {'form': form})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def workflowFile_add(request):
    # A HTTP POST?
    if request.method == 'POST':# and request.FILES['workflowFile']:
        form = WorkFlowFileForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():
            workflowFile = form.cleaned_data["json"]
            jsonFileName = str(uuid.uuid4()) + ".json"
            if not check_json(workflowFile, form):
                #file_data = workflowFile.read().decode("utf-8")
                fs = FileSystemStorage()
                #file saved in media
                filename = fs.save(jsonFileName, workflowFile)
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
        form = WorkFlowFileForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'upload/workflowFile_add.html', {'form': form})