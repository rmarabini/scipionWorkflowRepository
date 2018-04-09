from django import forms
from data.models import WorkFlow

class WorkFlowFormBase(forms.ModelForm):
    #  Basic form with no file information

    class Meta:
        # Provide an association between the ModelForm and a model
        model = WorkFlow
        fields = ('name', 'category',
                  'keywords', 'description',
                  'versionInit')
        labels = {'versionInit': 'Version'}
        widgets = {'name': forms.TextInput(attrs={'size': 64}),
                   'keywords': forms.TextInput(attrs={'size': 64}),
                   'description': forms.Textarea(attrs={'cols': '64', 'rows': '10'}),
                   'versionInit': forms.TextInput(attrs={'size': 64}),
                   }


class WorkFlowManualForm(WorkFlowFormBase):
    # add file upload to basic form
    json = forms.FileField(required=True, label="Workflow File")  #

class WorkFlowProgStep2Form(WorkFlowFormBase):
    # file already upladed and save in session variable
    pass

class WorkFlowProgStep1Form(forms.Form):
    # upload file and version, save them in sesssion variables
    # returns json con serverside name of the file and version
    json = forms.FileField(required=True, label="Workflow File")
    versionInit = forms.CharField(required=False, initial="-1.0")
