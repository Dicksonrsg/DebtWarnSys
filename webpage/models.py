from django.db import models

# https://docs.djangoproject.com/en/5.0/topics/db/models/
# Abstract base classes

class Address(models.Model):
    cep = models.CharField(max_length=8)
    street = models.CharField(max_length=140)
    number = models.CharField(max_length=7)
    neighbourhood = models.CharField(max_length=60)
    state = models.CharField(max_length=140)
    country = models.CharField(max_length=14)
    details = models.CharField(max_length=140)
    

class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=140)
    cpf = models.CharField(max_length=11)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=140)
    address = models.OneToOneField(Address, on_delete = models.CASCADE)
    
    class Meta:
        abstract = True


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    trading_name = models.CharField(max_length=140)
    company_name = models.CharField(max_length=140)
    cnpj = models.CharField(max_length=14)
    address = models.OneToOneField(Address, on_delete = models.CASCADE)
    
    def __str__(self) -> str:
        return(f"Name: {self.company_name}") 

    
class Employee(Person):
    role = models.CharField(max_length=70)
    company = models.ManyToManyField(Company)
    
    def __str__(self) -> str:
        return(f"Name: {self.name}")
    
    
class Debtor(Person):
    active = models.BooleanField(default=True)  
          
    def __str__(self) -> str:
        return(f"Name: {self.name}")   
    
    
class Debt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    contract = models.CharField(max_length=70)
    due_date = models.DateField()
    status = models.CharField(max_length=70)
    creditor = models.ForeignKey(Company, on_delete = models.CASCADE)
    debtor = models.ForeignKey(Debtor, on_delete = models.CASCADE)
    
    def __str__(self) -> str:
        return(f"Contract: {self.contract}")
    