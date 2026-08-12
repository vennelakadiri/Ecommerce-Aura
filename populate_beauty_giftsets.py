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

# Beauty gift sets subcategories to create
giftsets_subcategories = [
    {'name': 'Beauty Gift', 'slug': 'beauty-gift'},
    {'name': 'Makeup Kit', 'slug': 'makeup-kit'}
]

# Product data for each subcategory
giftsets_products = {
    'beauty-gift': [
        {'name': 'Luxury Skincare Gift Set', 'price': 1999, 'discount': 1499, 'description': 'Premium skincare gift set with moisturizer, serum, and face mask. Complete daily routine.'},
        {'name': 'Fragrance Gift Collection', 'price': 1499, 'discount': 1199, 'description': 'Elegant fragrance gift set with perfume and body mist. Perfect scent combination.'},
        {'name': 'Hair Care Gift Basket', 'price': 1299, 'discount': 999, 'description': 'Complete hair care gift set with shampoo, conditioner, and hair oil. Salon-quality products.'},
        {'name': 'Beauty Essentials Gift Box', 'price': 999, 'discount': 749, 'description': 'Essential beauty gift set with lip balm, hand cream, and body lotion. Daily care basics.'}
    ],
    'makeup-kit': [
        {'name': 'Professional Makeup Kit', 'price': 2999, 'discount': 2299, 'description': 'Complete professional makeup kit with all essentials. Perfect for makeup artists.'},
        {'name': 'Natural Makeup Set', 'price': 1999, 'discount': 1499, 'description': 'Natural look makeup kit with neutral tones. Everyday makeup essentials.'},
        {'name': 'Party Makeup Collection', 'price': 2499, 'discount': 1899, 'description': 'Glamorous party makeup kit with bold colors. Evening and special occasion looks.'},
        {'name': 'Travel Makeup Kit', 'price': 1499, 'discount': 1099, 'description': 'Compact travel makeup kit with mini sizes. Perfect for on-the-go beauty.'}
    ]
}

print("Creating Beauty gift sets subcategories and products...")

# Create subcategories and products
for subcat_data in giftsets_subcategories:
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
    if subcat_slug in giftsets_products:
        products_data = giftsets_products[subcat_slug]
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
                    gender='female',
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

print("\nBeauty gift sets population completed!")
