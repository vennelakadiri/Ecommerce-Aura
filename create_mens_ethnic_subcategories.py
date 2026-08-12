#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Category, SubCategory

print("=== Creating Men's Ethnic Wear Subcategories ===")

# Get or create Men's category
men_category, created = Category.objects.get_or_create(
    name='Men',
    defaults={'is_active': True, 'slug': 'men'}
)

# Create Indian ethnic wear subcategories
ethnic_subcategories = [
    ('kurtas', 'Kurtas & Kurta Sets'),
    ('sherwanis', 'Sherwanis'),
    ('nehru-jackets', 'Nehru Jackets'),
    ('dhotis', 'Dhotis'),
]

for slug, name in ethnic_subcategories:
    subcat, created = SubCategory.objects.get_or_create(
        name=name,
        slug=slug,
        category=men_category,
        defaults={'is_active': True}
    )
    if created:
        print(f"Created: {name}")
    else:
        print(f"Already exists: {name}")

print("\n=== Men's Ethnic Wear Subcategories Created ===")
