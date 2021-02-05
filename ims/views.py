from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, reset_queries
from .forms import new_item_form, item_update_form, new_sub_item_form, sub_item_update_form
from .models import EqAccount, EndItem, SubItem


@login_required(login_url='login')
def newItem(request):
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    title = "New Item"
    form = new_item_form()
    context = {
        'form': form, 
        'current_user': current_user,
        'user_id': user_id,
        'eq_acct': eq_acct,
        'end_items': end_items,
        'title': title,
    }
    if request.method == 'POST' and eq_acct:
        form = new_item_form(request.POST)
        form.instance.end_item_account_number = EqAccount.objects.filter(eq_account_custodian_id = request.user.pk).first()
        form.save()
        messages.success(request, f'Your equipment item has been added!')
        form = new_item_form()
        # return render(request, 'ims/new_end_item.html', context)
    elif eq_acct == None:
        messages.warning(request, f'You cannot add equipment because you do not have an account. Please contact you administrator for more information.')
        return redirect('home')
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
    item_acct = EqAccount.objects.values_list('eq_account_number', flat=True).filter(eq_account_number=item.end_item_account_number).first()
    sub_items = item.subitem_set.all()
    u_form = item_update_form(instance=item)
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
    if eq_acct != item_acct:
        messages.warning(request, f'You do not have access to that item!')
        return redirect('home')
    else:    
        if request.method == 'POST':
            u_form = item_update_form(request.POST, instance=item)
            
            if u_form.is_valid:
                u_form.save()
       
    return render(request, 'ims/item_update.html', context)

# this view will allow users to delete end items within their account
@login_required
def delete_item(request, pk):
    title = "Delete Item"
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    item = EndItem.objects.get(end_item_id=pk)
    item_acct = EqAccount.objects.values_list('eq_account_number', flat=True).filter(eq_account_number=item.end_item_account_number).first()
    context = {
            'item': item,
            'title': title,
            'current_user': current_user,
            'user_id': user_id,
            'eq_acct': eq_acct,
            'end_items': end_items
        }
    if eq_acct != item_acct:
        messages.warning(request, f'You do not have access to that item!')
        return redirect('home')
    else:
        if request.method == 'POST':
            item.delete()
            return redirect('home')
    
    return render(request, 'ims/delete.html', context)

# this view allows users to add new sub items
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
            form = new_sub_item_form()
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


    context = {'total_items': total_items, 
               'title': title,
               'current_user': current_user, 
               'user_id': user_id, 
               'eq_acct': eq_acct, 
               'end_items': end_items
        }
    return render(request, 'ims/home.html', context)

# this view allows users to update sub items
@login_required(login_url='login')
def update_sub_item(request, pk):
    title = "Update Sub Item"
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    context = {}
    item = SubItem.objects.get(sub_item_id=pk)
    u_form = sub_item_update_form(instance=item)
    end_item = item.sub_item_end_item_id
    end_item_obj = EndItem.objects.get(pk=end_item)
    context = {
                'end_item': end_item,
                'item': item,
                'u_form': u_form,
                'title': title,
                'current_user': current_user,
                'user_id': user_id,
                'eq_acct': eq_acct,
                'end_items': end_items,
            }
    item_acct = EqAccount.objects.values_list('eq_account_number', flat=True).filter(eq_account_number=end_item_obj.end_item_account_number).first()
    if eq_acct != item_acct:
        messages.warning(request, f'You do not have access to that item!')
        return redirect('home')
    else:
        if request.method == 'POST':
            u_form = sub_item_update_form(request.POST, instance=item)
            
            if u_form.is_valid:
                u_form.save()
                return redirect('updateItem',end_item)
        
    return render(request, 'ims/sub_item_update.html', context)

# this view allows users to remove sub items
@login_required
def delete_sub_item(request, pk):
    title = "Delete Sub Item"
    current_user = request.user
    user_id = get_user_id(request)
    eq_acct = get_eq_acct(user_id)
    end_items = get_end_items(eq_acct)
    item = SubItem.objects.get(sub_item_id=pk)
    end_item = item.sub_item_end_item_id
    end_item_obj = EndItem.objects.get(pk=end_item)
    context = {
                'end_item': end_item,
                'item': item,
                'title': title,
                'current_user': current_user,
                'user_id': user_id,
                'eq_acct': eq_acct,
                'end_items': end_items
            }
    item_acct = EqAccount.objects.values_list('eq_account_number', flat=True).filter(eq_account_number=end_item_obj.end_item_account_number).first()
    if eq_acct != item_acct:
        messages.warning(request, f'You do not have access to that item!')
        return redirect('home')
    else:
        if request.method == 'POST':
            item.delete()
            return redirect('updateItem',end_item)
        
    return render(request, 'ims/delete_sub.html', context)

# this is being used as a function to retrieve user ids
def get_user_id(request):
    current_user = request.user
    user_id = current_user.pk
    return user_id

# this is being used as a funciton to reteive the user's equipment account
def get_eq_acct(user_id):
    eq_acct = EqAccount.objects.values_list('eq_account_number', flat=True).filter(eq_account_custodian_id=user_id).first()
    return eq_acct

# this function provides a list of the current user's equipment
def get_end_items(eq_acct):
    end_items = EndItem.objects.filter(end_item_account_number=eq_acct)
    return end_items

# this function retreives a list of sub items for a given end item
def get_sub_items(end_item_id):
    sub_items = SubItem.objects.filter(sub_item_end_item_id=end_item_id)
    return sub_items
