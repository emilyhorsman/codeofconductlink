from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='new'),
    url(r'^(?P<pk>[0-9]+)/detail$', views.detail, name='detail')
]
