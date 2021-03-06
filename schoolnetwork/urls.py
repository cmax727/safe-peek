from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^messages/', include('postman.urls')),
    url(r'^relationships/', include('friendship.urls')),
    url(r'^admin-panel/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^avatar/', include('avatar.urls')),
    #url(r'^tinymce/', include('tinymce.urls')),
    url(r'^groups/', include('app.groups.urls', namespace='groups')),
    url(r'^users/', include('app.connections.urls', namespace='connections')),
    url(r'^timelines/', include('app.timelines.urls', namespace='timelines')),
    url(r'^events/', include('app.events.urls', namespace='events')),
    url(r'^academy/', include('app.academy.urls', namespace='academy')),
    url(r'', include('app.userprofile.urls', namespace='userprofile')),
    url(r'^chat/', include('jqchat.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }))
