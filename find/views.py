from django.shortcuts import render
from data.models import Category, WorkFlow
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import json
from django.template.defaultfilters import slugify

# return list of categories and corresponding workflows
def workflow_list(request, category_slug=False, jsonFlag=False):
    category = None
    categories = Category.objects.all().order_by('name') # show always by the same order
    workflows = WorkFlow.objects.all().order_by('-downloads',"-views", "name") # short by download
    found = True
    error = "No error"
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            workflows = workflows.filter(category=category)
        except ObjectDoesNotExist:
            workflow = None
            found = False
            error = "category=%s" % (category_slug)

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
    try:
        workflow = WorkFlow.objects.get(id=id, slug=slug)
        found = True
        error = "No error"
        workflow.views += 1
        workflow.save()
    except ObjectDoesNotExist:
        workflow = None
        found = False
        error = "slug=%s and id=%s"%(slug, id)

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

#    return HttpResponse(workflow.json, content_type="application/json")
    response = HttpResponse(workflow.json, content_type="application/octet-stream")
    if workflow.name.endswith('.json'):
        fileName = workflow.name
    else:
        fileName = "%s.json" % workflow.name

    response['Content-Disposition'] = 'inline; filename=%s' % fileName
    return response

