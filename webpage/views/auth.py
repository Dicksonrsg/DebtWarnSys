from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from ..forms import SignUpForm, UpdatePasswordForm
from ..helper.fetcher import get_debtor, is_debtor
from ..models import Company, CompanyUser


@login_required(login_url="login")
def home(request: WSGIRequest):
    try:
        if request.user.is_superuser:
            companies = Company.objects.all()
            return render(request, "home.html", {"companies": companies})
        else:
            company_user = CompanyUser.objects.get(user_auth=request.user)
            companies = company_user.company.all()
            return render(request, "home.html", {"companies": companies})
    except Company.DoesNotExist:
        messages.error(request, "Companies not found")
        return render(request, "home.html", {"companies": []})
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


# Register and authentication
def login_user(request: WSGIRequest):
    if request.method == "POST":
        user_name = request.POST["email_address"]
        password = request.POST["password"]
        # Authenticate
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are an active user")
            if is_debtor(auth_user=user):
                return redirect("debtor_home")

            return redirect("home")
        else:
            messages.error(request, "You are not an active user, contact us")
            return redirect("login")
    else:
        return render(request, "login.html")


def logout_user(request: WSGIRequest):
    logout(request)
    messages.success(request, "You have logged out")
    return redirect("home")


def register_user(request: WSGIRequest):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        try:
            # Validates if User is Debtor
            is_debtor = request.POST.get("isDebtor")
            debtor_cpf = request.POST.get("debtorCPF")

            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                form.save()

                # Authenticate and login
                user = authenticate(username=username, password=password)
                login(request=request, user=user)
                messages.success(request, "You have registered! Congrats")

                if is_debtor and debtor_cpf:
                    debtor_cpf = debtor_cpf.replace(".", "").replace("-", "")
                    debtor_object = get_debtor(cpf=debtor_cpf)
                    if debtor_object:
                        return redirect("update_debtor", debtor_object.id)
                    else:
                        return redirect("add_debtor")
                else:
                    return redirect("add_company_user")
            else:
                messages.error(request, form.errors)

        except Exception as e:
            status_code = getattr(e, "status_code", None)
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, "error.html", {"status_code": status_code})
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


@login_required(login_url="login")
def update_password(request: WSGIRequest):
    current_user = request.user
    if request.method == "POST":
        try:
            up_form = UpdatePasswordForm(current_user, request.POST)
            if up_form.is_valid():
                up_form.save()
                messages.success(request, "Your Password Has Been Updated...")
                login(request, current_user)
                return redirect("home")
            else:
                for error in list(up_form.errors.values()):
                    messages.error(request, error)
                    return redirect("update_password")
        except Exception as e:
            status_code = getattr(e, "status_code", None)
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, "error.html", {"status_code": status_code})
    else:
        up_form = UpdatePasswordForm(current_user)
        return render(request, "update_password.html", {"up_form": up_form})
