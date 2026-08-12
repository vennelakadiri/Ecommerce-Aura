import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category
from django.test import RequestFactory, Client
from store.views import products_view

# Test with Client (more realistic)
client = Client()

# Make a request to the products view
response = client.get('/store/products/?category=kids&subcategory=party-wear')

print(f"Response status: {response.status_code}")
print(f"Response content length: {len(response.content)}")

# Check if the response contains the girls products
content = response.content.decode('utf-8')
girls_products = ['Girls Evening Wear', 'Girls Formal Outfit', 'Girls Party Dress']

print("\nChecking for girls products in response:")
for product_name in girls_products:
    if product_name in content:
        print(f"  Found: {product_name}")
    else:
        print(f"  Missing: {product_name}")

# Also check for boys products to see what's actually being rendered
boys_products = ['Boys Formal Blazer', 'Boys Party Suit', 'Boys Dress Shirt Set']
print("\nChecking for boys products in response:")
for product_name in boys_products:
    if product_name in content:
        print(f"  Found: {product_name}")
    else:
        print(f"  Missing: {product_name}")

# Let's also check the products count in the response
if 'Products Found' in content:
    import re
    match = re.search(r'(\d+)\s+Products Found', content)
    if match:
        print(f"\nProducts count in response: {match.group(1)}")
