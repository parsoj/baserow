# Generated by Django 3.2.13 on 2022-11-28 09:06

from django.db import migrations


def delete_all_role_assignments(apps, schema_editor):
    RoleAssignment = apps.get_model("baserow_enterprise", "RoleAssignment")

    for role_assignment in RoleAssignment.objects.all():
        role_assignment.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("baserow_enterprise", "0007_teamsubject_baserow_ent_created_01fb9f_idx"),
    ]

    operations = [
        # We are deleting all duplicate role assignments here
        migrations.RunPython(delete_all_role_assignments, migrations.RunPython.noop),
    ]
