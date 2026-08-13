from django.db import migrations


def grant_admin_django_permissions(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.filter(role='admin').update(is_staff=True, is_superuser=True)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(grant_admin_django_permissions, migrations.RunPython.noop),
    ]
