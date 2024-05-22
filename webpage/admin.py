from django.contrib import admin

from .models import Address, Company, CompanyUser, Debt, Debtor

admin.site.register(Company)
admin.site.register(CompanyUser)
admin.site.register(Debtor)
admin.site.register(Debt)
admin.site.register(Address)
