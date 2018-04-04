from django import forms
from data.models import WorkFlow

class WorkFlowForm(forms.ModelForm):
    json = forms.FileField(required=True, label="Workflow File")  #
    # required=True is the default,
                                           # but I'm being explicit

    #  An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = WorkFlow
        fields = ('name', 'category', 'keywords', 'description')

class WorkFlowFileForm(forms.Form):
    json = forms.FileField(required=True, label="Workflow File")
    jsonFileName = forms.CharField(widget = forms.HiddenInput())
