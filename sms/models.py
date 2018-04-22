from django.db import models
from django.urls import reverse
from datetime import datetime


def digits_only(s):
    return ''.join([x for x in s if x.isdigit()])


def format_no(no):
    n = digits_only(str(no))
    if n:
        return n[:-6]+' '+n[-6:-3]+' '+n[-3:]
    return no  # Voicemail, T-Mobile, hidden caller ID


def safe_no(no):
    no = digits_only(no)
    if no.startswith('44'):
        no = '0'+no[2:]
    return no


class Net(models.Model):
    name = models.CharField("Network Operator", max_length=8)
    note = models.TextField("Notes", blank=True,
        help_text="Customer services number, top-up and packages details")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Network'
        verbose_name_plural = 'Networks'


class Sim(models.Model):
    imsi = models.CharField(max_length=25, null=True, blank=True, editable=False)
    no = models.CharField("Phone number", max_length=11,
        null=True, blank=True, help_text="registered for this SIM")
    serial = models.CharField("Serial No", max_length=25,
        null=True, blank=True, help_text="The long number written on the SIM")
    net = models.ForeignKey(Net, verbose_name="Operator", on_delete=models.CASCADE,
        null=True, blank=True, help_text="What network operator is it on?")
    ref = models.IntegerField("Reference #",
        null=True, blank=True, help_text="shows in the sidebar")
    active = models.BooleanField(default=False)
    url = models.CharField("URL", max_length=75,
        null=True, blank=True, help_text="Gateway/SIM topup URL")
    user = models.CharField("Username", max_length=25,
        null=True, blank=True, help_text="Gateway/SIM topup credentials")
    pwd = models.CharField("Password", max_length=25,
        null=True, blank=True)
    note = models.TextField("Any other notes?",
        help_text="About the package, topup etc.", blank=True)

    def __str__(self):
        u = ''
        if self.net: u += '%s' % self.net
        if self.ref: u += ' %s' % self.ref
        elif not self.net:
            u += 'Unknown'
        return u

    def nice_no(self):
        return format_no(self.no or '...')

    def get_absolute_url(self):
        return reverse('edit_sim', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ordering = ('net', 'ref')
        verbose_name = 'SIM'
        verbose_name_plural = 'SIMs'


def gateway_sim():
    return Sim.objects.filter(net__name='SMSBCAST').first()


class Cat(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Sms(models.Model):
    TYPE = [('s', 'Sent'), ('r', 'Received')]
    STATE = [('d', 'Delivered'), ('e', 'Expired'), ('f', 'Failed')]

    sim = models.ForeignKey(Sim, verbose_name="SIM", editable=False,
                            on_delete=models.CASCADE)
    no = models.CharField("Phone number", max_length=15)
    txt = models.TextField("Text")
    at = models.DateTimeField(default=datetime.now, editable=False)
    typ = models.CharField("Sent or Received", max_length=1, choices=TYPE,
        editable=False)
    state = models.CharField("Status", max_length=1, choices=STATE,
        blank=True, null=True, editable=False)
    cat = models.ForeignKey(Cat, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s: %s' % (self.no, self.txt)

    class Meta:
        ordering = ['-pk']


def get_cat(sms):
    fr, created = Cat.objects.get_or_create(name='Followup reply')
    txt = sms.txt.lower()
    same = Sms.objects.filter(txt__iexact=txt).exclude(cat=fr).first()
    if same: 
        return same.cat
    # replies to 2nd text should not be categorised, mark as followup replies
    if Sms.objects.filter(no=sms.no, typ='s').count() > 1:
        return fr
    return None


class Tpl(models.Model):
    name = models.CharField(max_length=40,
        verbose_name="Name (match recipient group)")
    tpl = models.TextField("Body")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'


class Log(models.Model):
    day = models.DateField()
    sim = models.ForeignKey(Sim, on_delete=models.CASCADE)
    sum = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.day, self.sim)

    class Meta:
        unique_together = ('day', 'sim')
        verbose_name = 'Daily total'
        verbose_name_plural = 'Stats'
