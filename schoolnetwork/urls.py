from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nutrition.views.home', name='home'),
    # url(r'^nutrition/', include('nutrition.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^messages/', include('postman.urls')),
    url(r'^relationships/', include('friendship.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('app.panel.urls', namespace='panel')),
    url(r'', include('app.friendships.urls', namespace='friendships')),
       (r'^accounts/', include('allauth.urls')),
       (r'^avatar/', include('avatar.urls')),


    # url(r'^accounts/signup/$', 'registration.views.register', {
    #     'backend': 'registration.backends.default.DefaultBackend',
    #     'form_class': UserRegistrationForm}, name='registration_register'),

    # url(r'^accounts/', include('registration.backends.default.urls')),
    # (r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
    #     {'post_reset_redirect': '/accounts/password/reset/done/'}),
    # (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    # (r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
    #     {'post_reset_redirect': '/accounts/password/done/'}),
    # (r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }))
