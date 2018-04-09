
from unittest import TestCase
from django.test import Client
from data.models import Category, WorkFlow, User
from data.management.commands.populate import Command, CATEGORY, USER, WORKFLOW

#DO NOT MODIFIED ANYTHING BELLOW THIS POINT
#very basic model testing, we just check the new objects exists
class modelsTests(TestCase):
    def setUp(self):
        #populate database
        self.populate = Command()
        self.populate.handle()

    def test_Category(self):
        baseName = CATEGORY
        for itemName in self.populate.data[baseName]:
            try:
                object = Category.objects.get(name=itemName)
            except Category.DoesNotExist:
                self.assertTrue(False, "%s: %s does not exist" % (baseName, itemName) )
            print("checked: %s" % itemName)

    def test_User(self):
        baseName = USER
        for itemName in self.populate.data[baseName]:
            try:
                object = User.objects.get(username=itemName)
            except Category.DoesNotExist:
                self.assertTrue(False, "%s: %s does not exist" % (baseName, itemName) )
            print("checked: %s" % itemName)

    def test_Workflow(self):
        baseName = WORKFLOW
        for itemName in self.populate.data[baseName]:
            try:
                object = WorkFlow.objects.get(name=itemName)
            except Category.DoesNotExist:
                self.assertTrue(False, "%s: %s does not exist" % (baseName, itemName) )
            print("checked: %s" % itemName)
