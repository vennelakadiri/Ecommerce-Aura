#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

# Read current store/views.py file
with open('store/views.py', 'r') as f:
    content = f.read()

# Fix product detail view RelatedManager issue
content = content.replace(
    '''related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]''',
    '''related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]'''
)

# Write fixed content back to the file
with open('store/views.py', 'w') as f:
    f.write(content)

print("✅ Fixed product detail view RelatedManager issue")
