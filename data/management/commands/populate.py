#populate database
# This code has to be placed in a file within the
# data/management/commands directory in your project.
# If that directory doesn't exist, create it.
# The name of the script is the name of the custom command,
# so let's call it populate.py. Another thing that has to be done
# is creating __init__.py files in both the management and commands
# directories, because these have to be Python packages.
#
# execute python manage.py  populate


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import django
import random

django.setup()

from data.models import Category, Protocol, WorkFlow
#models
CATEGORY = 'category'
USER = 'user'
WORKFLOW = 'workflow'
# The name of this class is not optional must  by Command
# otherwise manage.py will not process it properlly
class Command(BaseCommand):
    #  args = '<-no arguments>'
    # helps and arguments shown when command python manage.py help populate
    # is executed.
    help = 'This scripts populates de workflow database, no arguments needed.' \
           'Execute it with the command line python manage.py populate'

    data = {}

    def getData(self):
        return self.data

    def getParragraph(self, init, end):
        # getParragraph returns a parragraph, useful for testing
        if end > 445:
            end = 445
        if init < 0:
            init = 0
        return """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
deserunt mollit anim id est laborum."""[init:end]

    # handle is another compulsory name, This function will be
    # executed by default
    def handle(self, *args, **options):
        self.cleanDatabase()
        self.addCategory(CATEGORY)
        self.addUser(USER)
        self.addWorkflow(WORKFLOW, CATEGORY, USER)####### to be done

    def cleanDatabase(self):
        # delete all entries in database for
        # workflows, categories and users
        WorkFlow.objects.all().delete()
        Category.objects.all().delete()
        Protocol.objects.all().delete()
        User.objects.all().delete()

    def createObjects(self, objectName, numberOfObjects):
        # auxiliary function creates names to be used by categories, workflows and users
        data = self.data
        data[objectName] = []
        for i in range(1, numberOfObjects+1):
            data[objectName].append("%s%d"% (objectName, i))

    def addCategory(self, baseName):
        # create categories
        self.createObjects(baseName, 5)
        for item in self.data[baseName]:
            object = Category(name=item, tooltip="tooltip_" + item )
            object.save()
        #print (Category.objects.all())

    def addUser(self, baseName):
        # create users[**ALUMNO]
        self.createObjects(baseName, 4)
        for item in self.data[baseName]:
            object = User(first_name='fn_%s' % item,
                          last_name='ln_%s' % item,
                          username='%s' % item,
                          email='%s@gmail.com' % item,
                          password=item,
                          is_active=True)
            object.save()

    def addWorkflow(self, baseName, catName, userName):
        #create workflows [**ALUMNO]
        # create relationship with category
        numberOfCat = len(self.data[catName])
        # create relationship with user
        numberOfUsers = len(self.data[userName])
        # create fake json
        json = self.getJson() ### need to be improved
        # create random relationships
        numberWorkFlows = 13
        ########################################################
        self.createObjects(baseName, numberWorkFlows)
        flag = True
        for item in self.data[baseName]:
            #
            userIndex     = random.randint(0, numberOfUsers-1)
            author = User.objects.get(username=self.data[userName][userIndex])
            #
            categoryIndex = random.randint(0, numberOfCat-1)
            category = Category.objects.get(name=self.data[catName][categoryIndex])
            #
            keywords= "%s, %s" % (author.username, category.name)
            object = WorkFlow(name=item,
                              #category=category,
                              author=author,
                              versionInit="1.0",
                              keywords=keywords,
                              json=self.getJson(),
                              description = self.getParragraph(random.randint(0, 50),
                                                               random.randint(100, 456)
                                                               )
                              )
            object.save()
            object.category.add(category) # needs to have a value for field "id" before
                                          # this many-to-many relationship can be used
            if flag: # set two categories to the same workflow
                categoryIndex = random.randint(0, numberOfCat - 1)
                category = Category.objects.get(name=self.data[catName][categoryIndex])
                object.category.add(category)
                flag = False

    def getJson(self):
        return """[
    {
        "object.className": "ProtImportMovies",
        "object.id": "2",
        "object.label": "import movies",
        "object.comment": "\\n",
        "runName": null,
        "runMode": 0,
        "importFrom": 0,
        "filesPath": "",
        "filesPattern": "Falcon*.mrcs",
        "copyFiles": false,
        "acquisitionWizard": null,
        "voltage": 300.0,
        "sphericalAberration": 2.0,
        "amplitudeContrast": 0.1,
        "magnification": 39548,
        "samplingRateMode": 0,
        "samplingRate": 3.54,
        "scannedPixelSize": 14.0,
        "gainFile": null
    },
    {
        "object.className": "ProtMovieAlignment",
        "object.id": "40",
        "object.label": "movie alignment",
        "object.comment": "\\n",
        "runName": null,
        "runMode": 0,
        "cleanMovieData": true,
        "alignMethod": 0,
        "alignFrame0": 0,
        "alignFrameN": 0,
        "doGPU": false,
        "GPUCore": 0,
        "winSize": 150,
        "sumFrame0": 0,
        "sumFrameN": 0,
        "cropOffsetX": 0,
        "cropOffsetY": 0,
        "cropDimX": 0,
        "cropDimY": 0,
        "binFactor": 1,
        "extraParams": "",
        "hostName": "localhost",
        "numberOfThreads": 4,
        "numberOfMpi": 1,
        "inputMovies": "2.__attribute__outputMovies"
    },
    {
        "object.className": "ProtCTFFind",
        "object.id": "82",
        "object.label": "ctffind4",
        "object.comment": "\\n",
        "runName": null,
        "runMode": 0,
        "recalculate": false,
        "sqliteFile": null,
        "ctfDownFactor": 1.0,
        "useCftfind4": true,
        "astigmatism": 100.0,
        "findPhaseShift": false,
        "lowRes": 0.05,
        "highRes": 0.35,
        "minDefocus": 0.5,
        "maxDefocus": 4.0,
        "windowSize": 256,
        "hostName": "localhost",
        "numberOfThreads": 4,
        "numberOfMpi": 1,
        "inputMicrographs": "40.__attribute__outputMicrographs"
    },
    {
        "object.className": "EmanProtBoxing",
        "object.id": "369",
        "object.label": "eman2 - boxer",
        "object.comment": "",
        "runName": null,
        "runMode": 0,
        "inputMicrographs": "40.__attribute__outputMicrographs"
    },
    {
        "object.className": "ProtUserSubSet",
        "object.id": "380",
        "object.label": "3mics",
        "object.comment": "",
        "runName": null,
        "runMode": 0,
        "other": null,
        "sqliteFile": "Runs/000082_ProtCTFFind/ctfs_selection.sqlite,",
        "outputClassName": "SetOfMicrographs",
        "inputObject": "82.__attribute__outputCTF"
    },
    {
        "object.className": "XmippProtParticlePicking",
        "object.id": "420",
        "object.label": "xmipp3 - manual picking",
        "object.comment": "",
        "runName": null,
        "runMode": 0,
        "memory": 2.0,
        "inputMicrographs": "40.__attribute__outputMicrographs"
    },
    {
        "object.className": "XmippProtExtractParticles",
        "object.id": "449",
        "object.label": "extract 3 mics",
        "object.comment": "\\n",
        "runName": null,
        "runMode": 0,
        "micsSource": 0,
        "boxSize": 64,
        "doSort": false,
        "rejectionMethod": 0,
        "maxZscore": 3,
        "percentage": 5,
        "doRemoveDust": true,
        "thresholdDust": 3.5,
        "doInvert": true,
        "doFlip": false,
        "doNormalize": true,
        "normType": 2,
        "backRadius": -1,
        "hostName": "localhost",
        "numberOfThreads": 1,
        "numberOfMpi": 1,
        "ctfRelations": "82.__attribute__outputCTF",
        "inputCoordinates": "123.__attribute__outputCoordinates",
        "inputMicrographs": "369.outputMicrographs"
    },
    {
        "object.className": "XmippParticlePickingAutomatic",
        "object.id": "517",
        "object.label": "xmipp3 - auto-picking",
        "object.comment": "",
        "runName": null,
        "runMode": 0,
        "micsToPick": 0,
        "memory": 2.0,
        "hostName": "localhost",
        "numberOfThreads": 1,
        "numberOfMpi": 1,
        "xmippParticlePicking": "420"
    }
]"""

#There's no need to bypass manage.py, since it's a wonderful convenience wrapper around
        # the Django project administration tools. It can be used to create custom
        # management commands - e.g. your own commands parallel to shell, dumpdata,
        # and so on. Not only that creating such commands gives you a very succinct,
        # boilterplate-free way of writing custom management scripts, it also gives
        # you a natural location to house them, per application.


#('2D Refinement & Classification', 'self-explanatory,'),
#('3D Refinament & Classification', 'self-explanatory,'),
#('Courses', 'material used in Scipion courses'),
#('Data Collection', 'movie alignement, particle selection & CTF'),
#('Model Building', 'Methods to predict the atomic 3D structures of proteins'),
#('Localized Reconstruction', 'Localized reconstruction of subunits of macromolecular complexe'),
#('Tests', 'Scipion functiona test, usually good for ussage esamples'),
#('Uncategorized', 'Try not to use this category')
