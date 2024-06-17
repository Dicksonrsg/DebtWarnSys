import pytest

pytestmark = pytest.mark.django_db


class TestCompanyModel:
    def test_str_return(self, company_factory):
        c_name = "test-name"
        company = company_factory(company_name=c_name)
        assert company.__str__() == f"Name: {c_name}"


class TestCompanyUserModel:
    def test_str_return(self, company_user_factory):
        c_name = "test-name"
        company_user = company_user_factory(name=c_name)
        assert company_user.__str__() == f"Name: {c_name}"


class TestDebtorModel:
    def test_str_return(self, debtor_factory):
        name = "test-name"
        debtor = debtor_factory(name=name)
        assert debtor.__str__() == f"Name: {name}"


class TestDebtModel:
    def test_str_return(self, debt_factory):
        contract = "test-contract"
        debt = debt_factory(contract=contract)
        assert debt.__str__() == f"Contract: {contract}"
