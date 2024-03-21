from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Company

def home(request: HttpRequest):
    
    companies = Company.objects.all()
    

    if request.method == 'POST':
        email_address = request.POST['email_address']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=email_address, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are an active user")
            return redirect('home')
        else:
            messages.success(request, "You are not an active user, contact us")
            return redirect('home')
    else:
        return render(request, 'home.html', {'companies':companies})


def login_user(request: HttpRequest):
    pass


def logout_user(request: HttpRequest):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect('home')


def register_user(request: HttpRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request=request, user=user)
            messages.success(request, "You have registered! Congrats")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})
