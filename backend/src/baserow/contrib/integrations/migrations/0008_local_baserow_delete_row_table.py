# Generated by Django 4.2.13 on 2024-07-15 14:18

import django.db.models.deletion
from django.db import migrations, models

import baserow.core.formula.field


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0088_remove_blacklistedtoken_user"),
        ("database", "0160_merge_20240715_1319"),
        ("integrations", "0007_field_mapping_enabled"),
    ]

    operations = [
        migrations.CreateModel(
            name="LocalBaserowDeleteRow",
            fields=[
                (
                    "service_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.service",
                    ),
                ),
                ("row_id", baserow.core.formula.field.FormulaField()),
                (
                    "table",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="database.table",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("core.service",),
        ),
    ]
