# Generated by Django 5.0.6 on 2024-06-09 08:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapphome", "0002_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="linkdin_link",
            field=models.URLField(max_length=100),
        ),
    ]
