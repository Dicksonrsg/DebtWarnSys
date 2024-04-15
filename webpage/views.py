from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddressForm, CompanyForm, DebtorForm, DebtForm
from .models import Company, Address, Debtor, Debt

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
    

# Company    
def add_company(request: HttpRequest):
    company_form = CompanyForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if company_form.is_valid() and address_form.is_valid():
                address = address_form.save()
                company_form.instance.address = address
                company_form.save()
                messages.success(request, "Success, Company added")
                return redirect('home')
            else:
                messages.error(request, company_form.errors)
                
        return render(request, 'add_company.html', {'company_form':company_form, 'address_form': address_form})
    else:
        messages.success(request, "You must be logged in to add company")
        return redirect('home')


def company_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        # Look Up Company
        user_company = Company.objects.get(id=primary_key)
        return render(request, 'company.html', {'user_company':user_company})
    else:
        messages.success(request, "There is no company to be displayed")
        return redirect('home') 

    
def update_company(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        current_company = Company.objects.get(id=primary_key)
        current_address = Address.objects.get(id=current_company.address.id)
        company_form = CompanyForm(request.POST or None, instance=current_company)
        address_form = AddressForm(request.POST or None, instance=current_address)
        if company_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            company_form.instance.address = address
            company_form.save()
            messages.success(request, "Success, Company updated")
            return redirect('home')
        else:
            messages.error(request, company_form.errors)        
        
        return render(request, 'update_company.html', {'company_form':company_form, 'address_form': address_form})
    else:
        messages.success(request, "You must be logged in to update company")
        return redirect('home')


def delete_company(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        to_be_deleted = Company.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Company deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete")
        return redirect('home')  
 

# Debtor
def add_debtor(request: HttpRequest):
    debtor_form = DebtorForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if debtor_form.is_valid() and address_form.is_valid():
                address = address_form.save()
                debtor_form.instance.address = address
                debtor_form.save()
                messages.success(request, "Success, Debtor added")
                return redirect('home')
            else:
                messages.error(request, debtor_form.errors)
                
        return render(request, 'add_debtor.html', {'debtor_form':debtor_form, 'address_form': address_form})
    else:
        messages.success(request, "You must be logged in to add debtor")
        return redirect('home')
    

def debtor_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        # Look Up Debtor
        debtor = Debtor.objects.get(id=primary_key)
        return render(request, 'debtor.html', {'debtor':debtor})
    else:
        messages.success(request, "There is no debtor to be displayed")
        return redirect('home')


def all_debtors(request: HttpRequest):
    if request.user.is_authenticated:
        debtors = Debtor.objects.all()
        return render(request, 'all_debtors.html', {'debtors':debtors})
    else:
        messages.error(request, "There is no debtor to be displayed")
        return redirect('home')
    

def update_debtor(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        current_debtor = Debtor.objects.get(id=primary_key)
        current_address = Address.objects.get(id=current_debtor.address.id)
        debtor_form = DebtorForm(request.POST or None, instance=current_debtor)
        address_form = AddressForm(request.POST or None, instance=current_address)
        if debtor_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            debtor_form.instance.address = address
            debtor_form.save()
            messages.success(request, "Success, Debtor updated")
            return redirect('home')
        else:
            messages.error(request, debtor_form.errors)        
        
        return render(request, 'update_debtor.html', {'debtor_form':debtor_form, 'address_form': address_form})
    else:
        messages.success(request, "You must be logged in to update debtor")
        return redirect('home')
    
    
def delete_debtor(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        to_be_deleted = Debtor.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Debtor deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete")
        return redirect('home') 
    
    
# Debt
def add_debt(request: HttpRequest):
    debt_form = DebtForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                if debt_form.is_valid():
                    company = Company.objects.get(cnpj=debt_form.cnpj)
                    debtor = Debtor.objects.get(cpf=debt_form.cpf)
                    debt_form.instance.creditor = company
                    debt_form.instance.debtor = debtor
                    debt_form.save()
                    messages.success(request, "Success, Debt added")
                    return redirect('home')
                else:
                    messages.error(request, debt_form.errors)
            except Company.DoesNotExist:
                messages.error(request, "Company with CNPJ %s not found" % debt_form.cnpj) 
            except Debtor.DoesNotExist:
                messages.error(request, "Debtor with CPF %s not found" % debt_form.cpf)
            except Exception as e:
                messages.error(request, f"Unknown Exception ocurred: {str(e)}")
                
        return render(request, 'add_debt.html', {'debt_form':debt_form})
    else:
        messages.success(request, "You must be logged in to add debt")
        return redirect('home')
    

def debt_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        # Look Up Debt
        debt = Debt.objects.get(id=primary_key)
        return render(request, 'debt.html', {'debt':debt})
    else:
        messages.success(request, "There is no debt to be displayed")
        return redirect('home')
    
    
def all_debts_for_cnpj(request: HttpRequest):
    if request.user.is_authenticated:
        # Look Up Debts
        # Get Debts by company later on
        debts = Debt.objects.all()
        return render(request, 'debts_report.html', {'debts':debts})
    else:
        messages.success(request, "There is no debt to be displayed")
        return redirect('debts_report')
    

def update_debt(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        current_debt = Debt.objects.get(id=primary_key)
        debt_form = DebtForm(request.POST or None, instance=current_debt)
        if debt_form.is_valid():
            debt_form.save()
            messages.success(request, "Success, Debt updated")
            return redirect('home')
        else:
            messages.error(request, debt_form.errors)        
        
        return render(request, 'update_debt.html', {'debt_form':debt_form})
    else:
        messages.success(request, "You must be logged in to update debt")
        return redirect('home')
    
    
def delete_debt(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        to_be_deleted = Debtor.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Debt deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete")
        return redirect('home') 
    