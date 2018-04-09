from unittest import TestCase
from django.test import Client
from data.models import Category, WorkFlow, User
from data.management.commands.populate import Command, CATEGORY, USER, WORKFLOW
from django.urls import reverse
from django.db.models import Q
from .forms import WorkFlowManualForm, WorkFlowProgStep1Form, WorkFlowProgStep2Form
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.core.exceptions import ObjectDoesNotExist

# execute: python manage.py test find.tests.UploadTests.testNAME

WORKFLOW_ADD_MANUALLY = 'upload:workflow_add_manually'
WORKFLOW_PROG_STEP1 = 'upload:workflowProgStep1_add'
WORKFLOW_PROG_STEP2 = 'upload:workflowProgStep2_add'

NAME_CATEGORY = "category"
NAME_DESCRIPTION = "description"
NAME_KEYWORDS = "keywords"
NAME_NAME = "name"
NAME_VERSION = "versionInit"
NAME_JSON = 'json'
NAME_JSONFILENAME = 'jsonFileName'

ID_CATEGORY = "id_category"
ID_DESCRIPTION = "id_description"
ID_KEYWORDS = "id_keywords"
ID_NAME = "id_name"
ID_VERSION = "id_versionInit"
ID_JSON = 'id_json'


# DO NOT MODIFIED ANYTHING BELLOW THIS POINT

# Create your tests here.
# get keys, if not google efuse
# field form adn send
# ask for workflow

# sqme programatically

