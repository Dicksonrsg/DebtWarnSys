from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddCompanyForm
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


def company_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        # Look Up Company
        user_company = Company.objects.get(id=primary_key)
        return render(request, 'company.html', {'user_company':user_company})
    else:
        messages.success(request, "There is no company to be displayed")
        return redirect('home')
    
    
def delete_company(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        to_be_deleted = Company.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Compnay deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete")
        return redirect('home')   
    
    
def add_company(request: HttpRequest):
    form = AddCompanyForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Success, Company added")
                return redirect('home')
        
        return render(request, 'add_company.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to add company")
        return redirect('home')
    
    
def update_company(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        current_company = Company.objects.get(id=primary_key)
        form = AddCompanyForm(request.POST or None, instance=current_company)
        if form.is_valid():
            form.save()
            messages.success(request, "Success, Company updated")
            return redirect('home')
        
        return render(request, 'update_company.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to update company")
        return redirect('home')