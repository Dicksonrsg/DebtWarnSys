from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AddressForm, CompanyForm, DebtorForm, DebtForm, CompanyUserForm
from .models import Company, Address, Debtor, Debt, CompanyUser
from .helper.auth import assign_group
from .helper.fetcher import get_debtor, get_auth_user



@login_required(login_url="login")
def home(request: WSGIRequest):
    # Get only companies from a specific user
        companies = Company.objects.all()
        if companies:
            return render(request, 'home.html', {'companies':companies})
        else:
            return render(request, 'home.html', {'companies':companies})


def login_user(request: WSGIRequest):
    if request.method == 'POST':
        user_name = request.POST['email_address']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are an active user")
            return redirect('home')
        else:
            messages.error(request, "You are not an active user, contact us")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request: WSGIRequest):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect('home')


def register_user(request: WSGIRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        try:
            # Validates if User is Debtor
            is_debtor = request.POST.get('isDebtor')
            debtor_cpf = request.POST.get('debtorCPF')

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                form.save()
                
                # Authenticate and login
                user = authenticate(username=username, password=password)
                login(request=request, user=user)
                messages.success(request, "You have registered! Congrats")
                
                if is_debtor and debtor_cpf:
                    debtor_cpf = debtor_cpf.replace('.', '').replace('-', '')
                    debtor_object = get_debtor(cpf=debtor_cpf)
                    if debtor_object:
                        return redirect('update_debtor', debtor_object.id) 
                    else:
                        return redirect('add_debtor')
                else:
                    return redirect('add_company_user')
            else:
                messages.error(request, form.errors)

        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})
    
    

# Company
@login_required(login_url="login")    
def add_company(request: WSGIRequest):
    company_form = CompanyForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.method == "POST":
        try:
            if company_form.is_valid() and address_form.is_valid():
                address = address_form.save()
                company_form.instance.address = address
                company_form.save()
                messages.success(request, "Success, Company added")
                return redirect('home')
            else:
                messages.error(request, company_form.errors)
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')                
            
    return render(request, 'add_company.html', {'company_form':company_form, 'address_form': address_form})


@login_required(login_url="login")
def company_register(request: WSGIRequest, primary_key: int):
    try:
    # Look Up Company
        user_company = Company.objects.get(id=primary_key)
        return render(request, 'company.html', {'user_company':user_company})
    except Company.DoesNotExist:
        messages.error(request, "Companies not found")
    except Exception as e:
        messages.error(request, f"Unknown Exception ocurred: {str(e)}")
        return render(request, 'error.html')


@login_required(login_url="login")    
def update_company(request: WSGIRequest, primary_key: int):
    try:
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
    
    except Company.DoesNotExist as e:
        messages.error(request, "Company with Id %s not found" % primary_key)
    except Address.DoesNotExist as e:
        messages.error(request, "Address with Id %s not found" % current_company.address.id)
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')         


