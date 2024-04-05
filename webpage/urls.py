from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('company/<int:primary_key>', views.company_register, name='company'),
    path('delete_company/<int:primary_key>', views.delete_company, name='delete_company'),
    path('add_company/', views.add_company, name='add_company'),
    path('update_company/<int:primary_key>', views.update_company, name='update_company'),
    path('add_debtor/', views.add_debtor, name='add_debtor'),
    path('debtor/<int:primary_key>', views.debtor_register, name='debtor'),
    path('update_debtor/<int:primary_key>', views.update_debtor, name='update_debtor'),
    path('add_debt', views.add_debt, name='add_debt'),
    path('all_debtors', views.all_debtors, name='all_debtors'),        

]