from django import forms
from django.forms import ModelForm
from . import models


# this form is for a feature that may be added in the future. This provides statuses of equipment assets.
class Form_SnapShot(forms.Form):
    Status = forms.ChoiceField(choices=['FMC', 'PMC', 'NMC'])

    class Meta:
        fields = "status"


# this form is to update an end item record
class item_update_form(forms.ModelForm):
    end_item_id = forms.IntegerField()
    nomenclature = forms.CharField(max_length=45)
    part_number = forms.CharField(max_length=45)
    serial_number = forms.CharField(max_length=45)
    end_item_account_number = forms.IntegerField()
    status = forms.IntegerField

    class Meta:
        model = models.EndItem
        fields = ['end_item_id', 'nomenclature', 'part_number', 'serial_number', 'end_item_account_number']


class new_item_form(ModelForm):
    class Meta:
        model = models.EndItem
        fields = ("end_item_id", "nomenclature", "part_number", "serial_number", "end_item_account_number")

