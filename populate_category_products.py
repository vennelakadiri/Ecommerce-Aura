#!/usr/bin/env python
import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, Category, SubCategory, Brand, ProductImage

print("=== Adding Products for Accessories and New Arrivals Categories ===")

# Sample product data for accessories
accessories_products = [
    {
        'name': 'Classic Leather Belt',
        'price': 899,
        'description': 'Genuine leather belt with classic buckle',
        'category': 'accessories',
        'subcategory': 'wallets-accessories',
        'brand': 'jack-jones',
        'gender': 'men'
    },
    {
        'name': 'Designer Sunglasses',
        'price': 1299,
        'description': 'UV protection designer sunglasses',
        'category': 'accessories',
        'subcategory': 'sunglasses-accessories',
        'brand': 'fastrack',
        'gender': 'unisex'
    },
    {
        'name': 'Premium Wallet',
        'price': 799,
        'description': 'Genuine leather bifold wallet',
        'category': 'accessories',
        'subcategory': 'wallets-accessories',
        'brand': 'puma',
        'gender': 'men'
    },
    {
        'name': 'Fashion Scarf',
        'price': 599,
        'description': 'Silk blend fashion scarf for all seasons',
        'category': 'women',
        'subcategory': 'scarves-women',
        'brand': 'vero-moda',
        'gender': 'women'
    }
]

# Sample product data for new arrivals
new_arrivals_products = [
    {
        'name': 'Summer Collection Dress',
        'price': 1899,
        'description': 'Trendy summer dress with floral print',
        'category': 'women',
        'subcategory': 'tops',
        'brand': 'only',
        'gender': 'women'
    },
    {
        'name': 'Smart Watch Pro',
        'price': 3999,
        'description': 'Latest smartwatch with health tracking',
        'category': 'accessories',
        'subcategory': 'watches-accessories',
        'brand': 'casio',
        'gender': 'unisex'
    },
    {
        'name': 'Casual Sneakers',
        'price': 2299,
        'description': 'Comfortable casual sneakers for everyday wear',
        'category': 'men',
        'subcategory': 'sneakers',
        'brand': 'adidas',
        'gender': 'men'
    },
    {
        'name': 'Handbag Collection',
        'price': 2499,
        'description': 'Stylish handbag with multiple compartments',
        'category': 'women',
        'subcategory': 'travel-bags-women',
        'brand': 'mango',
        'gender': 'women'
    }
]

# Sample image URLs
sample_images = [
    'https://picsum.photos/seed/product1/400/400.jpg',
    'https://picsum.photos/seed/product2/400/400.jpg',
    'https://picsum.photos/seed/product3/400/400.jpg',
    'https://picsum.photos/seed/product4/400/400.jpg'
]

def create_products(product_list, category_name):
    print(f"\nAdding products for {category_name}...")
    
    for i, product_data in enumerate(product_list):
        try:
            # Get category
            category = Category.objects.get(slug=product_data['category'])
            
            # Get subcategory
            subcategory = SubCategory.objects.get(category=category, slug=product_data['subcategory'])
            
            # Get brand
            brand = Brand.objects.get(slug=product_data['brand'])
            
            # Generate unique SKU and slug
            import uuid
            sku = f"{category.slug.upper()}-{uuid.uuid4().hex[:8].upper()}"
            slug = f"{product_data['name'].lower().replace(' ', '-').replace('/', '-').replace('.', '')}-{uuid.uuid4().hex[:4]}"
            
            # Create product
            product = Product.objects.create(
                name=product_data['name'],
                slug=slug,
                description=product_data['description'],
                price=product_data['price'],
                category=category,
                subcategory=subcategory,
                brand=brand,
                gender=product_data['gender'],
                is_active=True,
                stock_quantity=random.randint(10, 50),
                sku=sku
            )
            
            # Add product image
            ProductImage.objects.create(
                product=product,
                image=sample_images[i % len(sample_images)],
                alt_text=product.name
            )
            
            print(f"  - Created: {product.name} (${product_data['price']})")
            
        except Exception as e:
            print(f"  - Error creating {product_data['name']}: {e}")

# Create products for both categories
create_products(accessories_products, "Accessories")
create_products(new_arrivals_products, "New Arrivals")

print("\n=== Product creation completed! ===")
