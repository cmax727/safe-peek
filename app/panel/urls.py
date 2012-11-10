from django.conf.urls.defaults import *
from django.conf.urls import patterns, url

#from django.views.generic import DetailView, ListView
#from app.product.models import Products


urlpatterns = patterns('app.panel.views',
    url(r'^$', 'main', name='main_page'),
    url(r'^removefriend/(?P<uname>\w+)/$', 'remove_friend', name='removefriend_page'),
    url(r'^signup/$', 'signup', name='signup_page'),
)
