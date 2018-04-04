from django.conf.urls import url
from upload import views

app_name = 'upload'

urlpatterns = [
    url(r'^workflow_add/$', views.workflow_add, name='workflow_add'),
    url(r'^workflowFile_add/$', views.workflowFile_add, name='workflowFile_add'),
]

