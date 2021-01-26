from django.contrib import admin
from django.contrib.auth.models import Group
from .models import EqAccount

# this class provides and admin function for equipment accounts in the administrator area of the site admins can add or remove accounts 
class EqAccountAdmin(admin.ModelAdmin):
    list_display        = ('eq_account_number', 'eq_account_custodian_id',)
    list_filter         = ('eq_account_number','eq_account_custodian_id')
    search_fields       = ('eq_account_number','eq_account_custodian_id')

    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()

admin.site.register(EqAccount, EqAccountAdmin)
admin.site.site_header  = "IMS Administration"
