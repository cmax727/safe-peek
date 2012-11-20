from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.academy.views',
    url(r'^course/create/$', 'createcourse', name='create_course'),
    url(r'^course/$', 'course', name='course'),
)
