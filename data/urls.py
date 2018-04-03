from django.conf.urls import url
from . import views

app_name = 'data'

urlpatterns = [
    url(r'^$', views.workflow_list, name='workflow_list'),
    url(r'^workflow_list/(?P<category_slug>[-\w]+)/$', views.workflow_list, name='workflow_list_by_category'),
    url(r'^workflow_detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.workflow_detail, name='workflow_detail'),
    url(r'^workflow_download/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.workflow_download, name='workflow_download'),
    url(r'^workflow_search/$', views.workflow_search, name='workflow_search'),
    url(r'^workflow_add/$', views.workflow_add, name='workflow_add'),
    #url(r'^workflow_add_success/$', views.workflow_add_success, name='workflow_add_success'),
]

