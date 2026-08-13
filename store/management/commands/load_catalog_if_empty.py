import json
import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from store.models import Banner, Brand, Category, Product


class Command(BaseCommand):
    help = 'Load catalog fixture when the production database has no products'

    def handle(self, *args, **options):
        engine = settings.DATABASES['default']['ENGINE']
        self.stdout.write(f'Database engine: {engine}')

        if os.environ.get('RENDER') and not os.environ.get('DATABASE_URL'):
            raise CommandError(
                'DATABASE_URL is not set on Render. '
                'Link a PostgreSQL database to this service so catalog data persists.'
            )

        if Product.objects.exists():
            self._report_counts('Catalog already present; skipping fixture load.')
            return

        fixture_path = Path('store/fixtures/catalog.json')
        if not fixture_path.exists():
            raise CommandError(f'Fixture not found: {fixture_path.resolve()}')

        self.stdout.write(f'Loading catalog from {fixture_path}...')

        fixture_objects = json.loads(fixture_path.read_text(encoding='utf-8'))
        if Banner.objects.exists():
            before = len(fixture_objects)
            fixture_objects = [
                obj for obj in fixture_objects if obj.get('model') != 'store.banner'
            ]
            skipped = before - len(fixture_objects)
            if skipped:
                self.stdout.write(
                    f'Existing banners detected; skipping {skipped} banner record(s).'
                )

        if not fixture_objects:
            raise CommandError('No catalog records available to load.')

        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            suffix='.json',
            delete=False,
        ) as temp_fixture:
            json.dump(fixture_objects, temp_fixture)
            temp_fixture_path = temp_fixture.name

        try:
            call_command('loaddata', temp_fixture_path, verbosity=1)
        except Exception as exc:
            raise CommandError(f'Catalog import failed: {exc}') from exc
        finally:
            Path(temp_fixture_path).unlink(missing_ok=True)

        if not Product.objects.exists():
            raise CommandError('Catalog import finished but no products were created.')

        self._report_counts(self.style.SUCCESS('Catalog loaded successfully.'))

    def _report_counts(self, message):
        self.stdout.write(message)
        self.stdout.write(
            f'Counts -> products: {Product.objects.count()}, '
            f'active products: {Product.objects.filter(is_active=True).count()}, '
            f'categories: {Category.objects.count()}, '
            f'brands: {Brand.objects.count()}'
        )
