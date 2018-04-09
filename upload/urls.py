from django.conf.urls import url
from upload import views

app_name = 'upload'

urlpatterns = [
    url(r'^workflow_add_manually/$', views.workflow_add_manually, name='workflow_add_manually'),
    url(r'^workflowProgStep1_add/$', views.workflowProgStep1_add, name='workflowProgStep1_add'),
    url(r'^workflowProgStep2_add/$', views.workflowProgStep2_add, name='workflowProgStep2_add'),
]

