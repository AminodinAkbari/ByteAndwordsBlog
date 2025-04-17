from django.shortcuts import render

# Create your views here.

def login_and_register(request):
    return render(request, 'login_and_register/login_index.html')
