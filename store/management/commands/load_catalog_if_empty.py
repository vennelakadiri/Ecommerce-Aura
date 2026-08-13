import json
from pathlib import Path

from django.core import serializers
from django.core.management.base import BaseCommand

from store.models import Banner, Product


class Command(BaseCommand):
    help = 'Load catalog fixture when the production database has no products'

    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write('Catalog already present; skipping fixture load.')
            return

        fixture_path = Path('store/fixtures/catalog.json')
        if not fixture_path.exists():
            self.stderr.write(self.style.ERROR(f'Fixture not found: {fixture_path}'))
            return

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
            self.stdout.write('No catalog records to load.')
            return

        loaded = 0
        for obj in serializers.deserialize('json', json.dumps(fixture_objects)):
            obj.save()
            loaded += 1

        self.stdout.write(self.style.SUCCESS(f'Catalog loaded successfully ({loaded} objects).'))
