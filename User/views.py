from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

def login_and_register(request):

    username = None

    # Check if the HTTP request method is POST (form submission)
    if request.method == "POST" and request.POST.get('hidden') != 'signup':
        print('POST request received')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('Username:', username)
        print('Password:', password)
        
        # Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            # Display an error message if the username does not exist
            messages.error(request, 'Invalid Username')
            print('Invalid Username')
            return redirect('/login_and_register/')
        
        # Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password")
            print('Invalid Password')
            return redirect('/login_and_register/')
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            username = user.username
            print('Login successful')
            return redirect('/login_and_register/')
        
    elif request.method == "POST" and request.POST.get('hidden') == 'signup':
        print('SIGNUP request received')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print('Username:', username)
        print('email:', email)
        print('Password:', password)
        print('Confirm password:', confirm_password)
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            print('Username already taken')
            return redirect('/login_and_register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            password=password,
            username=username
        )
        print('User created successfully')
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        print('Account created successfully')
        return redirect('/login_and_register/')
        
    # TODO: context not work BUT LOGIN WORKS
    context = {
        'username': username,
    }
    
    return render(request, 'login_and_register/login_index.html' , context)
