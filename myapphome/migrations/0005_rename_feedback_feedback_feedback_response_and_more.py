# Generated by Django 5.0.6 on 2024-06-12 15:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("myapphome", "0004_feedback_alter_company_linkdin_link"),
    ]

    operations = [
        migrations.RenameField(
            model_name="feedback",
            old_name="feedback",
            new_name="Feedback_response",
        ),
        migrations.RenameField(
            model_name="feedback",
            old_name="email",
            new_name="email_of_feedbacker",
        ),
        migrations.RenameField(
            model_name="feedback",
            old_name="name",
            new_name="name_of_feedbacker",
        ),
    ]
