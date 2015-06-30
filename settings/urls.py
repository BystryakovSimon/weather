# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(''
    ,url(r'^weather/', include('weather.urls'))

#    ,url(r'^admin/', include(admin.site.urls))

    , url(r'^admin/jsi18n', 'django.views.i18n.javascript_catalog')
    , url(r'^admin_tools/', include('admin_tools.urls'))
    , url(r'^admin/', include(admin.site.urls))
    , url(r'^', include('cms.urls'))

    , (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog')

    #url(r'^', include('clickmuncher.urls')),

    #url(r'^', include('wdaemon.urls')),

#    url(r'^auth/', 'lib.views.auth'),
#    url(r'^logout_user/$', 'lib.views.logout_user'),

    # Examples:
    # url(r'^$', 'weather.views.home', name='home'),
    # url(r'^weather/', include('weather.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns