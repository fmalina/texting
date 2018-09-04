# followup reply
from sms.models import Sms, Cat

texts = Sms.objects.filter(typ='r', cat=None)
fr, created = Cat.objects.get_or_create(name='Followup reply')

for sms in texts:
    sent = list(Sms.objects.filter(no=sms.no, typ='s'))
    last = None if not sent else sent[-1]
    # print(sms.at, len(sent), sms.txt)
    if len(sent) > 1 and sms.cat is None and last.at < sms.at:
        sms.cat = fr
        # print(last.at, 'FR')
        sms.save()
