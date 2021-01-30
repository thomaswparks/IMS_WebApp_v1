from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Profile

# this is a custom registration form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ("email","username","first_name","last_name","password1","password2")

class user_update_form(forms.ModelForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ['email','username']

class profile_update_form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']