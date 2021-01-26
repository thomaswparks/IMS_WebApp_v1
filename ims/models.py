from django.db import models
from account.models import Account  # needed as a foregin key


# this class is for each equipment account assigned to a user
class EqAccount(models.Model):
    eq_account_number = models.AutoField(primary_key=True)
    eq_account_custodian_id = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __int__(self):
        return self.eq_account_number

    def show_eqCust(self):
        return self.eq_account_custodian_id


USERNAME_FIELD = 'eq_account_number'
REQUIRED_FIELDS = ['eq_account_custodian_id', ]


# this class is for each end item. these are added to the equipment accounts
class EndItem(models.Model):
    end_item_id = models.AutoField(primary_key=True)
    nomenclature = models.CharField(max_length=45)
    part_number = models.CharField(max_length=45)
    serial_number = models.CharField(max_length=45)
    end_item_account_number = models.ForeignKey(EqAccount, on_delete=models.CASCADE, null=True)
    status = models.IntegerField


# SubItems are equipment assets that can be listed under an end item.
class SubItem(models.Model):
    sub_item_id = models.AutoField(primary_key=True)
    sub_item_end_item_id = models.ForeignKey(EndItem, on_delete=models.CASCADE)
    sub_serial_number = models.CharField(max_length=45)
    sub_part_number = models.CharField(max_length=45)
    sub_nomenclature = models.CharField(max_length=45)
    quantity = models.IntegerField
    sub_status = models.IntegerField


# this class will be used to offer users to keep official reords for their accounts
class Note(models.Model):
    record_id = models.AutoField(primary_key=True)
    notes_account_number = models.ForeignKey(EqAccount, on_delete=models.DO_NOTHING)
    notes_custodian_id = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    notes_end_item_id = models.ForeignKey(EndItem, on_delete=models.DO_NOTHING)
    notes_sub_item_id = models.ForeignKey(SubItem, on_delete=models.DO_NOTHING)
    entry = models.TextField
    created_at = models.DateTimeField(auto_now_add=True)
