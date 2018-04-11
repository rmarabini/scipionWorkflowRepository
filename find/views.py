from django.shortcuts import render
from data.models import Category, WorkFlow
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import json
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib, sys
from django.conf import settings

# return list of categories and corresponding workflows
def workflow_list(request, category_slug=False, jsonFlag=False):
    category = None
    found = True
    error = "No error"

    categories = Category.objects.all().order_by('name') # show always by the same order
    workflows_list = WorkFlow.objects.all().order_by('-downloads',"-views", "name") # short by download
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            workflows_list = workflows_list.filter(category=category)
        except ObjectDoesNotExist:
            workflows_list = None
            found = False
            error = "category=%s" % (category_slug)

    page = request.GET.get('page', 1)

    #https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
    paginator = Paginator(workflows_list, 10)
    try:
        workflows = paginator.page(page)
    except PageNotAnInteger:
        workflows = paginator.page(1)
    except EmptyPage:
        workflows = paginator.page(paginator.num_pages)


    _dict = {'category': category,
           'categories': categories,
           'workflows': workflows,
           'result': found,
           'error': error
             }
    if jsonFlag:
        return HttpResponse(json.dumps(_dict),
                            content_type="application/json")
    else:
        return render(request,
               'find/list.html', _dict)

def workflow_detail(request, id, slug, jsonFlag=False):
    _dict = {}
    try:
        workflow = WorkFlow.objects.get(id=id, slug=slug)
        _dict['result'] = True
        _dict['workflow'] = workflow
        _dict['error'] = "No error"
        _dict['RECAPTCHA_PUBLIC_KEY'] = settings.RECAPTCHA_PUBLIC_KEY
        workflow.views += 1
        workflow.save()
        if workflow.hash in request.session:
            _dict['deleteOn'] = True
    except ObjectDoesNotExist:
        _dict['workflow'] = None
        _dict['result'] = False
        _dict['error'] = "Workflow with 'slug=%s' and 'id=%s'Not found"%(slug, id)

    if jsonFlag:
        return HttpResponse(json.dumps(_dict),
                            content_type="application/json")
    else:
        return render(request,
               'find/detail.html', _dict)

def workflow_search(request, jsonFlag=False):
    print("workflow_search")
    if 'byName' in request.POST:
        print("byName")
        slug = slugify(request.POST.get('key', ''))
        try:
            workflow = WorkFlow.objects.get(slug=slug)
            found = True
            error = "No error"
        except ObjectDoesNotExist:
            workflow = None
            found = False
            error = "There is no workflow with name %s" % (slug)

        _dict = {'workflow': workflow,
                 'result': found,
                 'error': error,
                }
        if jsonFlag:
            return HttpResponse(json.dumps(_dict),
                                content_type="application/json")
        else:
            return render(request,
                   'find/detail.html', _dict)

    elif 'byKeyWord' in request.POST:
        print("byKeyWord")
        key = request.POST.get('key', '')
        query = Q(keywords__icontains=key)
        query.add(Q(description__icontains=key), Q.OR)
        categories = Category.objects.all()
        workflows = WorkFlow.objects.filter(query).order_by('-downloads',"-views", "name")
        if workflows.exists():
            found = True
            error = "No error"
        else:
            workflows = None
            found = False
            error = "%s in keywords OR in description" % key

        _dict = {'category': None,
                   'categories': categories,
                   'workflows': workflows,
                   'result': found,
                   'error': error}
        if jsonFlag:
            return HttpResponse(json.dumps(_dict), content_type="application/json")
        else:
            return render(request,
                   'find/list.html', _dict)
    else:
        print("Horro no POST request")

# get workflow and incement counter
def workflow_download(request, id, slug):
    return _workflow_download(request, id, slug, True)

# get workflow and do NOT incement counter
def workflow_download_no_count(request, id, slug):
    return _workflow_download(request, id, slug, False)

# get workflow either by name or by keyword
def _workflow_download(request, id, slug, count=False):
    try:
        workflow = WorkFlow.objects.get(id=id, slug=slug)
        if count:
            workflow.downloads += 1
            workflow.save()
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps("Error: Workflow %s not found" % slug))

    ''' Begin reCAPTCHA validation '''
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.RECAPTCHA_PRIVATE_KEY,
        'response': recaptcha_response
    }
    if sys.version_info >= (3, 0):
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
    elif sys.version_info < (3, 0) and sys.version_info >= (2, 5):
        import urllib2
        data = urllib.urlencode(values).encode()
        req = urllib2.Request(url, data=data)
        response = urllib2.urlopen(req)

    result = json.loads(response.read().decode())
    ''' End reCAPTCHA validation '''

    if result['success'] or count==False:
        response = HttpResponse(workflow.json, content_type="application/octet-stream")
        if workflow.name.endswith('.json'):
            fileName = workflow.name
        else:
            fileName = "%s.json" % workflow.name

        response['Content-Disposition'] = 'inline; filename=%s' % fileName
        return response
    else:
        _dict = {}
        _dict['workflow'] = None
        _dict['result'] = False
        _dict['error'] = "Please, check the captcha"
        _dict['link'] = "/workflow_detail/{}/{}/".format(id, slug)
        return render(request,
               'find/detail.html', _dict)

def workflow_delete(request, id, slug):
    workflow = WorkFlow.objects.get(id=id, slug=slug)
    if workflow.hash in request.session:
        workflow.delete()
        _dict = {'workflow': workflow,
                 'result': True,
                 'error': None,
                 'action': 'deleted'
                 }
        return render(request,
                      'find/success.html', _dict)
    else:
        _dict = {'workflow': workflow,
                 'result': False,
                 'error': "You have not created this workflow from this "
                          "browser. Therefore you cannot delete it",
                 'action': 'deleted'
                 }
        return render(request,
                      'find/success.html', _dict)
