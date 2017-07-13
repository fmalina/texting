from django.conf.urls import url
from sms import views as view

urlpatterns = [
    url(r'^$', view.index, name="index"),
    url(r'^(?P<dev>[0-9]+)/send$', view.send, name="send"),
    url(r'^(?P<dev>[0-9]+)/status$', view.status, name="status"),
    url(r'^(?P<dev>[0-9]+)/reply/(?P<no>[\+\-0-9a-zA-Z]+)$', view.send, name="reply"),
    url(r'^(?P<dev>[0-9]+)/(?P<box>[a-z]+)$', view.box, name="box"),
    url(r'^(?P<pk>[0-9]+)/(?P<box>[a-z]+)/(?P<date>[0-9]{4}/[0-9]{2}/[0-9]{2})$',
        view.day, name="day"),
    url(r'^(?P<dev>[a-z0-9]+)/rm/(?P<id>[0-9]+)$', view.rm, name="rm"),
    url(r'^tag/(?P<cat_id>[0-9]+)/(?P<id>[0-9]+)$', view.tag, name='tag'),
    url(r'^cat/(?P<cat_id>[0-9]+)$', view.cat, name='cat'),
    url(r'api/inbound', view.api_inbound, name='api_inbound'),
    url(r'api/status_update', view.api_status_update, name='api_status_update'),
    url(r'sort', view.sort, name='sort'),
    url(r'stat', view.stat, name='stat')
]
for p in ('cat', 'tpl', 'sim', 'net'):
    urlpatterns += [
        url(p+'s$', view.ls, {'p': p}, name=p+'s'),
        url(p+'$', view.form, {'p': p}),
        url(p+'/(?P<pk>[0-9]+)$', view.form, {'p': p}, name='edit_'+p),
        url(p+'-del/(?P<pk>[0-9]+)$', view.form, {'p': p, 'delete': True}),
    ]
