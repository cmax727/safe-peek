from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.connections.views',
    url(r'^search/$', 'search', name='search'),
    url(r'^finduser/$', 'finduser', name='finduser'),
    url(r'^findlocation/$', 'findlocation', name='findlocation'),
    url(r'^friends/$', 'friends', name='friends'),
    url(r'^add/(?P<username>[-\.\w]+)/$', 'add', name='add'),
    url(r'^remove/(?P<username>[-\.\w]+)/$', 'add', name='remove'),
    url(r'^accept/(?P<req_id>\d+)/$', 'accept', name='accept'),
    url(r'^reject/(?P<req_id>\d+)/$', 'reject', name='reject'),
)
