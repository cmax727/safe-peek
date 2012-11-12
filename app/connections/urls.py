from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.connections.views',
    url(r'^search/$', 'search', name='search'),
    url(r'^friends/$', 'friends', name='friends'),
    url(r'^add/(?P<username>[-\.\w]+)/$', 'add', name='add'),
    url(r'^accept/(?P<req_id>\d+)/$', 'accept', name='accept'),
    url(r'^reject/(?P<req_id>\d+)/$', 'reject', name='reject'),
)