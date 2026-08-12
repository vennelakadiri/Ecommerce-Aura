import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, Category, SubCategory

print('=== DYNAMIC VERIFICATION ===')
print()

# Check all categories
print('All Categories in Database:')
for cat in Category.objects.all().order_by('name'):
    subcat_count = SubCategory.objects.filter(category=cat).count()
    product_count = Product.objects.filter(category=cat, is_active=True).count()
    print(f'- {cat.name} (slug: {cat.slug}): {subcat_count} subcategories, {product_count} products')
print()

# Check TOP BRANDS specifically
print('TOP BRANDS Category Verification:')
top_brands = Category.objects.filter(slug='top-brands').first()
if top_brands:
    print(f'Category: {top_brands.name} - EXISTS in database')
    subcats = SubCategory.objects.filter(category=top_brands).order_by('name')
    for subcat in subcats:
        products = Product.objects.filter(subcategory=subcat, is_active=True)
        print(f'  - {subcat.name}: {products.count()} products')
        for product in products:
            print(f'    * {product.name} - ${product.discount_price} (was ${product.price})')
else:
    print('TOP BRANDS category NOT found')
print()

# Sample verification of products with prices
print('Sample Products with Prices:')
sample_products = [
    'Japanese Cherry Blossom Body Lotion',
    'Vitamin C Face Wash', 
    'Multi-Groom Trimmer Kit'
]

for product_name in sample_products:
    product = Product.objects.filter(name=product_name).first()
    if product:
        print(f'Product: {product.name}')
        print(f'  - Price: ${product.price}')
        print(f'  - Discount Price: ${product.discount_price}')
        print(f'  - Category: {product.category.name}')
        print(f'  - Subcategory: {product.subcategory.name}')
        print(f'  - Brand: {product.brand.name if product.brand else "No Brand"}')
        print(f'  - SKU: {product.sku}')
        print(f'  - Is Active: {product.is_active}')
        print()
    else:
        print(f'Product "{product_name}" not found')
        print()

print('=== VERIFICATION COMPLETE ===')
