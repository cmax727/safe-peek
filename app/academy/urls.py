from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.academy.views',
    url(r'^create/$', 'createuniversity', name='create_university'),
    url(r'^course/create/$', 'createcourse', name='create_course'),
    url(r'^course/$', 'course', name='course'),
    url(r'^course/(?P<id>(\d)+)/$', 'detailcourse', name='detail_course'),
    url(r'^course/join/(?P<id>(\d)+)/$', 'joincourse', name='join_course'),
    url(r'^course/leave/(?P<id>(\d)+)/(?P<uid>(\d)+)/$', 'leavecourse', name='leave_course'),
    url(r'^course/accept/(?P<id>(\d)+)/(?P<uid>(\d)+)/$', 'acceptcourse', name='accept_course'),
)
