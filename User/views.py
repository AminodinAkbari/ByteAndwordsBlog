from django.shortcuts import render
from django.contrib.auth import authenticate, login
from User.forms import LoginForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views import View


# TODO:Use class base view (if you want) but it's so better if you separate the rendering funciton from login and registers processes
    # TODO: Also you should use biult in djanfo forms. 
# TODO: Are you sure the hidden input is a correct way ?
# Using captcha can be done with this : https://django-simple-captcha.readthedocs.io/en/latest/usage.html#installation. before that , we need use buit in Forms and use class base view

class LoginAndRegisterView(View):
    form_class = LoginForm()
    initial_form = {"loginForm" : form_class}
    # TODO: Change the template name it self. it's a bad name
    template_name = 'login_and_register/login_index.html'

    def get(self, request):
        return render(request , self.template_name , self.initial_form)
    
    def post(self , request , *args , **kwargs):
        print("post is started")

        login_form =self.form_class

        if login_form.is_valid():
            print("forms are valid")
            username = login_form.username
            password = login_form.password

            if 'confirmPassword' in request.POST:
                print("this request is signup")
                pass
            elif 'username' in request.POST and 'password' in request.POST:
                print("This request is login")
                # Authenticate the user with the provided username and password
                user = authenticate(username=username, password=password)
                print("user authenticated")
                
                if user is None:
                    print("User is none.")
                    # Display an error message if authentication fails (invalid password)
                    messages.error(request, "Invalid Password")
                    return redirect('/login_register/')
                else:
                    print("user vaild. we loging it in ... ")
                    # Log in the user and redirect to the home page upon successful login
                    login(request, user)
                    print("user logged in")
                    return redirect('/')
                
            else:
                print("Form is not valid")
                return redirect('/login_register')
        else:
            print("Form is not valid!")
            print(f"The form is : {login_form}")
        return render(request , self.template_name , self.initial_form)




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
