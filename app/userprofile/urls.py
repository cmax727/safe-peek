from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.userprofile.views',
    url(r'^$', 'main', name='main_page'),
    url(r'^(?P<id>(\d)+)/create_event/$', 'personal_event', name='create_events'),
    url(r'^my-grades/$', 'my_grades', name='my_grades'),
    url(r'^(?P<username>[-\.\w]+)/$', 'profile_detail', name='detail'),
    url(r'^(?P<username>[-\.\w]+)/edit/$', 'edit', name='edit'),
    url(r'^(?P<username>[-\.\w]+)/groups/$', 'user_groups', name='user_groups'),
    url(r'^messages/setread/$', 'setread', name='setread'),
    url(r'^messages/setunread/$', 'setunread', name='setunread'),
    url(r'^write/text/$', 'update_timeline', {'timeline_type': 'text'}, name='upload_text'),
    url(r'^write/picture/$', 'update_timeline', {'timeline_type': 'picture'}, name='upload_picture'),
    url(r'^write/youtube/$', 'update_timeline', {'timeline_type': 'youtube'}, name='upload_youtube'),
    url(r'^write/file/$', 'update_timeline', {'timeline_type': 'file'}, name='upload_file'),
)
