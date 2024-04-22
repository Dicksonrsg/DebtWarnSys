from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddressForm, CompanyForm, DebtorForm, DebtForm, EmployeeForm
from .models import Company, Address, Debtor, Debt, Employee

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
    else:
        messages.success(request, "You must be logged in to add company")
        return redirect('home')


def company_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
        # Look Up Company
            user_company = Company.objects.get(id=primary_key)
            return render(request, 'company.html', {'user_company':user_company})
        except Company.DoesNotExist:
            messages.error(request, "Companies not found")
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.success(request, "There is no company to be displayed")
        return redirect('home') 

    
def update_company(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
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
    else:
        messages.success(request, "You must be logged in to update company")
        return redirect('home')


def delete_company(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
            to_be_deleted = Company.objects.get(id=primary_key)
            to_be_deleted.delete()
            messages.success(request, "Company deleted successfully")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html') 
    else:
        messages.success(request, "You must be logged in to delete")
        return redirect('home')  
 

# Debtor
def add_debtor(request: HttpRequest):
    debtor_form = DebtorForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                if debtor_form.is_valid() and address_form.is_valid():
                    address = address_form.save()
                    debtor_form.instance.address = address
                    debtor_form.save()
                    messages.success(request, "Success, Debtor added")
                    return redirect('home')
                else:
                    messages.error(request, debtor_form.errors)
            except Exception as e:
                messages.error(request, f"Unknown Exception ocurred: {str(e)}")
                return render(request, 'error.html') 
                            
        return render(request, 'add_debtor.html', {'debtor_form':debtor_form, 'address_form': address_form})
    else:
        messages.success(request, "You must be logged in to add debtor")
        return redirect('home')
    

def debtor_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
            # Look Up Debtor
            debtor = Debtor.objects.get(id=primary_key)
            return render(request, 'debtor.html', {'debtor':debtor})
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.success(request, "You must be logged in to view Debtors")
        return redirect('home')


def all_debtors(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            debtors = Debtor.objects.all()
            return render(request, 'all_debtors.html', {'debtors':debtors})
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.error(request, "You must be logged in to view Debtors")
        return redirect('home')
    

def update_debtor(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
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
        except Debtor.DoesNotExist:
            messages.error(request, "Debtor with Id %s not found" % primary_key)
        except Address.DoesNotExist:
            messages.error(request, "Address with Id %s not found" % current_debtor.address.id)
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.success(request, "You must be logged in to update debtor")
        return redirect('home')
    
    
def delete_debtor(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
            to_be_deleted = Debtor.objects.get(id=primary_key)
            to_be_deleted.delete()
            messages.success(request, "Debtor deleted successfully")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
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
                messages.error(request, "Company with CNPJ %s not found" % debt_form.cleaned_data['cnpj']) 
            except Debtor.DoesNotExist:
                messages.error(request, "Debtor with CPF %s not found" % debt_form.cleaned_data['cpf'])
            except Exception as e:
                messages.error(request, f"An Exception ocurred: {str(e)}")
                return render(request, 'error.html')
                
        return render(request, 'add_debt.html', {'debt_form':debt_form})
    else:
        messages.success(request, "You must be logged in to add debt")
        return redirect('home')
    

def debt_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
            # Look Up Debt
            debt = Debt.objects.get(id=primary_key)
            return render(request, 'debt.html', {'debt':debt})
        except Debt.DoesNotExist:
            messages.error(request, "Debt with Id %s not found" % primary_key)
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
        
    else:
        messages.success(request, "You must be logged in to view Debt")
        return redirect('home')
    
# Look Up Debts
# TODO: Get Debts by company   
def all_debts_for_cnpj(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            debts = Debt.objects.all()
            return render(request, 'debts_report.html', {'debts':debts})
        except Debt.DoesNotExist:
            messages.error(request, "Debts not found")
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.success(request, "You must be logged in to view Debts")
        return redirect('debts_report')
    
def all_debts_for_cpf(request: HttpRequest, debtor_cpf: str):
    if request.user.is_authenticated:
        try:
            debts = Debt.objects.get(cpf=debtor_cpf)
            return render(request, 'my_debts.html', {'debts': debts})
        except Debt.DoesNotExist:
            messages.error(request, "Debts not found")
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.success(request, "You must be logged in to view Debts")
        return redirect('my_Debts')

def update_debt(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
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
    else:
        messages.success(request, "You must be logged in to update debt")
        return redirect('home')
    
    
def delete_debt(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
            to_be_deleted = Debt.objects.get(id=primary_key)
            to_be_deleted.delete()
            messages.success(request, "Debt deleted successfully")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.success(request, "You must be logged in to delete")
        return redirect('home') 


# Employee
def add_employee(request: HttpRequest):
    employee_form = EmployeeForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                if employee_form.is_valid() and address_form.is_valid():
                    address = address_form.save()
                    employee_form.instance.address = address
                    company = Company.objects.get(cnpj=employee_form.cleaned_data['cnpj'])
                    employee_form.instance.creditor = company
                    employee_form.save()
                    messages.success(request, "Success, Employee added")
                    return redirect('home')
                else:
                    messages.error(request, employee_form.errors or address_form.errors)
            except Company.DoesNotExist:
                messages.error(request, "Company with CNPJ %s not found" % employee_form.cleaned_data['cnpj'])
            except Exception as e:
                messages.error(request, f"An Exception ocurred: {str(e)}")
                return render(request, 'error.html')
                
        return render(request, 'add_employee.html', {'employee_form':employee_form, 'address_form': address_form})
    else:
        messages.success(request, "You must be logged in to add Employee")
        return redirect('home')
    

def employee_register(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        # Look Up Employee
        # TODO: Return only employees if logged user has permission
        try:
            employee = Employee.objects.get(id=primary_key)
            return render(request, 'employee.html', {'employee':employee})
        except Employee.DoesNotExist:
            messages.error(request, "Employee with Id %s not found" % primary_key)
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.error(request, "You must be logged in to access this register")
        return redirect('home')
    
# Look Up Employees
# TODO: Bring only employees from a specific CNPJ    
def all_employees(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            employees = Employee.objects.all()
            return render(request, 'all_employees.html', {'employees': employees})
        except Employee.DoesNotExist:
            messages.error(request, "Employees not found")
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.error(request, "You must be logged in to access employees section")
        return redirect('home')
    

def update_employee(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
            current_employee = Employee.objects.get(id=primary_key)
            employee_form = EmployeeForm(request.POST or None, instance=current_employee)
            if employee_form.is_valid():
                employee_form.save()
                messages.success(request, "Success, Employee updated")
                return redirect('home')
            else:
                messages.error(request, employee_form.errors)        
            
            return render(request, 'update_employee.html', {'employee_form':employee_form})
        
        except Employee.DoesNotExist:
            messages.error(request, "Employee with CPF %s not found" % employee_form.cpf)
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
            return render(request, 'error.html')
    else:
        messages.error(request, "You must be logged in to update employee")
        return redirect('home')
    
    
def delete_employee(request: HttpRequest, primary_key: int):
    if request.user.is_authenticated:
        try:
            to_be_deleted = Employee.objects.get(id=primary_key)
            to_be_deleted.delete()
            messages.success(request, "Employee deleted successfully")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Unknown Exception ocurred: {str(e)}")
    else:
        messages.error(request, "You must be logged in to delete")
        return redirect('home') 
    