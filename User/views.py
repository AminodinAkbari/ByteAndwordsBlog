from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from User.forms import LoginForm , RegisterationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

class LoginAndRegisterView(View):
    template_name = 'login_and_register/login_index.html'

    def get(self ,request):
        login_form = LoginForm()
        registerForm = RegisterationForm()
        
        context = {
            "login_form": login_form,
            "register_form": registerForm
        }

        return render(request , self.template_name , context)
    
    def post(self , request):
        # Pass empty form if the input data have error

        context = {
            "login_form" : LoginForm(),
            "register_form" : RegisterationForm()
        }

        # Use hidden input "action" for determine data type (register or login)
        action = request.POST.get('action')

        if action == "register":
            register_form_includes_data = RegisterationForm(request.POST)
            if register_form_includes_data.is_valid():
                user = register_form_includes_data.save()
                login(request , user)
                # TODO: we can use f string for add user email in success message
                messages.success(request,f"User {user.username} registered successfuly !")
                return redirect('/')
        elif action == "login":
            requested_login_form = LoginForm(request.POST)
            if requested_login_form.is_valid():
                print("Valid")
                username = requested_login_form.cleaned_data.get("username")
                password = requested_login_form.cleaned_data.get("password")
                authentication = authenticate(username=username , password=password)
                if authentication is not None:
                    login(request , authentication)
                    # TODO: # TODO: we can use f string for add user email in info message
                    messages.info(request , "Welcome Back!")
                    return redirect('/')
                else:
                    messages.error(request , "Username or password is wrong")
            # Pass the form with errors back to the template
            context['login_form'] = requested_login_form
        else:
            #TODO: remove this printt statments or set error handler
            print("Not valid")
        return render(request , self.template_name , context)

def logout_view(request):
    logout(request)
    messages.error(request , "User logged out.")
    return redirect('/') # Redirect to the home page after logout