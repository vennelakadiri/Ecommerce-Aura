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

# Beauty fragrance subcategories to create
fragrance_subcategories = [
    {'name': 'Perfume', 'slug': 'perfume'},
    {'name': 'Deodorant', 'slug': 'deodorant'},
    {'name': 'Body Mist', 'slug': 'body-mist'}
]

# Product data for each subcategory
fragrance_products = {
    'perfume': [
        {'name': 'Floral Perfume', 'price': 1299, 'discount': 999, 'description': 'Elegant floral perfume with rose and jasmine notes. Sophisticated and feminine.'},
        {'name': 'Citrus Perfume', 'price': 999, 'discount': 799, 'description': 'Fresh citrus perfume with lemon and bergamot. Energizing and vibrant.'},
        {'name': 'Woody Perfume', 'price': 1499, 'discount': 1199, 'description': 'Rich woody perfume with sandalwood and cedar. Warm and masculine.'},
        {'name': 'Oriental Perfume', 'price': 1799, 'discount': 1399, 'description': 'Exotic oriental perfume with spices and vanilla. Mysterious and alluring.'}
    ],
    'deodorant': [
        {'name': 'Long-Lasting Deodorant', 'price': 299, 'discount': 199, 'description': '48-hour protection deodorant. Keeps you fresh all day.'},
        {'name': 'Antibacterial Deodorant', 'price': 349, 'discount': 249, 'description': 'Antibacterial deodorant with skin protection. Prevents odor-causing bacteria.'},
        {'name': 'Natural Deodorant', 'price': 399, 'discount': 299, 'description': 'Natural aluminum-free deodorant. Gentle on sensitive skin.'},
        {'name': 'Clinical Strength Deodorant', 'price': 449, 'discount': 349, 'description': 'Extra-strength clinical deodorant. Maximum sweat protection.'}
    ],
    'body-mist': [
        {'name': 'Refreshing Body Mist', 'price': 399, 'discount': 299, 'description': 'Cooling body mist with mint and cucumber. Instant refreshment.'},
        {'name': 'Romantic Body Mist', 'price': 449, 'discount': 349, 'description': 'Romantic body mist with rose petals. Soft and feminine fragrance.'},
        {'name': 'Energizing Body Mist', 'price': 349, 'discount': 249, 'description': 'Invigorating body mist with citrus fruits. Boosts energy and mood.'},
        {'name': 'Calming Body Mist', 'price': 399, 'discount': 299, 'description': 'Soothing body mist with lavender. Relaxing and stress-relieving.'}
    ]
}

print("Creating Beauty fragrance subcategories and products...")

# Create subcategories and products
for subcat_data in fragrance_subcategories:
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
    if subcat_slug in fragrance_products:
        products_data = fragrance_products[subcat_slug]
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

print("\nBeauty fragrance population completed!")
