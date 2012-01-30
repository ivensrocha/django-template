
# coding: utf-8
from django.conf.urls.defaults import patterns, url
from int.route import route
from django.views.generic.simple import redirect_to

urlpatterns = patterns('myAuth.views',
                       url(r'^signup/success/(?P<pk>\d+)/$', 'create_account_success', name='create_account_success'),
                       url(r'^signup/success/(?P<pk>\d+)$', 'create_account_success', name='create_account_success'),
                       url(r'^signup/success', redirect_to, {'url': '/signup/'}),
                       url(r'^signup/confirm/send/(?P<code>\w+)/$', 'send_confirmation_code', name='send_confirmation_code'),
                       url(r'^signup/confirm/send/(?P<code>\w+)$', 'send_confirmation_code', name='send_confirmation_code'),
                       url(r'^signup/confirm/(?P<code>\w+)/$', 'confirm_account', name='confirm_account'),
                       url(r'^signup/confirm/(?P<code>\w+)$', 'confirm_account', name='confirm_account'),
                       url(r'^signup/confirm', redirect_to, {'url': '/signup/'}),
                       route(r'^login/$', GET='login_get', POST='login_post', name='login'),
                       route(r'^login$', GET='login_get', POST='login_post', name='login'),
                       route(r'^signup/$', GET='create_account_get', POST='create_account_post', name='create_account'),
                       route(r'^signup$', GET='create_account_get', POST='create_account_post', name='create_account'),
                       url(r'^logout/$', 'logout_then_login', name='logout'),
                       url(r'^logout$', 'logout_then_login', name='logout'),
                       )
