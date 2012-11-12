from django.conf.urls.defaults import *
from django.conf.urls import patterns, url


urlpatterns = patterns('app.friendships.views',
    url(r'^search$', 'search', name='search_page'),
    (r'^accounts/', include('allauth.urls')),
)
