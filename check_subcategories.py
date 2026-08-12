import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import SubCategory, Category

kids_cat = Category.objects.get(slug='kids')
print('Kids subcategory slugs:')
for subcat in SubCategory.objects.filter(category=kids_cat).order_by('name'):
    print(f'- {subcat.name}: slug="{subcat.slug}"')
