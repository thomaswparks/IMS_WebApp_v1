from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, user_update_form, profile_update_form


# this view is for new users to register for an account
def registration_view(request):
    title = "Register"
    context = {'title': title}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get('pasword1')
            username = form.cleaned_data.get("username")
            account = authenticate(email=email, password=raw_password)
            messages.success(request, f'Account created for {username}! The admin will approve your account shortly.')
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


# this view directs all authenticated users to the IMS home page. Non-auth'd users will be redirected to the login page.
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'ims/home.html')

@login_required
def profile(request):
    title = "profile"
    if request.method == 'POST':
        u_form = user_update_form(request.POST, instance=request.user)
        p_form = profile_update_form(request.POST, 
                                     request.FILES, 
                                     instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            current_user = request.user
            user_id = current_user.pk
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            context = {'current_user': current_user,'user_id': user_id, 'title': title}
            u_form = user_update_form(request.POST, instance=request.user)
            p_form = profile_update_form(request.POST, 
                                        request.FILES, 
                                        instance=request.user.profile)
            return render(request, 'profile', context)
    else:
        u_form = user_update_form(instance=request.user)
        p_form = profile_update_form(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'account/profile.html', context)
