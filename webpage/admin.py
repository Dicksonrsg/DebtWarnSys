from django.contrib import admin
from .models import Company, Employee, Debtor, Debt, Address

admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Debtor)
admin.site.register(Debt)
admin.site.register(Address)