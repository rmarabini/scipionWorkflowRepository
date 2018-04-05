from django import forms
from data.models import WorkFlow


class WorkFlowFormBase(forms.ModelForm):
    #  An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = WorkFlow
        fields = ('name', 'category',
                  'keywords', 'description',
                  'versionInit')

# in this form you upload a file
class WorkFlowForm(WorkFlowFormBase):
    json = forms.FileField(required=True, label="Workflow File")  #

# in this form you give the name of the file already uploaded
class WorkFlowFileModelForm(WorkFlowFormBase):
    pass

class WorkFlowFileForm(forms.Form):
    json = forms.FileField(required=True, label="Workflow File")
    versionInit = forms.CharField(required=False, initial="-1.0")
