from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Count
from modem import list_devices
from humod.siminfo import show_operator, show_phone_no, full_sms_list, BOXES, system_info, seq
from sms.models import *
from sms.forms import *
from sms import gateway_api
from sms.stats import get_stats, least_used
from paging import simple_paging
import datetime as dt
import time, random
import unicodedata


def index(r):
    modems, modem, info = list_devices()
    return render(r, 'sms/index.html', {
        'modems': modems, 'info': info})

def box(r, box, dev=0):
    if box not in BOXES.keys():
        raise Http404
    
    modems, device, info = list_devices(dev)
    modem = device['modem']
    sim   = device['sim']
    
    if modem:
        from_db, source = False, 'GPS device'
        texts = full_sms_list(modem, box)
        count = len(texts)
        paging = False
    else:
        from_db, source = True, 'local database'
        box_typ = {'inbox': 'r', 'sent': 's', 'outbox': ''}
        texts = Sms.objects.filter(sim=sim, typ=box_typ[box])
        texts, count, paging = simple_paging(r, texts, 100)
    
    return render(r, 'sms/box.html', {
        'box': box,
        'device': int(dev),
        'texts': texts,
        'source': source, 'from_db': from_db,
        'count': count, 'paging': paging,
        'modems': modems, 'info': info})

def day(r, pk, box, date):
    """Daily view for chosen SIM. Linked from stats."""
    date = dt.datetime.strptime(date, '%Y/%m/%d')
    sim = get_object_or_404(Sim, pk=pk)
    texts = Sms.objects.filter(sim=sim, at__range=(
        dt.datetime.combine(date, dt.time.min),
        dt.datetime.combine(date, dt.time.max)))
    cnt = lambda t: len([x for x in texts if x.typ==t])
    return render(r, 'sms/box.html', {
        'box': str(sim),
        'from_db': True,
        'texts': texts,
        'sent_cnt': cnt('s'),
        'recd_cnt': cnt('r'),
        'count': len(texts)})

def status(r, dev=0):
    tripletise = lambda x: ' '.join(seq(str(x), 3))
    
    modems, device, info = list_devices(dev)
    modem = device['modem']
    sim   = device['sim']
    if modem:
        state = system_info(modem)
        rssi = modem.get_rssi()
        imei = modem.show_imei()
        state['Signal'] = '<i class="i gt"></i>' * rssi + ' %s' % rssi
        state['IMEI'] = tripletise(imei)
        state['Phone'] = show_phone_no(modem) or sim.no
        state['Operator'] = show_operator(modem) or 'No operator'
    else:
        imei = False
        state = {
            'Phone': sim.no,
            'Operator': sim.net.name
        }
    state['IMSI'] = tripletise(sim.imsi)
    return render(r, 'sms/status.html', {
        'state': state,
        'sim': sim,
        'imei': imei,
        'modems': modems, 'info': info})

def send(r, dev=0, no=''):
    modems, device, info = list_devices(dev)
    modem = device['modem']
    sim   = device['sim']
    
    initial = {}
    no = safe_no(no)
    texts = []
    if no:
        initial['no'] = no
        texts = Sms.objects.filter(no=no)
    form = SendForm(r.POST or None, initial=initial)
    if device and form.is_valid():
        cd = lambda k: form.cleaned_data.get(k, '')
        txt = cd('txt')
        numbers = []
        sms = None
        for no in cd('no').split(','):
            no = safe_no(no)
            numbers.append(no)
            sms = Sms(no=no, sim=sim, typ='s', txt=txt)
            sms.save()
            if modem:
                try:
                    modem.sms_send(sms.no, sms.txt)
                except Exception as e:
                    info.append(('Failed %s: "%s"' % (sms.no, sms.txt), e, dev))
                time.sleep(random.random())
        if not modem and sms:
            numbers = ','.join(numbers) # send all in one API call
            gateway_api.send(sim, numbers, sim.no, txt, sms.pk)
                
        return redirect('box', dev=dev, box='inbox')
    return render(r, 'sms/form.html', {
        'form': form,
        'texts': texts,
        'title': 'Send a text',
        'modems': modems, 'info': info})

def api_inbound(request):
    if 'to' not in request.GET:
        return HttpResponse('Listening...')
    _to, no, txt = gateway_api.receive(request.GET)
    # TODO sort out UTF8mb4 handling
    txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore')

    sim = gateway_sim() # not using request.GET['to']
    sms = Sms(sim=sim, no=safe_no(no), txt=txt, at=datetime.now(), typ='r')
    sms.cat = get_cat(sms)
    sms.save()
    return HttpResponse('ok')

def api_status_update(request):
    if 'to' not in request.GET:
        return HttpResponse('Listening...')
    _to, ref, _smsref, status = gateway_api.status(request.GET)
    if ref:
        sms = Sms.objects.get(pk=int(ref))
        sms.state = status[0].lower()
        sms.save()
        return HttpResponse('ok')
    return HttpResponse('No reference #')

def rm(request, dev=0, id=None):
    if dev=='db':
        sms = get_object_or_404(Sms, pk=int(id))
        sms.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        modems, device, info = list_devices(dev)
        modem = device['modem']
        if modem:
            modem.sms_del(int(id))
    return redirect('box', dev=dev, box='inbox')

def stat(request):
    return render(request, 'sms/stats.html', {
        'dates': get_stats(),
        'suggest': least_used()
    })

def sort(request):
    texts = Sms.objects.filter(typ='r', cat__isnull=True)
    texts, count, paging = simple_paging(request, texts, 100)
    return render(request, 'sms/sort.html', {
        'title': 'Sort incoming messages',
        'texts': texts,
        'count': count, 'paging': paging,
        'cats': Cat.objects.all()
    })

def tag(request, id, cat_id):
    cat = get_object_or_404(Cat, pk=int(cat_id))
    sms = get_object_or_404(Sms, pk=int(id))
    same = Sms.objects.filter(txt__iexact=sms.txt.lower())
    same.update(cat=cat)
    return HttpResponse('Tagged: %s' % cat.name)

def cat(request, cat_id):
    cat = get_object_or_404(Cat, pk=int(cat_id))
    ls = Sms.objects.filter(cat=cat).values('txt')\
            .annotate(Count('txt')).order_by('-txt__count')
    return render(request, 'sms/sort.html', {
        'texts': ls,
        'title': cat.name
        })

panels = {
   'cat': (Cat, CatForm),
   'tpl': (Tpl, TplForm),
   'sim': (Sim, SimForm),
   'net': (Net, NetForm)
}

def ls(request, p):
    """Generic listing of objects"""
    model = panels[p][0]
    return render(request, 'sms/ls.html', {
        'ls': model.objects.all(),
        'pane': p,
        'item': model._meta
        })

def form(request, pk=None, delete=False, p='sim'):
    model, form = panels[p]
    name = model._meta.verbose_name
    done = p+'s'
    ins = None
    title = 'New %s' % name
    if pk:
        ins = get_object_or_404(model, pk=pk)
        title = '%s: %s' % (name, ins)
    if delete:
        ins.delete()
        return redirect(done)
    form = form(request.POST or None, instance=ins)
    if form.is_valid():
        form.save()
        return redirect(done)
    return render(request, 'sms/form.html', {'form': form, 'title': title})
