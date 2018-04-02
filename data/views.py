from django.shortcuts import render, get_object_or_404
from .models import Category, WorkFlow
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .forms import WorkFlowForm
import json, sys

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
           'found': found,
           'error': error
             }
    if jsonFlag:
        return HttpResponse(json.dumps(_dict),
                            content_type="application/json")
    else:
        return render(request,
               'data/workflow/list.html', _dict)

def workflow_detail(request, id, slug, jsonFlag=False):
    print("workflow_detail.........................")
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
             'found': found,
             'error': error,
            }
    if jsonFlag:
        return HttpResponse(json.dumps(_dict),
                            content_type="application/json")
    else:
        return render(request,
               'data/workflow/detail.html', _dict)

def workflow_search(request, jsonFlag=False):
    if 'byName' in request.POST:
        slug = request.POST.get('key', '')
        try:
            workflow = WorkFlow.objects.get(slug=slug)
            found = True
            error = "No error"
        except ObjectDoesNotExist:
            workflow = None
            found = False
            error = "There is no workflow with name %s" % (slug)

        _dict = {'workflow': workflow,
                 'found': found,
                 'error': error,
                }
        if jsonFlag:
            return HttpResponse(json.dumps(_dict),
                                content_type="application/json")
        else:
            return render(request,
                   'data/workflow/detail.html', _dict)

    elif 'byKeyWord' in request.POST:
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
                   'found': found,
                   'error': error}
        if jsonFlag:
            return HttpResponse(json.dumps(_dict), content_type="application/json")
        else:
            return render(request,
                   'data/workflow/list.html', _dict)


def workflow_download(request, id, slug):
    try:
        workflow = WorkFlow.objects.get(id=id, slug=slug)
        workflow.downloads += 1
        workflow.save()
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps("Error: Workflow %s not found" % slug))

    return HttpResponse(workflow.json, content_type="application/json")

def workflow_add(request, workFlowJson=None):
    print("workflow_add.................................................")
    # A HTTP POST?
    if request.method == 'POST':
        print("workflow_add........POST")
        print(request.FILES)
        form = WorkFlowForm(request.POST, request.FILES)

        # Have we been provided with a valid form?
        if form.is_valid():
            #TODO: check json is correct and have maximum_length
            #do it in models
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return workflow_list(request) ### confirmation page
        else:
            # The supplied form contained errors - just print them to the terminal.
            print (form.errors)
    else:
        print("workflow_add........NO POST")
        # If the request was not a POST, display the form to enter details.
        form = WorkFlowForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    print("workflow_add........return")
    return render(request, 'data/workflow/workflow_add.html', {'form': form})