from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from webpage.forms import (AddressForm, CompanyForm)
from webpage.models import Address, Company


# Company
@login_required(login_url="login")
@permission_required(
    perm="webpage.add_company", login_url="login", raise_exception=True
)
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
                return redirect("home")
            else:
                messages.error(request, company_form.errors)
        except Exception as e:
            status_code = getattr(e, "status_code", None)
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, "error.html", {"status_code": status_code})

    return render(
        request,
        "add_company.html",
        {"company_form": company_form, "address_form": address_form},
    )


@login_required(login_url="login")
@permission_required(
    perm="webpage.view_company", login_url="login", raise_exception=True
)
def company_register(request: WSGIRequest, primary_key: int):
    try:
        # Look Up Company
        user_company = Company.objects.get(id=primary_key)
        return render(request, "company.html", {"user_company": user_company})
    except Company.DoesNotExist:
        messages.error(request, "Companies not found")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.change_company", login_url="login", raise_exception=True
)
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
            return redirect("home")
        else:
            messages.error(request, company_form.errors)

        return render(
            request,
            "update_company.html",
            {"company_form": company_form, "address_form": address_form},
        )

    except Company.DoesNotExist as e:
        messages.error(request, "Company with Id %s not found" % primary_key)
    except Address.DoesNotExist as e:
        messages.error(
            request, "Address with Id %s not found" % current_company.address.id
        )
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.delete_company", login_url="login", raise_exception=True
)
def delete_company(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = Company.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Company deleted successfully")
        return redirect("home")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})
