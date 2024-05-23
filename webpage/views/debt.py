from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render

from ..forms import DebtForm
from ..helper.fetcher import get_company_id
from ..models import Company, Debt, Debtor


# Debt
@login_required(login_url="login")
@permission_required(perm="webpage.add_debt", login_url="login", raise_exception=True)
def add_debt(request: WSGIRequest):
    debt_form = DebtForm(request.POST or None)
    if request.method == "POST":
        try:
            if debt_form.is_valid():
                company = Company.objects.get(cnpj=debt_form.cleaned_data["cnpj"])
                debtor = Debtor.objects.get(cpf=debt_form.cleaned_data["cpf"])
                debt_form.instance.creditor = company
                debt_form.instance.debtor = debtor
                to_save_df = debt_form.save(commit=False)
                to_save_df.created_by = request.user.email
                to_save_df.save()
                messages.success(request, "Success, Debt added")
                return redirect("home")
            else:
                messages.error(request, debt_form.errors)
        except Company.DoesNotExist:
            messages.error(
                request,
                "Company with CNPJ %s not found" % debt_form.cleaned_data["cnpj"],
            )
        except Debtor.DoesNotExist:
            messages.error(
                request, "Debtor with CPF %s not found" % debt_form.cleaned_data["cpf"]
            )
        except Exception as e:
            status_code = getattr(e, "status_code", None)
            messages.error(request, f"An Exception ocurred: {str(e)}")
            return render(request, "error.html", {"status_code": status_code})

    return render(request, "add_debt.html", {"debt_form": debt_form})


@login_required(login_url="login")
@permission_required(perm="webpage.view_debt", login_url="login", raise_exception=True)
def debt_register(request: WSGIRequest, primary_key: int):
    try:
        # Look Up Debt
        debt = Debt.objects.get(id=primary_key)
        return render(request, "debt.html", {"debt": debt})
    except Debt.DoesNotExist:
        messages.error(request, "Debt with Id %s not found" % primary_key)
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


# Look Up Debts
@login_required(login_url="login")
@permission_required(perm="webpage.view_debt", login_url="login", raise_exception=True)
def all_debts_for_cnpj(request: WSGIRequest):
    try:
        # debts = Debt.objects.filter(creditor=user.company)
        if request.user.is_superuser:
            debts = Debt.objects.all()
            return render(request, "debts_report.html", {"debts": debts})
        else:
            company_id = get_company_id(auth_user=request.user)
            debts = Debt.objects.filter(creditor=company_id)
            return render(request, "debts_report.html", {"debts": debts})
    except Debt.DoesNotExist:
        messages.error(request, "Debts not found")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(perm="webpage.view_debt", login_url="login", raise_exception=True)
def all_my_debts(request: WSGIRequest):
    try:
        debtor = Debtor.objects.get(user_auth=request.user)
        debts = Debt.objects.filter(cpf=debtor.cpf)
        return render(request, "my_debts.html", {"debts": debts})
    except Debtor.DoesNotExist:
        messages.error(request, "Debtor not found")
    except Debt.DoesNotExist:
        messages.error(request, "Debts not found")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.change_debt", login_url="login", raise_exception=True
)
def update_debt(request: WSGIRequest, primary_key: int):
    try:
        current_debt = Debt.objects.get(id=primary_key)
        debt_form = DebtForm(request.POST or None, instance=current_debt)
        if debt_form.is_valid():
            debt_form.save()
            messages.success(request, "Success, Debt updated")
            return redirect("home")
        else:
            messages.error(request, debt_form.errors)

        return render(request, "update_debt.html", {"debt_form": debt_form})
    except Debt.DoesNotExist:
        messages.error(request, "Debt with Id %s not found" % primary_key)
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})


@login_required(login_url="login")
@permission_required(
    perm="webpage.delete_debt", login_url="login", raise_exception=True
)
def delete_debt(request: WSGIRequest, primary_key: int):
    try:
        to_be_deleted = Debt.objects.get(id=primary_key)
        to_be_deleted.delete()
        messages.success(request, "Debt deleted successfully")
        return redirect("home")
    except Exception as e:
        status_code = getattr(e, "status_code", None)
        messages.error(request, f"An Exception ocurred: {str(e)}")
        return render(request, "error.html", {"status_code": status_code})
