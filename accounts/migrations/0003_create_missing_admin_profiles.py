from django.db import migrations


def create_missing_admin_profiles(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    AdminProfile = apps.get_model('accounts', 'AdminProfile')
    for user in User.objects.filter(role='admin'):
        AdminProfile.objects.get_or_create(
            user=user,
            defaults={'department': 'Management'},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_grant_admin_django_permissions'),
    ]

    operations = [
        migrations.RunPython(create_missing_admin_profiles, migrations.RunPython.noop),
    ]
