from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from ..forms import AddressForm, DebtorForm
from ..helper.auth import assign_group
from ..helper.fetcher import get_auth_user
from ..models import Address, Debtor


# Debtor
@login_required(login_url="login")
def add_debtor(request: WSGIRequest):
    debtor_form = DebtorForm(request.POST or None)
    address_form = AddressForm(request.POST or None)
    if request.method == "POST":
        try:
            if debtor_form.is_valid() and address_form.is_valid():
                current_user = get_auth_user(user_id=request.user.id)
                address = address_form.save()
                debtor_form.instance.address = address
                debtor_form.instance.user_auth = current_user
                debtor_form.save()
                assign_group(user_name=request.user.username, role="Debtor")
                messages.success(request, "Success, Debtor added")
                return redirect("home")
            else:
                messages.error(request, debtor_form.errors)
        except Exception as e:
            status_code = getattr(e, "status_code", None)
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, "error.html", {"status_code": status_code})

    return render(
        request,
        "add_debtor.html",
        {"debtor_form": debtor_form, "address_form": address_form},
    )


@login_required(login_url="login")
@permission_required(
    perm="webpage.view_debtor", login_url="login", raise_exception=True
)
def debtor_home(request: WSGIRequest):
    try:
        debtor = Debtor.objects.get(user_auth=request.user)
        return render(request, "debtor_home.html", {"debtor": debtor})
    except Debtor.DoesNotExist as e:
        messages.error(request, "Debtor not found")
        status_code = getattr(e, "status_code", None)
        return render(request, "error.html", {"status_code": status_code})
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.view_debtor", login_url="login", raise_exception=True
)
def debtor_register(request: WSGIRequest, primary_key: int):
    try:
        # Look Up Debtor
        debtor = Debtor.objects.get(id=primary_key)
        return render(request, "debtor.html", {"debtor": debtor})
    except Debtor.DoesNotExist:
        messages.error(request, f"Debtor was not found for Id: {primary_key}")
        return redirect("all_debtors")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.view_debtor", login_url="login", raise_exception=True
)
def all_debtors(request: WSGIRequest):
    try:
        debtors = Debtor.objects.all()
        return render(request, "all_debtors.html", {"debtors": debtors})
    except Debtor.DoesNotExist:
        messages.error(request, f"There are no Debtors to be displayed")
        return render(request, "all_debtors.html", {"debtors": None})
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.change_debtor", login_url="login", raise_exception=True
)
def update_debtor(request: WSGIRequest, primary_key: int):
    try:
        current_debtor = Debtor.objects.get(id=primary_key)
        current_address = Address.objects.get(id=current_debtor.address.id)
        current_user = get_auth_user(user_id=request.user.id)
        debtor_form = DebtorForm(request.POST or None, instance=current_debtor)
        address_form = AddressForm(request.POST or None, instance=current_address)
        if debtor_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            debtor_form.instance.address = address
            debtor_form.instance.user_auth = current_user
            debtor_form.save()
            messages.success(request, "Success, Debtor updated")
            return redirect("home")
        else:
            messages.error(request, debtor_form.errors)

        return render(
            request,
            "update_debtor.html",
            {"debtor_form": debtor_form, "address_form": address_form},
        )
    except Debtor.DoesNotExist:
        messages.error(request, "Debtor with Id %s not found" % primary_key)
    except Address.DoesNotExist:
        messages.error(
            request, "Address with Id %s not found" % current_debtor.address.id
        )
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.delete_debtor", login_url="login", raise_exception=True
)
def delete_debtor(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = Debtor.objects.get(id=primary_key)
        current_user = Debtor.objects.get(user_auth=request.user)
        if to_be_deleted == current_user:
            messages.error(request, "Sorry, You can not delete yourself")
            return redirect("home")

        to_be_deleted.delete()
        messages.success(request, "Debtor deleted successfully")
        return redirect("home")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})
