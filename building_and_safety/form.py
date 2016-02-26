from .models import FireAlarm
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets

'''
    To create a form from a fire alarm object
'''
class FireAlarmForm(forms.ModelForm):
    class Meta:
        model = FireAlarm
    def __init__(self, *args, **kwargs):
        super(FireAlarmForm, self).__init__(*args, **kwargs)
        self.fields['creation_date'].widget = widgets.AdminSplitDateTime()
        self.fields['activation_date'].widget = widgets.AdminSplitDateTime()
