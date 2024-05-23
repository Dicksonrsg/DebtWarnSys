from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from ..forms import (AddressForm, CompanyUserForm)
from ..helper.auth import assign_group
from ..helper.fetcher import (get_auth_user, get_company_id)
from ..models import Company, CompanyUser


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
                company = Company.objects.get(
                    cnpj=company_user_form.cleaned_data["cnpj"]
                )
                user_auth = get_auth_user(user_id=request.user.id)
                company_user_form.instance.user_auth = user_auth
                new_c_user = company_user_form.save()
                new_c_user.company.add(company)
                assign_group(
                    user_name=request.user.username,
                    role=company_user_form.cleaned_data["role"],
                )
                messages.success(request, "Success, Company User added")
                return redirect("home")
            else:
                messages.error(request, company_user_form.errors or address_form.errors)
        except Company.DoesNotExist:
            messages.error(
                request,
                "Company with CNPJ %s not found"
                % company_user_form.cleaned_data["cnpj"],
            )
        except Exception as e:
            status_code = getattr(e, "status_code", None)
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, "error.html", {"status_code": status_code})

    return render(
        request,
        "add_company_user.html",
        {"company_user_form": company_user_form, "address_form": address_form},
    )


@login_required(login_url="login")
@permission_required(
    perm="webpage.view_companyuser", login_url="login", raise_exception=True
)
def company_user_register(request: WSGIRequest, primary_key: int):
    # Look Up CompanyUSer
    try:
        company_user = CompanyUser.objects.get(id=primary_key)
        return render(request, "company_user.html", {"company_user": company_user})
    except CompanyUser.DoesNotExist:
        messages.error(request, "Company User with Id %s not found" % primary_key)
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.view_companyuser", login_url="login", raise_exception=True
)
def all_company_users(request: WSGIRequest):
    try:
        if request.user.is_superuser:
            company_users = CompanyUser.objects.all()
            return render(
                request, "all_company_users.html", {"company_users": company_users}
            )
        else:
            company_id = get_company_id(auth_user=request.user)
            company_users = CompanyUser.objects.filter(company=company_id)
            return render(
                request, "all_company_users.html", {"company_users": company_users}
            )
    except CompanyUser.DoesNotExist:
        messages.error(request, "Company Users not found")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.change_companyuser", login_url="login", raise_exception=True
)
def update_company_user(request: WSGIRequest, primary_key: int):
    try:
        current_company_user = CompanyUser.objects.get(id=primary_key)
        company_user_form = CompanyUserForm(
            request.POST or None, instance=current_company_user
        )
        if company_user_form.is_valid():
            company_user_form.save()
            messages.success(request, "Success, Company User updated")
            return redirect("all_comany_users")
        else:
            messages.error(request, company_user_form.errors)

        return render(
            request,
            "update_company_user.html",
            {"company_user_form": company_user_form},
        )

    except CompanyUser.DoesNotExist:
        messages.error(
            request, "Company User with CPF %s not found" % company_user_form.cpf
        )
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.delete_companyuser", login_url="login", raise_exception=True
)
def delete_company_user(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = CompanyUser.objects.get(id=primary_key)
        current_user = CompanyUser.objects.get(user_auth=request.user)
        if to_be_deleted == current_user:
            messages.error(request, "Sorry, You can not delete yourself")
            return redirect("home")

        to_be_deleted.delete()
        messages.success(request, "Company User deleted successfully")
        return redirect("home")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})
