from django import forms
from data.models import WorkFlow

class WorkFlowForm(forms.ModelForm):
#    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
#    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    jsonFileName = forms.FileField(required=True, label="Workflow File")  # required=True is the default,
                                           # but I'm being explicit

    #  An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = WorkFlow
        fields = ('name', 'category', 'keywords', 'description')
