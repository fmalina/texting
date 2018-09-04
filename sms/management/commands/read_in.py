""" Read texts into the db and delete them from SIM """
from django.core.management.base import BaseCommand
from modem import list_devices
from humod.siminfo import full_sms_list
from sms.models import Sms, Sim, safe_no, get_cat
import settings


def read_in():
    modems, device, info = list_devices()
    i=0
    for m in modems:
        modem = m['modem']
        sim = m['sim']
        if not modem:
            continue
        texts = full_sms_list(modem, 'inbox')
        for t in texts:
            try:
                txt = t['txt'].encode('ascii', 'ignore')
            except UnicodeDecodeError: # MMS or OTA update
                txt = 'Can not decode MMS'
            sms = Sms(
                sim=sim,
                no=safe_no(t['no']),
                txt=txt,
                at=t['at'],
                typ='r'
            )
            sms.cat = get_cat(sms)
            sms.save()
            modem.sms_del(int(t['id']))
            i+=1
    if i:
        msg = 'Saved %d replies.' % i
        print(msg)
        return msg


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        read_in()
