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

]