from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.events.views',
    url(r'^(?P<id>(\d)+)/$', 'detail', name='detail'),
    url(r'^main/$', 'main', name='main'),
    # url(r'^write/$', 'write', name='write'),
    url(r'^write/text/$', 'text', name='text'),
    url(r'^write/picture/$', 'picture', name='picture'),
    url(r'^write/video/$', 'video', name='video'),
    url(r'^write/attach/$', 'attach', name='attach'),
)
