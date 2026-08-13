import json
import os
import tempfile
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from store.models import Banner, Brand, Category, Product


class Command(BaseCommand):
    help = 'Load catalog fixture when the production database has no products'

    def handle(self, *args, **options):
        engine = settings.DATABASES['default']['ENGINE']
        self.stdout.write(f'Database engine: {engine}')

        if os.environ.get('RENDER') and not os.environ.get('DATABASE_URL'):
            self.stdout.write(
                self.style.WARNING(
                    'DATABASE_URL is not set. Using SQLite on Render; '
                    'link PostgreSQL for persistent production data.'
                )
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
        except IntegrityError:
            if Product.objects.exists():
                self.stdout.write('Catalog load raced with another worker; data is present.')
            else:
                raise CommandError('Catalog import failed due to a database integrity error.') from None
        except Exception as exc:
            if Product.objects.exists():
                self.stdout.write('Catalog load reported an error but products are present.')
            else:
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
