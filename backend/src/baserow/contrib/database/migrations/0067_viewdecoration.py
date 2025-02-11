# Generated by Django 3.2.12 on 2022-04-21 12:31

import django.db.models.deletion
from django.db import migrations, models

import baserow.core.mixins


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0066_airtableimportjob"),
    ]

    operations = [
        migrations.CreateModel(
            name="ViewDecoration",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        help_text=(
                            "The decorator type. This is then interpreted by "
                            "the frontend to display the decoration."
                        ),
                        max_length=255,
                    ),
                ),
                (
                    "value_provider_type",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text=(
                            "The value provider type that gives the value to "
                            "the decorator."
                        ),
                        max_length=255,
                    ),
                ),
                (
                    "value_provider_conf",
                    models.JSONField(
                        default=dict,
                        help_text="The configuration consumed by the value provider.",
                    ),
                ),
                (
                    "order",
                    models.SmallIntegerField(
                        default=32767,
                        help_text=(
                            "The position of the decorator has within the "
                            "view, lowest first. If there is another decorator "
                            "with the same order value then the decorator with "
                            "the lowest id must be shown first."
                        ),
                    ),
                ),
                (
                    "view",
                    models.ForeignKey(
                        help_text=(
                            "The view to which the decoration applies. Each view "
                            "can have his own decorations."
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        to="database.view",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
            bases=(baserow.core.mixins.OrderableMixin, models.Model),
        ),
    ]
