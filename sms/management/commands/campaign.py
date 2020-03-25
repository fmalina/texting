from django.core.management.base import BaseCommand
from django.conf import settings
from sms.models import Sms, Tpl, Sim
from sms.stats import least_used
from sms import gateway_api
from modem import list_devices
from datetime import datetime, timedelta
from time import sleep
import greeting
import urllib.request
import urllib.parse
import random
import json
import humod

greetings = greeting.timely_greeting()


def duplicates(no):
    now = datetime.now()
    return Sms.objects.filter(
        typ='s', no=no,
        at__range=(now - timedelta(days=180), now)
    ).count() > 1


def choose_modem_by_usage(devices):
    """Combine SIM stats and connected devices, ignoring unused SIMs
    Return least frequently used (LFU) SIM and its modem.
    """
    usage = least_used(get_list=True)
    lfu = []
    for sim, sent in usage:
        for m in devices:
            if m['sim']==sim:
                m['sent'] = sent
                lfu.append(m)
    try:
        l = lfu[0]
    except IndexError:
        return Sim.objects.get(net__name='SMSBCAST'), False
    return l['sim'], l['modem']


def send_one_text(modem, sim, txt, no, name=''):
    if name:
        txt = txt.replace("Hi,", f"Hi {name},")
    sms = Sms(typ='s', sim=sim, txt=txt, no=no)
    if settings.TEXTING_RUN and modem:
        try:
            modem.sms_send(sms.no, sms.txt)
            sms.save()
            sleep(random.random())
            return no
        except humod.errors.AtCommandError as e:
            print('ERROR', e, no)
            sleep(1)
            return False
    elif settings.TEXTING_RUN:
        sms.save()  # save 1st, so pk is ready for status update
        gateway_api.send(sim, sms.no, sim.no, sms.txt, sms.pk)
        return no


def send_texts(cat, nums):
    tpl = Tpl.objects.get(name=cat)
    txt = tpl.tpl.replace('{greeting}', greetings)

    devices, _modem, _info = list_devices()
    sim, modem = choose_modem_by_usage(devices)

    sent = []
    print(f'\n{cat.upper()}  {sim}')
    print(f'{txt} ({len(txt)} chars)')
    i = 0
    for i, number_name in enumerate(nums):
        no, name = number_name
        ok = True
        if not duplicates(no):
            ok = send_one_text(modem, sim, txt, no, name)
        if ok:
            sent.append(no)
    mark_used(sent)
    return i+1, modem, sim


def text_managers(modem, sim, msg):
    for no in settings.MANAGER_PHONE.split(','):
        send_one_text(modem, sim, msg, no)


def mark_used(sent):
    nums = ', '.join(sent)
    data = urllib.parse.urlencode({'numbers': nums}).encode()
    rqst = urllib.request.Request(settings.TEXTING_API_URL, data)
    return urllib.request.urlopen(rqst).read()


def pull_numbers_and_send():
    datastr = urllib.request.urlopen(settings.TEXTING_API_URL,
                                     timeout=15).read().decode()
    data = json.loads(datastr)
    alerts = []
    for cat, nums in data.items():
        if nums:
            i, modem, sim = send_texts(cat, nums)
            alerts.append(f'{i} {cat.lower()}')
    if settings.TEXTING_RUN and alerts:
        msg = ', '.join(alerts)
        text_managers(modem, sim, msg)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        pull_numbers_and_send()
