# Generated by Django 4.2.10 on 2024-04-24 20:06

import django.db.models.deletion
import django_countries.fields
import localflavor.br.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cep", models.CharField(max_length=8)),
                ("street", models.CharField(max_length=140)),
                ("number", models.CharField(max_length=9)),
                ("neighbourhood", models.CharField(max_length=60)),
                ("state", localflavor.br.models.BRStateField(max_length=2)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("details", models.CharField(blank=True, max_length=140, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("trading_name", models.CharField(max_length=140)),
                ("company_name", models.CharField(max_length=140)),
                ("cnpj", models.CharField(max_length=14, unique=True)),
                ("phone", models.CharField(default="", max_length=14)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webpage.address",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Debtor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=140)),
                ("cpf", models.CharField(max_length=11, unique=True)),
                ("phone", models.CharField(max_length=14)),
                ("active", models.BooleanField(default=True)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webpage.address",
                    ),
                ),
                (
                    "user_auth",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Debt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.EmailField(max_length=254)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("contract", models.CharField(max_length=70, unique=True)),
                ("due_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Paid", "Paid - Debt was paid"),
                            ("Past Due", "Past due - Debt has not been paid"),
                            ("Contested", "Contested - Debt has been contested"),
                        ],
                        default="Past Due",
                        max_length=70,
                    ),
                ),
                ("value", models.FloatField()),
                ("times_contacted", models.IntegerField(blank=True, null=True)),
                ("last_contact", models.DateTimeField(blank=True, null=True)),
                (
                    "creditor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webpage.company",
                    ),
                ),
                (
                    "debtor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="webpage.debtor"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanyUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=140)),
                ("cpf", models.CharField(max_length=11, unique=True)),
                ("phone", models.CharField(max_length=14)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Owner", "Owner - All power"),
                            ("Admin", "Admin - Administrative"),
                            ("Worker", "Worker - Operation level"),
                        ],
                        default="Worker",
                        max_length=9,
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webpage.address",
                    ),
                ),
                ("company", models.ManyToManyField(to="webpage.company")),
                (
                    "user_auth",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
