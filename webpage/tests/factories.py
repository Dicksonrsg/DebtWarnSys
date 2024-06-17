import factory
from faker import Faker
fake = Faker()

import datetime

from django.contrib.auth.models import User
from webpage.models import Address, Company, CompanyUser, Debtor, Debt
from webpage.tests.utils import generate_cnpj, generate_cpf



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    is_active = True
    
    
class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address
        
    cep = fake.zipcode()
    street = fake.street_name()
    number = '81'
    neighbourhood = f'{fake.color} Canyon'
    state = f'{fake.color} North'
    country = fake.country()
    
    
class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        
    trading_name = fake.company()
    company_name = fake.company()
    cnpj = generate_cnpj()
    phone = fake.phone_number()
    address = factory.SubFactory(AddressFactory)


class CompanyUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyUser
        
    user_auth = factory.SubFactory(UserFactory)
    name = fake.name()
    cpf = generate_cpf()
    phone = fake.phone_number()
    address = factory.SubFactory(AddressFactory)
    role = "Worker"
    
    @factory.post_generation
    def company(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.company.add(*extracted)
        self.save()
    
    
class DebtorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Debtor
        
    user_auth = factory.SubFactory(UserFactory)
    name = fake.name()
    cpf = generate_cpf()
    phone = fake.phone_number()
    address = factory.SubFactory(AddressFactory)
    active = True
    

class DebtFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Debt
        
    contract = "TESTEABC"
    due_date = fake.date_this_decade(before_today=True)
    status = "Past Due"
    value = 43.34
    creditor = factory.SubFactory(CompanyFactory)
    debtor = factory.SubFactory(DebtorFactory)