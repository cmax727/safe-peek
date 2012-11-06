
from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
#from django.views.generic import DetailView, ListView
#from app.product.models import Products


urlpatterns = patterns('app.friendships.views',
    url(r'^$', 'main', name='main_page'),
    url(r'^inbox/$', 'inbox', name='inbox_page'),
    url(r'^write/$', 'write', name='write_page'),
    url(r'^sent/$', 'sent', name='sent_page'),
    url(r'^reply/$', 'reply', name='reply_page'),
    url(r'^trash/$', 'trash', name='trash_page'),
    url(r'^messages/', 'messages', include('postman.urls')),
)