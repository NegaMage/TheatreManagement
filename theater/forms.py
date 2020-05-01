from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type = 'date'

class MakePurchase(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['time','seats','date']
        widgets = {
            'date' : DateInput(),
        }