class UploadTests(TestCase):
    def setUp(self):
        # The test client is a Python class that acts as a dummy Web browser
        self._client = Client()

        # populate database
        self.populate = Command()
        self.populate.handle()

        # data is a pointer to workflow, users and categories names
        self.data = self.populate.getData()

    def test_0_form_workflow_add_manually(self):
        # create auxiliary json file
        jsonFileName = "/tmp/workflow.json"
        f = open(jsonFileName, "w")
        f.write(self.populate.getJson())
        f.close()
        upload_file = open(jsonFileName, "rb")
        file_dict = {NAME_JSON: SimpleUploadedFile(upload_file.name, upload_file.read())}

        # get category IDs for the select Category field
        category0 = Category.objects.get(name=self.data[CATEGORY][0])
        category1 = Category.objects.get(name=self.data[CATEGORY][1])
        # new workflow name
        workFlowName = 'workflow999'
        data_dict = {
            NAME_NAME: workFlowName,
            NAME_CATEGORY: [category0.id, category1.id],
            NAME_KEYWORDS: self.populate.getParragraph(1, 14),
            NAME_DESCRIPTION: self.populate.getParragraph(23, 123),
            NAME_VERSION: '3.1415',
        }

        # form with fieldfields has two independent dictionaries
        form = WorkFlowManualForm(data=data_dict, files=file_dict)
        self.assertTrue(form.is_valid(), form.errors)
        if form.is_valid():
            file_data = form.cleaned_data["json"].read().decode("utf-8")
            # modify object json value
            form.instance.json = file_data
        newWorkflow = form.save()
        self.assertEqual(newWorkflow.name, workFlowName)

        # Note that we are ignoring recaptcha
        # there is no simple way to automatize it

    def test_1_form_workflowProgStep1_add(self):
        # create auxiliary json file
        jsonFileName = "/tmp/workflow.json"
        f = open(jsonFileName, "w")
        f.write(self.populate.getJson())
        f.close()
        upload_file = open(jsonFileName, "rb")
        file_dict = {NAME_JSON: SimpleUploadedFile(upload_file.name, upload_file.read())}

        # new workflow name
        workFlowName = 'workflow999'
        data_dict = {
            NAME_VERSION: '3.141592',
        }
        # form with fieldfields has two independent dictionaries
        # we are testing the form not the views
        form = WorkFlowProgStep1Form(data=data_dict, files=file_dict)
        self.assertTrue(form.is_valid(), form.errors)

    def test_2_form_workflowProgStep2_add(self):
        # get category IDs for the select Category field
        category0 = Category.objects.get(name=self.data[CATEGORY][0])
        category1 = Category.objects.get(name=self.data[CATEGORY][1])
        # new workflow name
        workFlowName = 'workflow999'
        data_dict = {
            NAME_NAME: workFlowName,
            NAME_CATEGORY: [category0.id, category1.id],
            NAME_KEYWORDS: self.populate.getParragraph(1, 14),
            NAME_DESCRIPTION: self.populate.getParragraph(23, 123),
            NAME_VERSION: '3.1415',
        }

        # form with fieldfields has two independent dictionaries
        form = WorkFlowProgStep2Form(data=data_dict, )
        self.assertTrue(form.is_valid(), form.errors)
        if form.is_valid():
            file_data = self.populate.getJson()
            # modify object json 2alue
            form.instance.json = file_data
        newWorkflow = form.save()
        self.assertEqual(newWorkflow.name, workFlowName)

        # Note that we are ignoring recaptcha
        # there is no simple way to automatize it

    # Now test views

    def test_4_view_workflow_add_manually(self):
        # create auxiliary json file
        jsonFileName = "/tmp/workflow.json"
        f = open(jsonFileName, "w")
        f.write(self.populate.getJson())
        f.close()
        upload_file = open(jsonFileName, "rb")
        file = SimpleUploadedFile(upload_file.name, upload_file.read())

        workFlowName = 'workflow999'
        category0 = Category.objects.get(name=self.data[CATEGORY][0])
        category1 = Category.objects.get(name=self.data[CATEGORY][1])

        version = '3.1415'
        response = self._client.post(reverse(WORKFLOW_ADD_MANUALLY),
                                     data={
                                         NAME_NAME: workFlowName,
                                         NAME_KEYWORDS: self.populate.getParragraph(1, 14),
                                         NAME_CATEGORY: [category0.id, category1.id],
                                         NAME_DESCRIPTION: self.populate.getParragraph(23, 123),
                                         NAME_VERSION: version,
                                         NAME_JSON: file
                                     }
                                     )
        workflow = WorkFlow.objects.get(name=workFlowName)
        self.assertEqual(workflow.versionInit, version)

    def test_5_view_workflow_add_programatically(self):
        # create auxiliary json file
        jsonFileName = "/tmp/workflow.json"
        f = open(jsonFileName, "w")
        f.write(self.populate.getJson())
        f.close()
        upload_file = open(jsonFileName, "rb")
        file = SimpleUploadedFile(upload_file.name, upload_file.read())

        workFlowName = 'workflow999'
        category0 = Category.objects.get(name=self.data[CATEGORY][0])
        category1 = Category.objects.get(name=self.data[CATEGORY][1])

        version = '3.1415'
        response = self._client.post(reverse(WORKFLOW_PROG_STEP1),
                                     data={
                                         NAME_VERSION: version,
                                         NAME_JSON: file
                                     }
                                     )
        self.assertIn("jsonFileName", response.content.decode("utf-8"))
        _dict = json.loads(response.content.decode("utf-8"))


        # call with GET (send filename)
        fileNameUrl = "?jsonFileName=%s&versionInit=%s" % \
                      (_dict['jsonFileName'], version)
        response = self._client.get(reverse(WORKFLOW_PROG_STEP2)+fileNameUrl)

        # workflow should not be available yet.
        try:
             workflow = WorkFlow.objects.get(name=workFlowName)
             self.assertTrue(False, "This workflow should not exist")
        except ObjectDoesNotExist:
            pass

        # call with POST (send metadata)
        response = self._client.post(reverse(WORKFLOW_PROG_STEP2),
                                     data={
                                         NAME_NAME: workFlowName,
                                         NAME_KEYWORDS: self.populate.getParragraph(1, 14),
                                         NAME_CATEGORY: [category0.id, category1.id],
                                         NAME_DESCRIPTION: self.populate.getParragraph(23, 123),
                                         NAME_VERSION: version, # from json
                                         # NAME_JSON: file - in session variable
                                     }
                                     )
        workflow = WorkFlow.objects.get(name=workFlowName)
        self.assertEqual(workflow.versionInit, version)
