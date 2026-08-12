import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Get beauty category and brands
beauty_category = Category.objects.get(slug='beauty')
brands = list(Brand.objects.all())

# Beauty grooming tools subcategories to create
grooming_subcategories = [
    {'name': 'Hair Straightener', 'slug': 'hair-straightener'},
    {'name': 'Hair Dryer', 'slug': 'hair-dryer'},
    {'name': 'Epilator', 'slug': 'epilator'}
]

# Product data for each subcategory
grooming_products = {
    'hair-straightener': [
        {'name': 'Ceramic Hair Straightener', 'price': 1999, 'discount': 1499, 'description': 'Professional ceramic hair straightener with floating plates. Smooth, frizz-free styling.'},
        {'name': 'Ionic Hair Straightener', 'price': 2499, 'discount': 1999, 'description': 'Advanced ionic hair straightener for salon results. Reduces frizz and adds shine.'},
        {'name': 'Mini Travel Hair Straightener', 'price': 1299, 'discount': 999, 'description': 'Compact mini hair straightener for travel. Dual voltage for worldwide use.'},
        {'name': 'Digital Hair Straightener', 'price': 2999, 'discount': 2299, 'description': 'Digital temperature control hair straightener. Precise heat settings for all hair types.'}
    ],
    'hair-dryer': [
        {'name': 'Professional Hair Dryer', 'price': 2499, 'discount': 1999, 'description': 'Salon-quality hair dryer with ionic technology. Fast drying with reduced frizz.'},
        {'name': 'Lightweight Hair Dryer', 'price': 1999, 'discount': 1499, 'description': 'Ultra-lightweight hair dryer for comfortable styling. Powerful motor with ergonomic design.'},
        {'name': 'Cordless Hair Dryer', 'price': 3499, 'discount': 2799, 'description': 'Rechargeable cordless hair dryer for ultimate freedom. Portable and convenient.'},
        {'name': 'Tourmaline Hair Dryer', 'price': 2999, 'discount': 2299, 'description': 'Tourmaline-coated hair dryer for shiny hair. Negative ion technology for smooth results.'}
    ],
    'epilator': [
        {'name': 'Wet and Dry Epilator', 'price': 3999, 'discount': 3299, 'description': 'Versatile wet and dry epilator for gentle hair removal. Waterproof design for use in shower.'},
        {'name': 'Face Epilator', 'price': 1999, 'discount': 1499, 'description': 'Precision face epilator for facial hair removal. Gentle on sensitive skin.'},
        {'name': 'Body Epilator', 'price': 2999, 'discount': 2299, 'description': 'Full body epilator for smooth skin. Multiple attachments for different body areas.'},
        {'name': 'Cordless Epilator', 'price': 3499, 'discount': 2799, 'description': 'Rechargeable cordless epilator for convenience. Long battery life for complete sessions.'}
    ]
}

print("Creating Beauty grooming tools subcategories and products...")

# Create subcategories and products
for subcat_data in grooming_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=beauty_category,
        defaults={
            'name': subcat_name,
            'is_active': True
        }
    )
    
    if created:
        print(f"Created subcategory: {subcat_name}")
    else:
        print(f"Subcategory already exists: {subcat_name}")
    
    # Create products for this subcategory
    if subcat_slug in grooming_products:
        products_data = grooming_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=beauty_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='unisex',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"BEAUTY-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nBeauty grooming tools population completed!")
