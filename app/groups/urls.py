from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.groups.views',
    url(r'^create/$', 'create', name='create'),
    url(r'^(?P<groupname>[-\.\w]+)/$', 'detail', name='detail'),
    url(r'^$', 'index', name='index'),
)
