from django import forms
from sms.models import *

class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        exclude = []

class TplForm(forms.ModelForm):
    class Meta:
        model = Tpl
        exclude = []

class SimForm(forms.ModelForm):
    class Meta:
        model = Sim
        exclude = []

class NetForm(forms.ModelForm):
    class Meta:
        model = Net
        exclude = []

class SendForm(forms.Form):
    no  = forms.CharField(label='Phone', widget=forms.Textarea(attrs={'cols':50, 'rows':1,}))
    txt = forms.CharField(label='Text',  widget=forms.Textarea(attrs={'cols':50, 'rows':3,}))