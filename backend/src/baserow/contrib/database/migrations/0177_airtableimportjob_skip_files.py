# Generated by Django 5.0.9 on 2025-01-27 20:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0176_try_regexp_replace"),
    ]

    operations = [
        migrations.AddField(
            model_name="airtableimportjob",
            name="skip_files",
            field=models.BooleanField(
                db_default=False,
                default=False,
                help_text="If true, then the files are not downloaded and imported.",
            ),
        ),
    ]
