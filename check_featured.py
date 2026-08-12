#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Category

print('=== Checking Featured Categories in Database ===')
featured_categories = Category.objects.all()
print(f'Total categories: {featured_categories.count()}')
for cat in featured_categories:
    print(f'{cat.name} - {cat.slug} - Featured: {getattr(cat, "is_featured", False)}')
