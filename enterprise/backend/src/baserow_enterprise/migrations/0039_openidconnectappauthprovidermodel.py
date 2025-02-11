# Generated by Django 5.0.9 on 2025-01-14 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("baserow_enterprise", "0038_localbaserowgroupedaggregaterows_and_more"),
        ("core", "0093_alter_appauthprovider_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OpenIdConnectAppAuthProviderModel",
            fields=[
                (
                    "appauthprovider_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.appauthprovider",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "base_url",
                    models.URLField(help_text="Base URL of the authorization server"),
                ),
                (
                    "client_id",
                    models.CharField(
                        help_text="App ID, or consumer key", max_length=191
                    ),
                ),
                (
                    "secret",
                    models.CharField(
                        help_text="API secret, client secret, or consumer secret",
                        max_length=191,
                    ),
                ),
                (
                    "authorization_url",
                    models.URLField(help_text="URL to initiate auth flow"),
                ),
                (
                    "access_token_url",
                    models.URLField(help_text="URL to obtain access token"),
                ),
                ("user_info_url", models.URLField(help_text="URL to get user info")),
            ],
            options={
                "abstract": False,
            },
            bases=("core.appauthprovider", models.Model),
        ),
    ]
