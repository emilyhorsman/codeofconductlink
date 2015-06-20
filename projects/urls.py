from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.CreateProject.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/(?P<name>\w+)/detail$', views.ProjectDetail.as_view(), name='detail')
]
