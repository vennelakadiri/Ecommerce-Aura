#!/usr/bin/env python
import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage, Category, SubCategory, Brand

# Create media/products directory if it doesn't exist
media_products_dir = os.path.join('media', 'products')
if not os.path.exists(media_products_dir):
    os.makedirs(media_products_dir, exist_ok=True)

print("=== Creating Men's Ethnic Wear Products ===")

# Get or create Men's category and subcategories
men_category = Category.objects.get(name='Men')
kurtas_subcat = SubCategory.objects.get(name='Kurtas & Kurta Sets', category=men_category)
sherwanis_subcat = SubCategory.objects.get(name='Sherwanis', category=men_category)
nehru_subcat = SubCategory.objects.get(name='Nehru Jackets', category=men_category)
dhotis_subcat = SubCategory.objects.get(name='Dhotis', category=men_category)

# Get or create a brand for ethnic wear
ethnic_brand, created = Brand.objects.get_or_create(
    name='Ethnic Wear',
    slug='ethnic-wear',
    defaults={'is_active': True}
)

# Ethnic wear products to create
ethnic_products = [
    {
        'name': 'Traditional White Kurta',
        'slug': 'traditional-white-kurta',
        'subcategory': kurtas_subcat,
        'price': 1299.00,
        'image': 'temp_image_140.jpg',
        'description': 'Classic white kurta with traditional embroidery'
    },
    {
        'name': 'Designer Sherwani',
        'slug': 'designer-sherwani',
        'subcategory': sherwanis_subcat,
        'price': 2499.00,
        'image': 'temp_image_141.jpg',
        'description': 'Elegant designer sherwani for special occasions'
    },
    {
        'name': 'Nehru Jacket',
        'slug': 'nehru-jacket',
        'subcategory': nehru_subcat,
        'price': 1899.00,
        'image': 'temp_image_142.jpg',
        'description': 'Classic nehru jacket with button closure'
    },
    {
        'name': 'Traditional Dhoti',
        'slug': 'traditional-dhoti',
        'subcategory': dhotis_subcat,
        'price': 899.00,
        'image': 'temp_image_143.jpg',
        'description': 'Traditional cotton dhoti with matching border'
    },
]

for product_data in ethnic_products:
    # Create product
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        slug=product_data['slug'],
        category=men_category,
        subcategory=product_data['subcategory'],
        brand=ethnic_brand,
        defaults={
            'price': product_data['price'],
            'description': product_data['description'],
            'is_active': True
        }
    )
    
    if created:
        # Add image
        image_filename = product_data['image']
        source_path = os.path.join(os.getcwd(), image_filename)
        
        if os.path.exists(source_path):
            product_image_name = f"{product.slug}_{image_filename}"
            dest_path = os.path.join(media_products_dir, product_image_name)
            
            # Copy image to media folder
            import shutil
            shutil.copy2(source_path, dest_path)
            
            # Create product image record
            with open(dest_path, 'rb') as f:
                ProductImage.objects.create(
                    product=product,
                    image=File(f, name=product_image_name)
                )
            
            print(f"Created: {product.name}")
            print(f"  Image: {image_filename}")
            print(f"  Price: ${product_data['price']}")
        else:
            print(f"Image not found: {image_filename}")
    else:
        print(f"Already exists: {product.name}")

print("=== Men's Ethnic Wear Products Created ===")
