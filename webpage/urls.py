from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # Company
    path('company/<int:primary_key>', views.company_register, name='company'),
    path('delete_company/<int:primary_key>', views.delete_company, name='delete_company'),
    path('add_company/', views.add_company, name='add_company'),
    path('update_company/<int:primary_key>', views.update_company, name='update_company'),
    # Debtor
    path('debtor_home', views.debtor_home, name='debtor_home'),
    path('add_debtor/', views.add_debtor, name='add_debtor'),
    path('debtor/<int:primary_key>', views.debtor_register, name='debtor'),
    path('update_debtor/<int:primary_key>', views.update_debtor, name='update_debtor'),
    path('all_debtors', views.all_debtors, name='all_debtors'),
    path('my_debts', views.all_my_debts, name='my_debts'),
    # Debt
    path('add_debt', views.add_debt, name='add_debt'),
    path('debt/<int:primary_key>', views.debt_register, name='debt'),
    path('update_debt/<int:primary_key>', views.update_debt, name='update_debt'),
    path('debts_report', views.all_debts_for_cnpj, name='debts_report'),
    path('delete_debt/<int:primary_key>', views.delete_debt, name='delete_debt'),
    # CompanyUser
    path('add_company_user', views.add_company_user, name='add_company_user'),
    path('company_user/<int:primary_key>', views.company_user_register, name='company_user'),
    path('update_company_user/<int:primary_key>', views.update_company_user, name='update_company_user'),
    path('all_company_users', views.all_company_users, name='all_company_users'),
    path('delete_company_user/<int:primary_key>', views.delete_company_user, name='delete_company_user'),
    
]