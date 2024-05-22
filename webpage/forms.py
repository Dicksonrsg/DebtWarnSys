from django import forms
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from localflavor.br import forms as lf_forms

from .models import Address, Company, CompanyUser, Debt, Debtor


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=140,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=210,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields.pop("first_name")
        self.fields.pop("last_name")

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Email"
        self.fields["username"].label = "Email Address"
        self.fields[
            "username"
        ].help_text = '<span class="form-text text-muted"><small>Required. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "Confirm Email"
        self.fields["email"].label = ""
        self.fields[
            "email"
        ].help_text = '<span class="form-text text-muted"><small>Required. Type the same Email address as above.</small></span>'

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = "Password"
        self.fields[
            "password1"
        ].help_text = "<ul class=\"form-text text-muted small\"><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields[
            "password2"
        ].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        if username != email:
            raise ValidationError("Both emails should be equal.")
        return cleaned_data


class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["placeholder"] = "Password"
        self.fields["new_password1"].label = "Create new password"
        self.fields[
            "new_password1"
        ].help_text = "<ul class=\"form-text text-muted small\"><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"

        self.fields["new_password2"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["new_password2"].label = "Confirm new password"
        self.fields[
            "new_password2"
        ].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class AddressForm(forms.ModelForm):
    cep = forms.CharField(
        max_length=9,
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"data-mask": "00000-000", "class": "form-control"}
        ),
        label="Cep",
    )
    street = forms.CharField(
        max_length=140,
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Street", "class": "form-control"}
        ),
        label="Street",
    )
    number = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Number", "class": "form-control"}
        ),
        label="Number",
    )
    neighbourhood = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Neighbourhood", "class": "form-control"}
        ),
        label="Neighbourhood",
    )
    state = lf_forms.BRStateChoiceField(required=True)
    country = CountryField().formfield()
    details = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Details", "class": "form-control"}
        ),
        label="Details",
    )

    def clean_cep(self):
        cep = self.cleaned_data["cep"]
        return cep.replace("-", "")

    class Meta:
        model = Address
        fields = (
            "cep",
            "street",
            "number",
            "neighbourhood",
            "state",
            "country",
            "details",
        )


class CompanyForm(forms.ModelForm):
    trading_name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Trading Name", "class": "form-control"}
        ),
        label="Trading Name",
    )
    company_name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Company Name", "class": "form-control"}
        ),
        label="Company Name",
    )
    cnpj = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "CNPJ",
                "data-mask": "00.000.000/0000-00",
                "class": "form-control",
            }
        ),
        label="CNPJ",
    )
    phone = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Phone",
                "data-mask": "(00) 00000-0000",
                "class": "form-control",
            }
        ),
        label="Phone",
    )

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

    def clean_cnpj(self):
        cnpj = self.cleaned_data["cnpj"]
        return cnpj.replace(".", "").replace("/", "").replace("-", "")

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        return phone.replace("(", "").replace(")", "").replace("-", "")

    class Meta:
        model = Company
        fields = ("trading_name", "company_name", "cnpj", "phone")


class DebtorForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Name", "class": "form-control"}
        ),
        label="Name",
    )
    cpf = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "CPF",
                "data-mask": "000.000.000-00",
                "class": "form-control",
            }
        ),
        label="CPF",
    )
    phone = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Phone",
                "data-mask": "(00) 00000-0000",
                "class": "form-control",
            }
        ),
        label="Phone",
    )
    active = forms.BooleanField(
        required=True,
        widget=forms.widgets.NullBooleanSelect(
            attrs={"placeholder": "Active", "class": "form-control"}
        ),
        label="Active",
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        return phone.replace("(", "").replace(")", "").replace("-", "")

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        return cpf.replace(".", "").replace("-", "")

    class Meta:
        model = Debtor
        fields = ("name", "cpf", "phone", "active")


class DebtForm(forms.ModelForm):
    created_by = forms.EmailField(required=False, widget=forms.widgets.HiddenInput())
    contract = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Contract", "class": "form-control"}
        ),
        label="Contract",
    )
    due_date = forms.DateField(
        required=True,
        widget=forms.widgets.DateInput(
            format="%m-%d-%Y", attrs={"type": "date", "class": "form-control"}
        ),
        label="Due Date",
    )
    status = forms.ChoiceField(choices=Debt.STATUS, label="Status")
    value = forms.FloatField(
        required=True,
        widget=forms.widgets.NumberInput(attrs={"class": "form-control"}),
        label="Value",
    )
    cpf = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", "data-mask": "000.000.000-00"}
        ),
        label="CPF",
    )
    cnpj = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", "data-mask": "00.000.000/0000-00"}
        ),
        label="CNPJ",
    )

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        return cpf.replace(".", "").replace("-", "")

    def clean_cnpj(self):
        cnpj = self.cleaned_data["cnpj"]
        return cnpj.replace(".", "").replace("/", "").replace("-", "")

    class Meta:
        model = Debt
        fields = (
            "created_by",
            "contract",
            "due_date",
            "status",
            "value",
            "cpf",
            "cnpj",
        )


class CompanyUserForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Name", "class": "form-control"}
        ),
        label="Name",
    )
    cpf = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "CPF",
                "class": "form-control",
                "data-mask": "000.000.000-00",
            }
        ),
        label="CPF",
    )
    phone = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                "placeholder": "Phone",
                "class": "form-control",
                "data-mask": "(00) 00000-0000",
            }
        ),
        label="Phone",
    )
    role = forms.ChoiceField(choices=CompanyUser.ROLE, label="Role")
    cnpj = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control", "data-mask": "00.000.000/0000-00"}
        ),
        label="CNPJ",
    )

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        return cpf.replace(".", "").replace("-", "")

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        return phone.replace("(", "").replace(")", "").replace("-", "")

    def clean_cnpj(self):
        cnpj = self.cleaned_data["cnpj"]
        return cnpj.replace(".", "").replace("/", "").replace("-", "")

    class Meta:
        model = CompanyUser
        fields = ("name", "cpf", "phone", "role", "cnpj")
