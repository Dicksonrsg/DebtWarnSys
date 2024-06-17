import os
import pytest
from django.conf import settings
from pytest_factoryboy import register
from webpage.tests.factories import (
    UserFactory, AddressFactory, CompanyFactory,
    CompanyUserFactory, DebtorFactory, DebtFactory
)

os.environ['DJANGO_SETTINGS_MODULE'] = 'dws.settings'

register(UserFactory)
register(AddressFactory)
register(CompanyFactory)
register(CompanyUserFactory)
register(DebtorFactory)
register(DebtFactory)

