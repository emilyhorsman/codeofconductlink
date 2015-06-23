from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/', views.CreateReport.as_view(), name='new'),
    url(r'^(?P<pk>[0-9]+)/update$', views.UpdateReport.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.DeleteReport.as_view(), name='delete'),
]
