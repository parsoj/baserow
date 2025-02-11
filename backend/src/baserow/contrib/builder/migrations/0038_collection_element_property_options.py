# Generated by Django 4.2.13 on 2024-09-10 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("builder", "0037_recordselectorelement"),
    ]

    operations = [
        migrations.CreateModel(
            name="CollectionElementPropertyOptions",
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
                    "schema_property",
                    models.CharField(
                        help_text="The name of the property in the schema this option belongs to.",
                        max_length=225,
                    ),
                ),
                (
                    "searchable",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this element is searchable or not by visitors.",
                    ),
                ),
                (
                    "filterable",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this element is filterable or not by visitors.",
                    ),
                ),
                (
                    "sortable",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this element is sortable or not by visitors.",
                    ),
                ),
                (
                    "element",
                    models.ForeignKey(
                        help_text="The element this property option belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="property_options",
                        to="builder.element",
                    ),
                ),
            ],
            options={
                "unique_together": {("element", "schema_property")},
            },
        ),
    ]
