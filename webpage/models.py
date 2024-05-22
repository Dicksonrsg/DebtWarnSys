from django.contrib.auth.admin import User
from django.db import models
from django_countries.fields import CountryField
from localflavor.br.models import BRStateField


class Address(models.Model):
    cep = models.CharField(max_length=8, blank=False, null=False)
    street = models.CharField(max_length=140, blank=False, null=False)
    number = models.CharField(max_length=9, blank=False, null=False)
    neighbourhood = models.CharField(max_length=60, blank=False, null=False)
    state = BRStateField(blank=False, null=False)
    country = CountryField(blank_label="(select country)")
    details = models.CharField(max_length=140, blank=True, null=True)


class Person(models.Model):
    user_auth = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=140)
    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    phone = models.CharField(max_length=14)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    trading_name = models.CharField(max_length=140, blank=False, null=False)
    company_name = models.CharField(max_length=140, blank=False, null=False)
    cnpj = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=14, default="")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Name: {self.company_name}"


class CompanyUser(Person):
    OWNER = "Owner"
    ADMIN = "Admin"
    WORKER = "Worker"
    ROLE = [
        (OWNER, "Owner - All power"),
        (ADMIN, "Admin - Administrative"),
        (WORKER, "Worker - Operation level"),
    ]

    role = models.CharField(max_length=9, choices=ROLE, default=WORKER)
    company = models.ManyToManyField(Company)

    def __str__(self) -> str:
        return f"Name: {self.name}"


class Debtor(Person):
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Name: {self.name}"


class Debt(models.Model):
    PAID = "Paid"
    PAST_DUE = "Past Due"
    CONTESTED = "Contested"
    STATUS = [
        (PAID, "Paid - Debt was paid"),
        (PAST_DUE, "Past due - Debt has not been paid"),
        (CONTESTED, "Contested - Debt has been contested"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.EmailField(blank=False, null=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    contract = models.CharField(max_length=70, unique=True, blank=False, null=False)
    due_date = models.DateField(blank=False, null=False)
    status = models.CharField(max_length=70, choices=STATUS, default=PAST_DUE)
    value = models.FloatField(blank=False, null=False)
    times_contacted = models.IntegerField(blank=True, null=True)
    last_contact = models.DateTimeField(blank=True, null=True)
    creditor = models.ForeignKey(Company, on_delete=models.CASCADE)
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Contract: {self.contract}"
