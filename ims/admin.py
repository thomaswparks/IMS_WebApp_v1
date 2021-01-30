from django.contrib import admin
from django.contrib.auth.models import Group
from .models import EqAccount, EndItem
from ims.forms import item_update_form


# this class provides and admin function for equipment accounts in the administrator area of the site admins can add or remove accounts 
class EqAccountAdmin(admin.ModelAdmin):
    list_display        = ('eq_account_number','eq_account_custodian_id')
    list_filter         = ('eq_account_number','eq_account_custodian_id')
    search_fields       = ('eq_account_custodian_id',)
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()
    

class EndItemAdmin(admin.ModelAdmin):
    list_display = ('end_item_account_number','nomenclature','part_number','serial_number')
    list_filter = ('end_item_account_number','end_item_id','nomenclature','part_number','serial_number')
    search_fields = ('end_item_id','nomenclature','part_number','serial_number')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.site_header = "IMS Administration"
admin.site.register(EqAccount, EqAccountAdmin)
admin.site.register(EndItem, EndItemAdmin)