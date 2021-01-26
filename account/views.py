from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.contrib import messages
from .forms import RegistrationForm, user_update_form


# this view is for new users to register for an account
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get('pasword1')
            username = form.cleaned_data.get("username")
            account = authenticate(email=email, password=raw_password)
            #login(request, account)
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


def profile(request):
    u_form = user_update_form()

    context = {
        'u_form': u_form,
    }

    return render(request, 'account/profile.html', context)