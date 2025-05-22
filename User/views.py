from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# TODO:Use class base view (if you want) but it's so better if you separate the rendering funciton from login and registers processes
    # TODO: Also you should use biult in djanfo forms. 
# TODO: Are you sure the hidden input is a correct way ?
# Using captcha can be done with this : https://django-simple-captcha.readthedocs.io/en/latest/usage.html#installation. before that , we need use buit in Forms and use class base view

def login_and_register(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST" and request.POST.get('hidden') != 'signup':

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/login_and_register/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            return redirect('/login_and_register/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            username = user.username
            return redirect('/login_and_register/')
        
    elif request.method == "POST" and request.POST.get('hidden') == 'signup':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('/login_and_register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            password=password,
            username=username
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('/login_and_register/')
    
    return render(request, 'login_and_register/login_index.html')
