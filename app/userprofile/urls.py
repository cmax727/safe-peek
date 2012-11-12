from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.userprofile.views',
    url(r'^$', 'main', name='main_page'),
    url(r'^(?P<username>[-\.\w]+)/$', 'profile_detail', name='detail'),
    # url(r'^removefriend/(?P<uname>\w+)/$', 'remove_friend', name='removefriend_page'),
)