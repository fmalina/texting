from django.conf.urls import url
from django.shortcuts import redirect
from sms.views import index, send, status, box, day, rm, tag, cat,\
                      api_inbound, api_status_update, sort, stat, ls, form
import settings

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^(?P<dev>[0-9]+)/send$', send, name="send"),
    url(r'^(?P<dev>[0-9]+)/status$', status, name="status"),
    url(r'^(?P<dev>[0-9]+)/reply/(?P<no>[\+\-0-9a-zA-Z]+)$', send, name="reply"),
    url(r'^(?P<dev>[0-9]+)/(?P<box>[a-z]+)$', box, name="box"),
    url(r'^(?P<pk>[0-9]+)/(?P<box>[a-z]+)/(?P<date>[0-9]{4}/[0-9]{2}/[0-9]{2})$', day, name="day"),
    url(r'^(?P<dev>[a-z0-9]+)/rm/(?P<id>[0-9]+)$', rm, name="rm"),
    url(r'^tag/(?P<cat_id>[0-9]+)/(?P<id>[0-9]+)$', tag, name='tag'),
    url(r'^cat/(?P<cat_id>[0-9]+)$', cat, name='cat'),
    url(r'api/inbound', api_inbound, name='api_inbound'),
    url(r'api/status_update', api_status_update, name='api_status_update'),
    url(r'sort', sort, name='sort'),
    url(r'stat', stat, name='stat')
]
for p in ('cat', 'tpl', 'sim', 'net'):
    urlpatterns += [
        url(p+'s$', ls, {'p': p}, name=p+'s'),
        url(p+'$', form, {'p': p}),
        url(p+'/(?P<pk>[0-9]+)$', form, {'p': p}, name='edit_'+p),
        url(p+'-del/(?P<pk>[0-9]+)$', form, {'p': p, 'delete': True}),
    ]
