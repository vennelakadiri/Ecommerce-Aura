import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category

# Get the party wear subcategory
kids_category = Category.objects.get(slug='kids')
party_subcat = SubCategory.objects.filter(category=kids_category, slug='party-wear').first()

if party_subcat:
    # Get all products for this subcategory
    products = Product.objects.filter(subcategory=party_subcat, is_active=True).order_by('-created_at')
    
    print(f"Party Wear Subcategory Debug:")
    print(f"Total products: {products.count()}")
    print(f"Subcategory ID: {party_subcat.id}")
    print(f"Subcategory name: {party_subcat.name}")
    
    print("\nProducts (showing first 10):")
    for i, product in enumerate(products[:10]):
        print(f"  {i+1}. {product.name} (ID: {product.id})")
        print(f"     Created: {product.created_at}")
        print(f"     Is active: {product.is_active}")
        print(f"     Category: {product.category.name}")
        print(f"     Subcategory: {product.subcategory.name}")
        print()
    
    # Test the query that the view uses
    print("Testing view query:")
    view_products = Product.objects.filter(
        is_active=True,
        category__slug='kids',
        subcategory__slug='party-wear'
    ).order_by('-created_at')
    
    print(f"View query results: {view_products.count()}")
    for i, p in enumerate(view_products[:5]):
        print(f"  {i+1}. {p.name}")
else:
    print("Party wear subcategory not found")
