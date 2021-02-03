from django import forms
from django.db.models import fields
from django.forms import ModelForm
from . import models



# this form is for a feature that may be added in the future. This provides statuses of equipment assets.
class Form_SnapShot(forms.Form):
    Status = forms.ChoiceField(choices=['FMC', 'PMC', 'NMC'])

    class Meta:
        fields = "status"


# this form is to update an end item record
class item_update_form(forms.ModelForm):
    
    class Meta:
        model = models.EndItem
        exclude = ['end_item_account_number',]


class new_item_form(ModelForm):
    class Meta:
        model = models.EndItem
        exclude = ('end_item_account_number',)

class new_sub_item_form(ModelForm):
    class Meta:
        model = models.SubItem
        exclude = ('sub_item_end_item',)
