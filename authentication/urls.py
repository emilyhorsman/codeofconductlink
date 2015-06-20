from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from . import views

urlpatterns = [
    url(r'^$', views.ProfileDetail.as_view(), name='detail'),
    url(r'^register/$', views.CreateProfile.as_view(), name='register'),
]
