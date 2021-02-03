from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, reset_queries
from .forms import new_item_form, item_update_form, new_sub_item_form
from .models import EqAccount, EndItem, SubItem


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
        context = { 
            'form': form, 
            'current_user': current_user, 
            'user_id': user_id, 
            'eq_acct': eq_acct, 
            'end_items': end_items, 
            'title': title,
        }
        form.instance.end_item_account_number = EqAccount.objects.filter(eq_account_custodian_id = request.user.pk).first()
        form.save()
        messages.success(request, f'Your equipment item has been added!')
        
    
    form = new_item_form()
    context = {
        'form': form, 
        'current_user': current_user,
        'user_id': user_id,
        'eq_acct': eq_acct,
        'end_items': end_items,
        'title': title,
    }
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
    sub_items = item.subitem_set.all()
    u_form = item_update_form(instance=item)
    
    if request.method == 'POST':
        u_form = item_update_form(request.POST, instance=item)
        
        if u_form.is_valid:
            u_form.save()
    context = {
            'sub_items': sub_items,
            'item': item,
            'u_form': u_form,
            'title': title,
            'current_user': current_user,
            'user_id': user_id,
            'eq_acct': eq_acct,
            'end_items': end_items
        }
    return render(request, 'ims/item_update.html', context)


@login_required
def delete_item(request, pk):
    title = "Update Item"
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    context = {}
    item = EndItem.objects.get(end_item_id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {
            'item': item,
            'title': title,
            'current_user': current_user,
            'user_id': user_id,
            'eq_acct': eq_acct,
            'end_items': end_items
        }
    return render(request, 'ims/delete.html', context)


@login_required
def new_sub(request, pk):
    title = "Add Sub Item: " + str(pk)
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    form = new_sub_item_form()
    if request.method == 'POST':
        if form.is_valid:
            form = new_sub_item_form(request.POST)
            context = { 
                'form': form, 
                'current_user': current_user, 
                'user_id': user_id, 
                'eq_acct': eq_acct, 
                'end_items': end_items, 
                'title': title,
            }
            form.instance.sub_item_end_item_id = EndItem.objects.filter(end_item_id=pk).first()
            form.save()
            messages.success(request, f'Your equipment item has been added!')
    context = {
        'form': form, 
        'current_user': current_user,
        'user_id': user_id,
        'eq_acct': eq_acct,
        'end_items': end_items,
        'title': title,
    }
    return render(request, 'ims/sub-item.html', context)

# this view grabs all End_Item objects from all of the current user's equipment accounts and passes it to home.html
@login_required(login_url='login')
def home(request):
    current_user = request.user
    user_id = current_user.pk
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    title = "Home"
    total_items = 0

    for item in end_items:
        total_items += 1

    print('ims.views.home: ', eq_acct)
    context = {'total_items': total_items, 'title': title,'current_user': current_user, 'user_id': user_id, 'eq_acct': eq_acct, 'end_items': end_items}
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

def get_sub_items(end_item_id):
    sub_items = SubItem.objects.filter(sub_item_end_item_id=end_item_id)

    return sub_items