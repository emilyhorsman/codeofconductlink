from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProjectIndex.as_view(), name='index'),
    url(r'^new/$', views.CreateProject.as_view(), name='create'),

    url(r'^(?P<pk>[0-9]+)/$',                   views.ProjectDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)-(?P<name>[-_\w]+)/$', views.ProjectDetail.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/update$', views.ProjectUpdate.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.ProjectDelete.as_view(), name='delete'),
    url(r'^(?P<project_pk>[0-9]+)/submissions/create$', views.SubmissionCreate.as_view(), name='create-submission'),
    url(r'^(?P<project_pk>[0-9]+)-(?P<project_name>[-_\w]+)/submission/create$', views.SubmissionCreate.as_view(), name='create-submission'),
    url(r'^(?P<project_pk>[0-9]+)/submissions/(?P<submission_pk>[0-9]+)/update$',
        views.SubmissionUpdate.as_view(), name='update-submission'),
    url(r'^(?P<project_pk>[0-9]+)/submissions/(?P<submission_pk>[0-9]+)/delete$',
        views.SubmissionDelete.as_view(), name='delete-submission'),

    url(r'^tag/(?P<tag>[-_\w]+)/$', views.ProjectIndexByTag.as_view(), name='list-by-tag'),

    url(r'^vouch/$', views.ToggleVouch.as_view(), name='vouch'),
    url(r'^verify/$', views.ToggleVerify.as_view(), name='verify'),
]
