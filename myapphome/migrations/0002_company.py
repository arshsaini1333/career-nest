# Generated by Django 5.0.6 on 2024-06-09 07:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapphome", "0001_initial"),
    ]

    operations = [
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
                ("companyname", models.CharField(max_length=100)),
                ("hr_name", models.CharField(max_length=100)),
                ("hr_email_id", models.EmailField(max_length=254)),
                ("linkdin_link", models.CharField(max_length=100)),
            ],
        ),
    ]
