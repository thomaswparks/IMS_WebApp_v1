from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .forms import new_item_form, item_update_form
from .models import EqAccount, EndItem


# this view will allow users to add new items to their inventory
@login_required(login_url='login')
def newItem(request):
    form = new_item_form(request.POST or None)
    current_user = request.user
    user_id = current_user.pk
    eq_acct = EqAccount.objects.filter(eq_account_custodian_id=user_id)
    end_items = EndItem.objects.all()
    if form.is_valid():
        instance = form.save(commit=False)
        instance.eq_account_number = request.POST.get('end_item_account_number')
        instance.save()
        form = new_item_form()
    context = {'form': form, 'eq_acct': eq_acct, 'user_id': user_id, 'current_user': current_user,
               'end_items': end_items}
    return render(request, 'ims/new_end_item.html', context)


# this view will update any changes made to an End_Item
@login_required(login_url='login')
def updateItem(request):
    form = item_update_form(request.POST or None)
    current_user = request.user
    user_id = current_user.pk
    eq_acct = EqAccount.objects.filter(eq_account_custodian_id=user_id)
    end_items = EndItem.objects.all()
    form = item_update_form()
    messages.success(request, f'Success!')
    context = {'form': form, 'eq_acct': eq_acct, 'user_id': user_id, 'current_user': current_user,
               'end_items': end_items}
    return render(request, 'ims/item_update.html', context)


# this view grabs all End_Item objects from all of the current user's equipment accounts and passes it to home.html
@login_required(login_url='login')
def home(request):
    current_user = request.user
    user_id = current_user.pk
    eq_acct = EqAccount.objects.filter(eq_account_custodian_id=user_id)
    end_items = EndItem.objects.all()

    print(eq_acct)
    context = {'current_user': current_user, 'user_id': user_id, 'eq_acct': eq_acct, 'end_items': end_items}
    return render(request, 'ims/home.html', context)
