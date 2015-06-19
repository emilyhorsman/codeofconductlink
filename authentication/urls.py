from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    """
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={ 'next_page': '/' }),
    url(r'^reset/$', auth_views.password_reset, name='password_reset'),
    """
]
