# coding: utf-8

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns['',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^req/', include('int.core.urls', namespace='core')),
    (r'^auth/', include('int.myAuth.urls', namespace='myAuth')),
  ]                     

urlpatterns += staticfiles_urlpatterns()
