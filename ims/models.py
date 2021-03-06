from django.db import models
from django.conf import settings
from account.models import Account  # needed as a foregin key


# this class is for each equipment account assigned to a user
class EqAccount(models.Model):
    eq_account_number = models.AutoField(primary_key=True)
    eq_account_custodian_id = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE)

    def __int__(self):
        return self.eq_account_number


# this class is for each end item. these are added to the equipment accounts
class EndItem(models.Model):
    SERVICEABLE = 'SR'
    NEEDS_REPAIR = 'R'
    UNREPAIRABLE = 'NR'
    STATUS_CHOICES = [
        (SERVICEABLE, 'Serviceable'),
        (NEEDS_REPAIR, 'Needs Repair'),
        (UNREPAIRABLE, 'Unrepairable'),
    ]
    end_item_id = models.AutoField(primary_key=True)
    nomenclature = models.CharField(max_length=45)
    part_number = models.CharField(max_length=45)
    serial_number = models.CharField(max_length=45)
    end_item_account_number = models.ForeignKey(EqAccount, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=45, choices=STATUS_CHOICES, default=SERVICEABLE)

    def __int__(self):
        return self.end_item_id


# SubItems are equipment assets that can be listed under an end item.
class SubItem(models.Model):
    sub_item_id = models.AutoField(primary_key=True)
    sub_item_end_item = models.ForeignKey(EndItem, on_delete=models.CASCADE, null=True, blank=True)
    sub_serial_number = models.CharField(max_length=45, null=True, blank=True)
    sub_part_number = models.CharField(max_length=45)
    sub_nomenclature = models.CharField(max_length=45)
    quantity = models.IntegerField(null=True, blank=True)

    def __int__(self):
        return self.sub_item_end_item_id


# this class will be used to offer users to keep official reords for their accounts
class Note(models.Model):
    record_id = models.AutoField(primary_key=True)
    notes_account_number = models.ForeignKey(EqAccount, on_delete=models.DO_NOTHING)
    notes_custodian_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    notes_end_item_id = models.ForeignKey(EndItem, on_delete=models.DO_NOTHING)
    notes_sub_item_id = models.ForeignKey(SubItem, on_delete=models.DO_NOTHING)
    entry = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.record_id