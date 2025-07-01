from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder" : "username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder" : "password"})
    )

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder" : "password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder" : "confirm password"})
    )

    class Meta:
        model = User
        fields = ('username' , 'email')
        widgets = {
            'username' : forms.TextInput(attrs={
                'placeholder' : 'username (We know you with this username as a person)'
            }),
            'email' : forms.EmailInput(attrs={
                'placeholder' : 'email'
            })
        }

        def clean(self):
            print("clean run.")
            # First, get the cleaned data from the parent class
            cleaned_data = super().clean()

            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password and confirm_password and password != confirm_password:
                print("here we are")
                raise forms.ValidationError("Passwords are not match")
            print("It's cleaned")
            print(password)
            print(confirm_password)
            return cleaned_data

        def save(self , commit=True):
            # Get writed password in form
            password = self.cleaned_data.get("password")
            # Save new user objecct in db
            user = super().save(commit=False)
            user.set_password(password)
            if commit:
                user.save()
            return user
