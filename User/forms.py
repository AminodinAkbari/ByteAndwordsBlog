from django.forms import ModelForm , TextInput , PasswordInput
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder" : "username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder" : "password"})
    )