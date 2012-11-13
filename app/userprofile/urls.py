from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.userprofile.views',
    url(r'^$', 'main', name='main_page'),
    url(r'^messages/setread/$', 'setread', name='setread'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^(?P<username>[-\.\w]+)/$', 'profile_detail', name='detail'),
)
