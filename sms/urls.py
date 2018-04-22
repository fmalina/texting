from django.urls import re_path
from sms import views as view

urlpatterns = [
    re_path(r'^$', view.index, name="index"),
    re_path(r'^(?P<dev>[0-9]+)/send$', view.send, name="send"),
    re_path(r'^(?P<dev>[0-9]+)/status$', view.status, name="status"),
    re_path(r'^(?P<dev>[0-9]+)/reply/(?P<no>[\+\-0-9a-zA-Z]+)$', view.send, name="reply"),
    re_path(r'^(?P<dev>[0-9]+)/(?P<box>[a-z]+)$', view.box, name="box"),
    re_path(r'^(?P<pk>[0-9]+)/(?P<box>[a-z]+)/(?P<date>[0-9]{4}/[0-9]{2}/[0-9]{2})$',
        view.day, name="day"),
    re_path(r'^(?P<dev>[a-z0-9]+)/rm/(?P<id>[0-9]+)$', view.rm, name="rm"),
    re_path(r'^tag/(?P<cat_id>[0-9]+)/(?P<id>[0-9]+)$', view.tag, name='tag'),
    re_path(r'^cat/(?P<cat_id>[0-9]+)$', view.cat, name='cat'),
    re_path(r'api/inbound', view.api_inbound, name='api_inbound'),
    re_path(r'api/status_update', view.api_status_update, name='api_status_update'),
    re_path(r'sort', view.sort, name='sort'),
    re_path(r'stat', view.stat, name='stat')
]
for p in ('cat', 'tpl', 'sim', 'net'):
    urlpatterns += [
        re_path(p+'s$', view.ls, {'p': p}, name=p+'s'),
        re_path(p+'$', view.form, {'p': p}),
        re_path(p+'/(?P<pk>[0-9]+)$', view.form, {'p': p}, name='edit_'+p),
        re_path(p+'-del/(?P<pk>[0-9]+)$', view.form, {'p': p, 'delete': True}),
    ]
