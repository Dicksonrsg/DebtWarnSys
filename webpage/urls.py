from django.urls import path

from webpage.views import auth, company, company_user, debt, debtor

urlpatterns = [
    path("", auth.home, name="home"),
    path("login/", auth.login_user, name="login"),
    path("logout/", auth.logout_user, name="logout"),
    path("register/", auth.register_user, name="register"),
    path("update_password/", auth.update_password, name="update_password"),
    # Company
    path("company/<int:primary_key>", company.company_register, name="company"),
    path(
        "delete_company/<int:primary_key>",
        company.delete_company,
        name="delete_company",
    ),
    path("add_company/", company.add_company, name="add_company"),
    path(
        "update_company/<int:primary_key>",
        company.update_company,
        name="update_company",
    ),
    # Debtor
    path("debtor_home", debtor.debtor_home, name="debtor_home"),
    path("add_debtor/", debtor.add_debtor, name="add_debtor"),
    path("debtor/<int:primary_key>", debtor.debtor_register, name="debtor"),
    path("update_debtor/<int:primary_key>", debtor.update_debtor, name="update_debtor"),
    path("all_debtors", debtor.all_debtors, name="all_debtors"),
    # Debt
    path("add_debt", debt.add_debt, name="add_debt"),
    path("debt/<int:primary_key>", debt.debt_register, name="debt"),
    path("my_debts", debt.all_my_debts, name="my_debts"),
    path("update_debt/<int:primary_key>", debt.update_debt, name="update_debt"),
    path("debts_report", debt.all_debts_for_cnpj, name="debts_report"),
    path("delete_debt/<int:primary_key>", debt.delete_debt, name="delete_debt"),
    # CompanyUser
    path("add_company_user", company_user.add_company_user, name="add_company_user"),
    path(
        "company_user/<int:primary_key>",
        company_user.company_user_register,
        name="company_user",
    ),
    path(
        "update_company_user/<int:primary_key>",
        company_user.update_company_user,
        name="update_company_user",
    ),
    path("all_company_users", company_user.all_company_users, name="all_company_users"),
    path(
        "delete_company_user/<int:primary_key>",
        company_user.delete_company_user,
        name="delete_company_user",
    ),
]
