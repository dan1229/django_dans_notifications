# Generated by Django 4.0.4 on 2022-07-05 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("django_dans_notifications", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notificationemailtemplate",
            options={"ordering": ["datetime_created"]},
        ),
    ]