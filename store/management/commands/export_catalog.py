from io import StringIO

from django.core.management import call_command
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    help = 'Export store catalog fixture with UTF-8 encoding for Render deployment'

    def handle(self, *args, **options):
        fixture_path = Path('store/fixtures/catalog.json')
        fixture_path.parent.mkdir(parents=True, exist_ok=True)

        buffer = StringIO()
        call_command(
            'dumpdata',
            'store.Category',
            'store.SubCategory',
            'store.Brand',
            'store.Product',
            'store.ProductImage',
            'store.Banner',
            indent=2,
            stdout=buffer,
        )
        fixture_path.write_text(buffer.getvalue(), encoding='utf-8')
        self.stdout.write(self.style.SUCCESS(f'Exported catalog to {fixture_path}'))
