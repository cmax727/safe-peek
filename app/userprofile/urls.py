from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.userprofile.views',
    url(r'^$', 'main', name='main_page'),
    url(r'^(?P<username>[-\.\w]+)/$', 'profile_detail', name='detail'),
    url(r'^(?P<username>[-\.\w]+)/edit/$', 'edit', name='edit'),
    url(r'^(?P<username>[-\.\w]+)/groups/$', 'user_groups', name='user_groups'),
    url(r'^messages/setread/$', 'setread', name='setread'),
    url(r'^messages/setunread/$', 'setunread', name='setunread'),
    url(r'^statuses/$', 'statuses', name='statuses'),
    url(r'^write_status$', 'write_status', name='write_status'),
    url(r'^comment/(?P<id>(\d)+)/$', 'comment', name='comment'),
)
