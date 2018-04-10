from django.conf.urls import url
from find import views

app_name = 'find'

urlpatterns = [
    url(r'^$', views.workflow_list, name='workflow_list'),
    url(r'^workflow_list/(?P<category_slug>[-\w]+)/$', views.workflow_list, name='workflow_list_by_category'),
    url(r'^workflow_detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.workflow_detail, name='workflow_detail'),
    url(r'^workflow_download/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.workflow_download, name='workflow_download'),
    url(r'^workflow_delete/(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.workflow_delete, name='workflow_delete'),
    url(r'^workflow_download_no_count/(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.workflow_download_no_count, name='workflow_download_no_count'),
    url(r'^workflow_search/$', views.workflow_search, name='workflow_search'),
]

