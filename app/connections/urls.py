from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.connections.views',
    url(r'^search/$', 'search', name='search'),
    url(r'^add/(?P<username>[-\.\w]+)/$', 'add', name='add'),
)
