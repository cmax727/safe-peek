from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.academy.views',
    url(r'^$', 'index', name='index'),
    url(r'^create/$', 'createuniversity', name='create_university'),
    url(r'^(?P<slug>[-\.\w]+)/course/$', 'course', name='course'),
    url(r'^(?P<slug>[-\.\w]+)/course/syllabus/create/(?P<id>(\d)+)/$', 'syllabus', name='create_syllabus'),
    url(r'^(?P<slug>[-\.\w]+)/course/files/(?P<id>(\d)+)/$', 'files', name='upload_file'),
    url(r'^(?P<slug>[-\.\w]+)/course/(?P<id>(\d)+)/$', 'detailcourse', name='detail_course'),
    url(r'^(?P<slug>[-\.\w]+)/course/join/(?P<id>(\d)+)/$', 'joincourse', name='join_course'),
    url(r'^(?P<slug>[-\.\w]+)/course/leave/(?P<id>(\d)+)/(?P<uid>(\d)+)/$', 'leavecourse', name='leave_course'),
    url(r'^(?P<slug>[-\.\w]+)/course/accept/(?P<id>(\d)+)/(?P<uid>(\d)+)/$', 'acceptcourse', name='accept_course'),
    url(r'^(?P<slug>[-\.\w]+)/course/assignment/create/(?P<id>(\d)+)/$', 'createassignment', name='create_assignment'),
    url(r'^(?P<slug>[-\.\w]+)/course/assignment/(?P<id>(\d)+)/$', 'detailassignment', name='detail_assignment'),
    url(r'^(?P<slug>[-\.\w]+)/$', 'detail', name='detail'),
    url(r'^(?P<slug>[-\.\w]+)/admins/$', 'university_admins', name='university_admins'),
    url(r'^(?P<slug>[-\.\w]+)/professors/$', 'university_professors', name='university_professors'),
    url(r'^(?P<slug>[-\.\w]+)/courses/create/$', 'university_create_course', name='university_create_course'),
    url(r'^(?P<id>(\d)+)/write/text/$', 'write_timeline', {'timeline_type': 'text'}, name='upload_text'),
    url(r'^(?P<id>(\d)+)/write/picture/$', 'write_timeline', {'timeline_type': 'picture'}, name='upload_picture'),
    url(r'^(?P<id>(\d)+)/write/youtube/$', 'write_timeline', {'timeline_type': 'youtube'}, name='upload_youtube'),
    url(r'^(?P<id>(\d)+)/write/file/$', 'write_timeline', {'timeline_type': 'file'}, name='upload_file'),
)
