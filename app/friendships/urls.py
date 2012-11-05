from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
#from django.views.generic import DetailView, ListView
#from app.product.models import Products


urlpatterns = patterns('app.friendships.views',
    url(r'^$', 'main', name='main_page'),
)
