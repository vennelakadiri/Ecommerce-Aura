import os


def bootstrap_render_database():
    """Ensure migrations and catalog data exist when running on Render."""
    if not os.environ.get('RENDER'):
        return

    if os.environ.get('AURA_DB_BOOTSTRAPPED') == '1':
        return

    from django.core.management import call_command
    from store.models import Product

    call_command('migrate', '--no-input', verbosity=0)

    if not Product.objects.exists():
        call_command('load_catalog_if_empty', verbosity=1)
    else:
        call_command('load_catalog_if_empty', verbosity=0)

    os.environ['AURA_DB_BOOTSTRAPPED'] = '1'
