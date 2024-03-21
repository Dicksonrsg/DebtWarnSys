# Generated by Django 4.2.10 on 2024-03-20 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

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
                ("number", models.CharField(max_length=7)),
                ("neighbourhood", models.CharField(max_length=60)),
                ("state", models.CharField(max_length=140)),
                ("country", models.CharField(max_length=14)),
                ("details", models.CharField(max_length=140)),
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
                ("cnpj", models.CharField(max_length=14)),
                (
                    "address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webpage.address",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
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
                ("cpf", models.CharField(max_length=11)),
                ("phone", models.CharField(max_length=14)),
                ("email", models.CharField(max_length=140)),
                ("role", models.CharField(max_length=70)),
                (
                    "address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webpage.address",
                    ),
                ),
                ("company", models.ManyToManyField(to="webpage.company")),
            ],
            options={
                "abstract": False,
            },
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
                ("cpf", models.CharField(max_length=11)),
                ("phone", models.CharField(max_length=14)),
                ("email", models.CharField(max_length=140)),
                ("active", models.BooleanField(default=True)),
                (
                    "address",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="webpage.address",
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
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("contract", models.CharField(max_length=70)),
                ("due_date", models.DateTimeField()),
                ("status", models.CharField(max_length=70)),
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
    ]