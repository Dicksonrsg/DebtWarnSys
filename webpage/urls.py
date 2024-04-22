from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # Company
    path('company/<int:primary_key>', views.company_register, name='company'),
    path('delete_company/<int:primary_key>', views.delete_company, name='delete_company'),
    path('add_company/', views.add_company, name='add_company'),
    path('update_company/<int:primary_key>', views.update_company, name='update_company'),
    # Debtor
    path('add_debtor/', views.add_debtor, name='add_debtor'),
    path('debtor/<int:primary_key>', views.debtor_register, name='debtor'),
    path('update_debtor/<int:primary_key>', views.update_debtor, name='update_debtor'),
    path('all_debtors', views.all_debtors, name='all_debtors'),
    path('my_debts', views.all_debts_for_cpf, name='my_debts'),
    # Debt
    path('add_debt', views.add_debt, name='add_debt'),
    path('debt/<int:primary_key>', views.debt_register, name='debt'),
    path('update_debt/<int:primary_key>', views.update_debt, name='update_debt'),
    path('debts_report', views.all_debts_for_cnpj, name='debts_report'),
    path('delete_debt/<int:primary_key>', views.delete_debt, name='delete_debt'),
    # Employee
    path('add_employee', views.add_employee, name='add_employee'),
    path('employee/<int:primary_key>', views.employee_register, name='employee'),
    path('update_employee/<int:primary_key>', views.update_employee, name='update_employee'),
    path('all_employees', views.all_employees, name='all_employees'),
    
]