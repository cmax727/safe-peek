from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.timelines.views',
    url(r'^(?P<id>(\d)+)/$', 'detail', name='detail'),
)