
from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xxx.views.home', name='home'),
    # url(r'^xxx/', include('xxx.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ('^$', index),
    ('^index/$', index),

    ('^join/$', join),
    ('^list/persons/$', list_persons),

    ('^persons/(.*?)/rotate_picture/$', rotate_picture),

    ('^mini/header/(.*?)/$', mini_header),

)
# This will work if DEBUG is True
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
