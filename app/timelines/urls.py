from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.timelines.views',
    url(r'^(?P<id>(\d)+)/$', 'detail', name='detail'),
    url(r'^main/$', 'main', name='main'),
    url(r'^write/$', 'write', name='write'),
    url(r'^text/$', 'text', name='text'),
    url(r'^picture/$', 'picture', name='picture'),
    url(r'^video/$', 'video', name='video'),
    url(r'^attach/$', 'attach', name='attach'),
)
