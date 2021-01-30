from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .forms import new_item_form, item_update_form
from .models import EqAccount, EndItem


@login_required(login_url='login')
def newItem(request):
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    title = "New Item"
    context = {}
    print('Eq Acct: ', eq_acct)
    if request.method == 'POST':
        form = new_item_form(request.POST)
        # form.fields['end_item_account_number'].initial = eq_acct
        context = {'form': form, 'current_user': current_user,
                'user_id': user_id,
                'eq_acct': eq_acct,
                'end_items': end_items,
                'title': title,
        }
        form.instance.end_item_account_number = EqAccount.objects.filter(eq_account_custodian_id = request.user.pk).first()
        form.save()
        messages.success(request, f'Your equipment item has been added!')
        
    else:
        form = new_item_form()
        # form.fields['end_item_account_number'].initial = eq_acct
        context = {'form': form, 'current_user': current_user,
                'user_id': user_id,
                'eq_acct': eq_acct,
                'end_items': end_items,
                'title': title,
        }

    # print('Printing POST: ', request.POST)
    return render(request, 'ims/new_end_item.html', context)


# this view will update any changes made to an End_Item
@login_required(login_url='login')
def updateItem(request, pk):
    title = "Update Item"
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    context = {}
    item = EndItem.objects.get(end_item_id=pk)


    u_form = item_update_form()
    if request.POST:
        u_form = item_update_form(request.POST)
        
    context = {
            'item': item,
            'u_form': u_form,
            'title': title,
            'current_user': current_user,
            'user_id': user_id,
            'eq_acct': eq_acct,
            'end_items': end_items
        }
    return render(request, 'ims/item_update.html', context)
        


# this view grabs all End_Item objects from all of the current user's equipment accounts and passes it to home.html
@login_required(login_url='login')
def home(request):
    current_user = request.user
    user_id = current_user.pk
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    title = "Home"

    print(eq_acct)
    context = {'current_user': current_user, 'user_id': user_id, 'eq_acct': eq_acct, 'end_items': end_items}
    return render(request, 'ims/home.html', context)

def get_user_id(request):
    current_user = request.user
    user_id = current_user.pk

    return user_id

def get_eq_acct(user_id):
    eq_acct = EqAccount.objects.values_list('eq_account_number', flat=True).filter(eq_account_custodian_id=user_id).first()

  
    return eq_acct

def get_end_items(eq_acct):
    end_items = EndItem.objects.filter(end_item_account_number=eq_acct)

    return end_items