# TODO: a company user can't delete it
@login_required(login_url="login")
def delete_company(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = Company.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Company deleted successfully")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"Unknown Exception ocurred: {str(e)}")
        return render(request, 'error.html') 

 

# Debtor
# TODO: Design a different home for debtors 
@login_required(login_url="login")
def add_debtor(request: WSGIRequest):
    debtor_form = DebtorForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.method == "POST":
        try:
            if debtor_form.is_valid() and address_form.is_valid():
                current_user = get_auth_user(id=request.user.id)
                address = address_form.save()
                debtor_form.instance.address = address
                debtor_form.instance.user_auth = current_user
                debtor_form.save()
                assign_group(user_name=request.user.username, role='Debtor')
                messages.success(request, "Success, Debtor added")
                return redirect('home')
            else:
                messages.error(request, debtor_form.errors)
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html') 
                        
    return render(request, 'add_debtor.html', {'debtor_form':debtor_form, 'address_form': address_form})

    
@login_required(login_url="login")
def debtor_register(request: WSGIRequest, primary_key: int):
    try:
        # Look Up Debtor
        debtor = Debtor.objects.get(id=primary_key)
        return render(request, 'debtor.html', {'debtor':debtor})
    except Debtor.DoesNotExist:
        messages.error(request, f"Debtor was not found for Id: {primary_key}")
        return redirect('all_debtors')
    except Exception as e:
        messages.error(request, f"Unknown Exception ocurred: {str(e)}")
        return render(request, 'error.html')


@login_required(login_url="login")
def all_debtors(request: WSGIRequest):
    try:
        debtors = Debtor.objects.all()
        return render(request, 'all_debtors.html', {'debtors':debtors})
    except Debtor.DoesNotExist:
        messages.error(request, f"There are no Debtors to be displayed")
        return render(request, 'all_debtors.html', {'debtors':None})
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')

    
@login_required(login_url="login")
def update_debtor(request: WSGIRequest, primary_key: int):
    try:
        current_debtor = Debtor.objects.get(id=primary_key)
        current_address = Address.objects.get(id=current_debtor.address.id)
        current_user = get_auth_user(id=request.user.id)
        debtor_form = DebtorForm(request.POST or None, instance=current_debtor)
        address_form = AddressForm(request.POST or None, instance=current_address)
        if debtor_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            debtor_form.instance.address = address
            debtor_form.instance.user_auth = current_user
            debtor_form.save()
            messages.success(request, "Success, Debtor updated")
            return redirect('home')
        else:
            messages.error(request, debtor_form.errors)        
        
        return render(request, 'update_debtor.html', {'debtor_form':debtor_form, 'address_form': address_form})
    except Debtor.DoesNotExist:
        messages.error(request, "Debtor with Id %s not found" % primary_key)
    except Address.DoesNotExist:
        messages.error(request, "Address with Id %s not found" % current_debtor.address.id)
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')
    
    
# TODO: Debtor can't delete themselves
@login_required(login_url="login")
def delete_debtor(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = Debtor.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Debtor deleted successfully")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')
 
    
# Debt
@login_required(login_url="login")
def add_debt(request: WSGIRequest):
    debt_form = DebtForm(request.POST or None)
    if request.method == "POST":
        try:
            if debt_form.is_valid():
                company = Company.objects.get(cnpj=debt_form.cleaned_data['cnpj'])
                debtor = Debtor.objects.get(cpf=debt_form.cleaned_data['cpf'])
                debt_form.instance.creditor = company
                debt_form.instance.debtor = debtor
                to_save_df = debt_form.save(commit=False)
                to_save_df.created_by = request.user.email
                to_save_df.save()
                messages.success(request, "Success, Debt added")
                return redirect('home')
            else:
                messages.error(request, debt_form.errors)
        except Company.DoesNotExist:
            messages.error(request, "Company with CNPJ %s not found" % debt_form.cleaned_data['cnpj']) 
        except Debtor.DoesNotExist:
            messages.error(request, "Debtor with CPF %s not found" % debt_form.cleaned_data['cpf'])
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
            
    return render(request, 'add_debt.html', {'debt_form':debt_form})

    

@login_required(login_url="login")
def debt_register(request: WSGIRequest, primary_key: int):
    try:
        # Look Up Debt
        debt = Debt.objects.get(id=primary_key)
        return render(request, 'debt.html', {'debt':debt})
    except Debt.DoesNotExist:
        messages.error(request, "Debt with Id %s not found" % primary_key)
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')

    
# Look Up Debts
# TODO: Get Debts by company
@login_required(login_url="login")   
def all_debts_for_cnpj(request: WSGIRequest):
    try:
        # debts = Debt.objects.filter(creditor=user.company)
        debts = Debt.objects.all()
        return render(request, 'debts_report.html', {'debts':debts})
    except Debt.DoesNotExist:
        messages.error(request, "Debts not found")
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')
    

@login_required(login_url="login")     
def all_debts_for_cpf(request: WSGIRequest, debtor_cpf: str):
    try:
        debts = Debt.objects.filter(cpf=debtor_cpf)
        return render(request, 'my_debts.html', {'debts': debts})
    except Debt.DoesNotExist:
        messages.error(request, "Debts not found")
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')


@login_required(login_url="login")
def update_debt(request: WSGIRequest, primary_key: int):
    try:
        current_debt = Debt.objects.get(id=primary_key)
        debt_form = DebtForm(request.POST or None, instance=current_debt)
        if debt_form.is_valid():
            debt_form.save()
            messages.success(request, "Success, Debt updated")
            return redirect('home')
        else:
            messages.error(request, debt_form.errors)        
        
        return render(request, 'update_debt.html', {'debt_form':debt_form})
    except Debt.DoesNotExist:
        messages.error(request, "Debt with Id %s not found" % primary_key)
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')        

    
# TODO: Only admin can delete Debts
@login_required(login_url="login") 
def delete_debt(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = Debt.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Debt deleted successfully")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html') 


# CompanyUser
@login_required(login_url="login")
def add_company_user(request: WSGIRequest):
    company_user_form = CompanyUserForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.method == "POST":
        try:
            if company_user_form.is_valid() and address_form.is_valid():
                address = address_form.save()
                company_user_form.instance.address = address
                company = Company.objects.get(cnpj=company_user_form.cleaned_data['cnpj'])
                company_user_form.instance.creditor = company
                user_auth = get_auth_user(id=request.user.id)
                company_user_form.instance.user_auth = user_auth
                company_user_form.save()
                assign_group(user_name=request.user.username, role=company_user_form.cleaned_data['role'])
                messages.success(request, "Success, Company User added")
                return redirect('home')
            else:
                messages.error(request, company_user_form.errors or address_form.errors)
        except Company.DoesNotExist:
            messages.error(request, "Company with CNPJ %s not found" % company_user_form.cleaned_data['cnpj'])
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
            
    return render(request, 'add_company_user.html', {'company_user_form':company_user_form, 'address_form': address_form})


# TODO: Return only CompanyUsers if logged user has permission    
@login_required(login_url="login") 
def company_user_register(request: WSGIRequest, primary_key: int):
        # Look Up CompanyUSer        
    try:
        company_user = CompanyUser.objects.get(id=primary_key)
        return render(request, 'company_user.html', {'company_user':company_user})
    except CompanyUser.DoesNotExist:
        messages.error(request, "Company User with Id %s not found" % primary_key)
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')


# Look Up Company Users
# TODO: Bring only Company Users from a specific CNPJ
@login_required(login_url="login")    
def all_company_users(request: WSGIRequest):
    try:
        company_users = CompanyUser.objects.all()
        return render(request, 'all_company_users.html', {'company_users': company_users})
    except CompanyUser.DoesNotExist:
        messages.error(request, "Company Users not found")
    except Exception as e:
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, 'error.html')

    
@login_required(login_url="login")
def update_company_user(request: WSGIRequest, primary_key: int):
    try:
        current_company_user = CompanyUser.objects.get(id=primary_key)
        company_user_form = CompanyUserForm(request.POST or None, instance=current_company_user)
        if company_user_form.is_valid():
            company_user_form.save()
            messages.success(request, "Success, Company User updated")
            return redirect('all_comany_users')
        else:
            messages.error(request, company_user_form.errors)        
        
        return render(request, 'update_company_user.html', {'company_user_form':company_user_form})
    
    except CompanyUser.DoesNotExist:
        messages.error(request, "Company User with CPF %s not found" % company_user_form.cpf)
    except Exception as e:
        messages.error(request, f"Unknown Exception ocurred: {str(e)}")
        return render(request, 'error.html')

    
# TODO: User can't delete themselves
@login_required(login_url="login")
def delete_company_user(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = CompanyUser.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Company User deleted successfully")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"Unknown Exception ocurred: {str(e)}") 
    