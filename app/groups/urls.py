from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.groups.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<id>(\d)+)/$', 'detail', name='detail'),
    url(r'^create/$', 'create', name='create'),
    url(r'^delete/(?P<id>(\d)+)/$', 'delete', name='delete'),
    url(r'^join/(?P<id>(\d)+)/$', 'join', name='join'),
    url(r'^leave/(?P<id>(\d)+)/$', 'leave', name='leave'),
    url(r'^manage/(?P<id>(\d)+)/$', 'manage', name='manage'),
    url(r'^manage/(?P<id>(\d)+)/invite/$', 'invite', name='invite'),
    url(r'^manage/(?P<id>(\d)+)/write_groups/$', 'write_groups', name='write_groups'),
    url(r'^manage/(?P<id>(\d)+)/change-ownership/$', 'change_ownership', name='change_ownership'),
    url(r'^manage/(?P<id>(\d)+)/accept/(?P<user_id>(\d)+)/$', 'accept_membership', name='accept_membership'),
    url(r'^manage/(?P<id>(\d)+)/remove/(?P<user_id>(\d)+)/$', 'remove_membership', name='remove_membership'),
)
