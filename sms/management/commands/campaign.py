from django.core.management.base import BaseCommand
from django.core.mail import mail_admins
from greeting import timely_greeting
from sms.models import Sms
from sms.stats import least_used
from sms.parallel import parallel
from sms import gateway_api
from modem import list_devices
from datetime import datetime, timedelta
from time import sleep
from settings_campaign import *
import settings
import urllib.request
import urllib.parse
import random
import json
import humod

greetings = timely_greeting()

def duplicates(no):
    now = datetime.now()
    return Sms.objects.filter(typ='s', no=no,
        at__range=(now - timedelta(days=180), now)).count() > 1

def choose_modem_by_usage(devices):
    """Combine SIM stats and connected devices, ignoring unused SIMs
    Return least frequently used (LFU) SIM and its modem."""
    usage = least_used(get_list=True)
    lfu = []
    for sim, sent in usage:
        for m in devices:
            if m['sim']==sim:
                m['sent'] = sent
                lfu.append(m)
    l = lfu[0] # later this could give alternative if modem doesn't respond
    return l['sim'], l['modem']

def send_one_text(modem, sim, txt, no, name=''):
    if name:
        txt = txt.replace("Hi,", "Hi %s," % name)
    sms = Sms(typ='s', sim=sim, txt=txt, no=no)
    if RUN and modem:
        try:
            modem.sms_send(sms.no, sms.txt)
            sms.save()
            sleep(random.random())
            return no
        except humod.errors.AtCommandError as e:
            print('ERROR', e, no)
            sleep(1)
            return False
    elif RUN:
        sms.save() # save 1st, so pk is ready for status update
        gateway_api.send(sim, sms.no, sim.no, sms.txt, sms.pk)
        return no

def send_texts(cat, nums):
    txt = TEXTS[CATEGORIES[cat]]
    txt = custom_replace(txt, cat, greetings)

    devices, _modem, _info = list_devices()
    sim, modem = choose_modem_by_usage(devices)

    sent = []
    print('\n%s  %s' % (cat.upper(), sim))
    print('%s (%s chars)' % (txt, len(txt)))
    for i, number_name in enumerate(nums):
        no, name = number_name
        ok = True
        if not duplicates(no):
            ok = send_one_text(modem, sim, txt, no, name)
        if ok: sent.append(no)
    mark_used(sent)
    return i+1, modem, sim

def text_managers(modem, sim, msg):
    for no in settings.MANAGER_PHONE.split(','):
        send_one_text(modem, sim, msg, no)

def mark_used(sent):
    nums = ', '.join(sent)
    data = urllib.parse.urlencode({'numbers': nums}).encode()
    rqst = urllib.request.Request(API_URL, data)
    return urllib.request.urlopen(rqst).read()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        datastr = urllib.request.urlopen(API_URL, timeout=15).read().decode()
        data = json.loads(datastr)
        alerts = []
        for cat, nums in data.items():
            if nums:
                i, modem, sim = send_texts(cat, nums)
                alerts.append('%s %s' % (i, cat.lower()))
        if RUN and alerts:
            msg = ', '.join(alerts)
            text_managers(modem, sim, msg)
