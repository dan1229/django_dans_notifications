# Generated by Django 4.0.4 on 2022-05-30 22:14

import uuid

import django.db.models.deletion
from django.db import migrations, models

import django_dans_notifications.models.notifications


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NotificationBasic",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_modified", models.DateTimeField(auto_now=True)),
                ("datetime_sent", models.DateTimeField(blank=True, null=True)),
                ("sent_successfully", models.BooleanField(default=False)),
                (
                    "sender",
                    models.CharField(
                        help_text="This should be the sending users email.",
                        max_length=300,
                    ),
                ),
                (
                    "recipients",
                    models.CharField(
                        help_text="Comma separated list of email recipients.",
                        max_length=900,
                    ),
                ),
                ("read", models.BooleanField(default=False)),
                ("message", models.CharField(max_length=600)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NotificationEmailTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_modified", models.DateTimeField(auto_now=True)),
                ("path", models.CharField(max_length=300)),
                ("nickname", models.CharField(max_length=300)),
            ],
            options={
                "abstract": False,
            },
            managers=[
                (
                    "objects",
                    django_dans_notifications.models.notifications.NotificationEmailTemplateManager(),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotificationPush",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_modified", models.DateTimeField(auto_now=True)),
                ("datetime_sent", models.DateTimeField(blank=True, null=True)),
                ("sent_successfully", models.BooleanField(default=False)),
                (
                    "sender",
                    models.CharField(
                        help_text="This should be the sending users email.",
                        max_length=300,
                    ),
                ),
                (
                    "recipients",
                    models.CharField(
                        help_text="Comma separated list of email recipients.",
                        max_length=900,
                    ),
                ),
                ("message", models.CharField(max_length=300)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NotificationEmail",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_modified", models.DateTimeField(auto_now=True)),
                ("datetime_sent", models.DateTimeField(blank=True, null=True)),
                ("sent_successfully", models.BooleanField(default=False)),
                (
                    "sender",
                    models.CharField(
                        help_text="This should be the sending users email.",
                        max_length=300,
                    ),
                ),
                (
                    "recipients",
                    models.CharField(
                        help_text="Comma separated list of email recipients.",
                        max_length=900,
                    ),
                ),
                ("subject", models.CharField(max_length=300)),
                ("context", models.JSONField(blank=True, null=True)),
                (
                    "template",
                    models.ForeignKey(
                        default=django_dans_notifications.models.notifications.get_default_template,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="template",
                        to="django_dans_notifications.notificationemailtemplate",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                (
                    "objects",
                    django_dans_notifications.models.notifications.NotificationEmailManager(),
                ),
            ],
        ),
    ]
