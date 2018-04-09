
from unittest import TestCase
from django.test import Client
from data.models import Category, WorkFlow, User
from data.management.commands.populate import Command, CATEGORY, USER, WORKFLOW
from django.urls import reverse
from django.db.models import Q

#execute: python manage.py test find.tests.FindTests.testNAME

#very basis model testing, we just check the objects exists
# returns all  workflows
WORKFLOW_LIST = 'find:workflow_list'
# list of workflows related to a given category
WORKFLOW_LIST_BY_CARTEGORY = 'find:workflow_list_by_category'
# full information related with a workflow
WORKFLOW_DETAIL = 'find:workflow_detail'
# Dowload json with workflow
WORKFLOW_DOWNLOAD = 'find:workflow_download'
# get workflow but do not
# increment download counter (it is used by workflow viewer -web component)
WORKFLOW_DOWNLOAD_NO_COUNT = 'find:workflow_download_no_count'
# search for workflows vy name or keyword
WORKFLOW_SEARCH = 'find:workflow_search'

#DO NOT MODIFIED ANYTHING BELLOW THIS POINT
class FindTests(TestCase):
    def setUp(self):
        # The test client is a Python class that acts as a dummy Web browser
        self._client   = Client()

        # populate database
        self.populate = Command()
        self.populate.handle()

        #data is a pointer to workflow, users and categories names
        self.data = self.populate.getData()

    def test_0_workflow_list(self):
        #firts check all workflows
        print ("test_workflow_list:")
        # WORKFLOW_LIST returns all  workflows
        # If you set follow = True the client will follow any redirects
        response = self._client.get(reverse(WORKFLOW_LIST), follow=True)

        # Check that all categories and workflow are in the returned page
        baseName = CATEGORY
        for itemName in self.data[baseName]:
            self.assertIn(itemName, str(response.content))
            print ("    assert: %s"%itemName)
        baseName = WORKFLOW
        for itemName in self.data[baseName]:
            self.assertIn(itemName, str(response.content))
            print ("    assert: %s"%itemName)

    def test_1_workflow_category(self):
        # firts check all workflows related with a category
        print ("test_workflow_category")
        baseName = CATEGORY
        category = Category.objects.get(name = self.data[baseName][0])
        response = self._client.get(reverse(WORKFLOW_LIST_BY_CARTEGORY,
                                            kwargs={'category_slug':category.slug}))

        workflows = WorkFlow.objects.filter(category=category)
        for itemName in workflows:
            self.assertIn("%s</a>"%itemName.name,str(response.content))
            print("    assert: %s in %s" % (itemName.name, category.name))

        # django Q objects have being designed to make complex queries
        # in this case search for objects NOT equal to a given category
        workflows = WorkFlow.objects.filter(~Q(category=category))
        for itemName in workflows:
            self.assertNotIn("%s</a>"%itemName.name,str(response.content))
            print("    assert: %s NOT in %s" % (itemName.name, category.name))

    def test_2_workflow_detail(self):
        print ("test_workflow_detail.")
        # getworkflow detail
        baseName = WORKFLOW
        workflow = WorkFlow.objects.get(name = self.data[baseName][0])
        print ("    workflow %s has been seem %d times" % (workflow.name, workflow.views) )
        response = self._client.get(reverse(WORKFLOW_DETAIL,
                                            kwargs={'id':workflow.id,
                                                    'slug':workflow.slug}))
        self.assertIn(workflow.name,str(response.content))
        self.assertIn(workflow.description, response.content.decode("utf-8"))
        # get workflow detail again, viewsshould be 1
        workflow = WorkFlow.objects.get(name = self.data[baseName][0])
        self.assertEqual(workflow.views, 1)
        print ("    workflow %s has been seem %d times" % (workflow.name, workflow.views) )
        response = self._client.get(reverse(WORKFLOW_DETAIL,
                                            kwargs={'id':workflow.id,
                                                    'slug':workflow.slug}))
        workflow = WorkFlow.objects.get(name = self.data[baseName][0])
        # get workflow detail again, views should be 2
        self.assertEqual(workflow.views, 2)
        print ("    workflow %s has been seem %d times" % (workflow.name, workflow.views) )

    def test_3_workflow_download(self):
        print("test_3_workflow_download.")
        baseName = WORKFLOW
        workflow = WorkFlow.objects.get(name = self.data[baseName][0])

        # download workflow & get workflow again
        # downloads should be 1 after download
        print ("    workflow %s has been seem %d times" % (workflow.name, workflow.downloads) )
        self.assertEqual(workflow.downloads, 0)
        response = self._client.get(reverse(WORKFLOW_DOWNLOAD,
                                            kwargs={'id' : workflow.id,
                                                    'slug' : workflow.slug}))
        # reload workflow
        workflow = WorkFlow.objects.get(name = self.data[baseName][0])
        print ("    workflow %s has been seem %d times" % (workflow.name, workflow.downloads) )
        self.assertEqual(workflow.downloads, 1)
        self.assertIn(self.populate.getJson(), response.content.decode("utf-8"))

        # try the non-count version of download
        # download should not be incremented
        response = self._client.get(reverse(WORKFLOW_DOWNLOAD_NO_COUNT,
                                            kwargs={'id' : workflow.id,
                                                    'slug' : workflow.slug}))
        # reload workflow
        workflow = WorkFlow.objects.get(name = self.data[baseName][0])
        print ("    workflow %s has been seem %d times (No count)" % (workflow.name, workflow.downloads) )
        self.assertEqual(workflow.downloads, 1)
        self.assertIn(self.populate.getJson(), response.content.decode("utf-8"))

    def test_4_workflow_search(self):
        #search for a workflow workflow_search/
        print ("test_4_workflow_search.")
        baseName = WORKFLOW
        workflow = WorkFlow.objects.get(name=self.data[baseName][0])
        response = self._client.post(reverse(WORKFLOW_SEARCH),
                                            {'byName': 'byName',
                                             'key': workflow.slug})
        print ("   ByName search for workflow %s" % workflow.slug)
        self.assertIn(workflow.name,str(response.content))
        self.assertIn(workflow.description, response.content.decode("utf-8"))

        valueToSearch = workflow.keywords[:5]
        response = self._client.post(reverse(WORKFLOW_SEARCH),
                                            {'byKeyWord': 'byKeyWord',
                                             'key': workflow.slug})
        print ("   ByKeyWord search for %s" % valueToSearch)
        self.assertIn(workflow.name,str(response.content))
