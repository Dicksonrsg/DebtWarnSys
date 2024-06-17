from django.contrib.auth.models import User
from django.test import TestCase

from webpage.forms import (AddressForm, CompanyForm, CompanyUserForm, DebtForm,
                           DebtorForm, SignUpForm)


class SignUpFormTests(TestCase):
    def test_clean_method(self):
        # Test clean method with valid data
        form_data = {
            "username": "test@example.com",
            "email": "test@example.com",
            "password1": "my_password123",
            "password2": "my_password123",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Test clean method with invalid data
        form_data["email"] = "different@example.com"
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Both emails should be equal.", form.errors["__all__"])
        self.assertEqual(form.errors["__all__"][0], "Both emails should be equal.")

    def test_fields(self):
        form = SignUpForm()
        self.assertEqual(form.fields["email"].label, "")
        self.assertEqual(form.fields["username"].widget.attrs["placeholder"], "Email")
        # Add more field tests as needed

    def test_meta_model(self):
        form = SignUpForm()
        self.assertEqual(form.Meta.model, User)


class DebtorFormTests(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.form_data = {
            "cpf": "123.456.789-10",
            "phone": "(12) 34567-8901",
        }

    def test_clean_phone(self):
        form = DebtorForm(data=self.form_data)
        form.is_valid()
        cleaned_phone = form.clean_phone()
        self.assertEqual(cleaned_phone, "12 345678901")

    def test_clean_cpf(self):
        form = DebtorForm(data=self.form_data)
        form.is_valid()
        cleaned_cpf = form.clean_cpf()
        self.assertEqual(cleaned_cpf, "12345678910")


class AddressFormTests(TestCase):
    def test_clean_cep(self):
        form = AddressForm(
            data={
                "cep": "59106-114",
            }
        )
        form.is_valid()
        cleaned_cep = form.clean_cep()
        self.assertEqual(cleaned_cep, "59106114")


class CompanyFormTests(TestCase):
    def test_clean_cnpj(self):
        form = CompanyForm(data={"cnpj": "45.713.317/0001-03"})
        form.is_valid()
        cleaned_cnpj = form.clean_cnpj()
        self.assertEqual(cleaned_cnpj, "45713317000103")

    def test_clean_phone(self):
        form = CompanyForm(data={"phone": "(12) 34567-8901"})
        form.is_valid()
        cleaned_phone = form.clean_phone()
        self.assertEqual(cleaned_phone, "12 345678901")


class DebtFormTests(TestCase):
    def test_clean_cpf(self):
        form = DebtForm(data={"cpf": "123.456.789-10"})
        form.is_valid()
        cleaned_cnpj = form.clean_cpf()
        self.assertEqual(cleaned_cnpj, "12345678910")

    def test_clean_cnpj(self):
        form = DebtForm(data={"cnpj": "45.713.317/0001-03"})
        form.is_valid()
        cleaned_cnpj = form.clean_cnpj()
        self.assertEqual(cleaned_cnpj, "45713317000103")


class CompanyUserFormTests(TestCase):
    def test_clean_cpf(self):
        form = CompanyUserForm(data={"cpf": "123.456.789-10"})
        form.is_valid()
        cleaned_cnpj = form.clean_cpf()
        self.assertEqual(cleaned_cnpj, "12345678910")

    def test_clean_phone(self):
        form = CompanyUserForm(data={"phone": "(12) 34567-8901"})
        form.is_valid()
        cleaned_phone = form.clean_phone()
        self.assertEqual(cleaned_phone, "12 345678901")

    def test_clean_cnpj(self):
        form = CompanyUserForm(data={"cnpj": "45.713.317/0001-03"})
        form.is_valid()
        cleaned_cnpj = form.clean_cnpj()
        self.assertEqual(cleaned_cnpj, "45713317000103")
