import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Get kids category and brands
kids_category = Category.objects.get(slug='kids')
brands = list(Brand.objects.all())

# Kids accessories subcategories to create
accessories_subcategories = [
    {'name': 'Bags & Backpacks', 'slug': 'kids-bags-backpacks'},
    {'name': 'Watches', 'slug': 'kids-watches'},
    {'name': 'Jewellery & Hair accessory', 'slug': 'kids-jewellery-hair-accessory'},
    {'name': 'Sunglasses', 'slug': 'kids-sunglasses'},
    {'name': 'Masks & Protective Gears', 'slug': 'kids-masks-protective-gears'},
    {'name': 'Caps & Hats', 'slug': 'kids-caps-hats'}
]

# Product data for each subcategory
accessories_products = {
    'kids-bags-backpacks': [
        {'name': 'Kids School Backpack', 'price': 899, 'discount': 699, 'description': 'Durable school backpack for kids. Multiple compartments for books and supplies.'},
        {'name': 'Kids Cartoon Backpack', 'price': 999, 'discount': 799, 'description': 'Fun cartoon-themed backpack with popular characters. Makes school exciting for kids.'},
        {'name': 'Kids Sports Bag', 'price': 799, 'discount': 599, 'description': 'Lightweight sports bag for gym and activities. Easy to carry and clean.'},
        {'name': 'Kids Lunch Bag Set', 'price': 699, 'discount': 499, 'description': 'Insulated lunch bag with water bottle. Keeps food fresh and cool for hours.'}
    ],
    'kids-watches': [
        {'name': 'Kids Digital Watch', 'price': 799, 'discount': 599, 'description': 'Colorful digital watch with time and date display. Easy to read for young learners.'},
        {'name': 'Kids Analog Watch', 'price': 999, 'discount': 799, 'description': 'Educational analog watch for learning time. Clear numbers and hands for practice.'},
        {'name': 'Kids Smart Watch', 'price': 1299, 'discount': 999, 'description': 'Kids smart watch with games and fitness tracking. Fun and educational features.'},
        {'name': 'Kids Cartoon Watch', 'price': 699, 'discount': 499, 'description': 'Character-themed watch with fun designs. Makes time-telling exciting for kids.'}
    ],
    'kids-jewellery-hair-accessory': [
        {'name': 'Kids Hair Clips Set', 'price': 399, 'discount': 299, 'description': 'Colorful hair clips set of 12. Various shapes and sizes for different hairstyles.'},
        {'name': 'Kids Hair Bands Pack', 'price': 449, 'discount': 349, 'description': 'Soft hair bands pack of 6. Comfortable and gentle on hair for all-day wear.'},
        {'name': 'Kids Bracelet Set', 'price': 599, 'discount': 449, 'description': 'Fun bracelet set with charms. Safe and adjustable for kids wrists.'},
        {'name': 'Kids Necklace Set', 'price': 699, 'discount': 549, 'description': 'Cute necklace set with pendants. Child-safe materials and designs.'}
    ],
    'kids-sunglasses': [
        {'name': 'Kids UV Protection Sunglasses', 'price': 599, 'discount': 449, 'description': 'UV protection sunglasses for kids. Polarized lenses for eye safety.'},
        {'name': 'Kids Sports Sunglasses', 'price': 699, 'discount': 549, 'description': 'Durable sports sunglasses for active kids. Wrap-around design for full coverage.'},
        {'name': 'Kids Cartoon Sunglasses', 'price': 499, 'discount': 349, 'description': 'Fun cartoon-themed sunglasses. Makes sun protection exciting for kids.'},
        {'name': 'Kids Fashion Sunglasses', 'price': 799, 'discount': 599, 'description': 'Stylish fashion sunglasses for kids. Trendy designs with UV protection.'}
    ],
    'kids-masks-protective-gears': [
        {'name': 'Kids Face Masks Pack', 'price': 299, 'discount': 199, 'description': 'Pack of 10 reusable face masks. Comfortable and breathable for kids.'},
        {'name': 'Kids Protective Helmet', 'price': 999, 'discount': 799, 'description': 'Safety helmet for cycling and sports. Adjustable straps for secure fit.'},
        {'name': 'Kids Knee & Elbow Pads', 'price': 799, 'discount': 599, 'description': 'Protective knee and elbow pads set. Essential for skating and outdoor activities.'},
        {'name': 'Kids Safety Goggles', 'price': 499, 'discount': 349, 'description': 'Protective safety goggles for science and sports. Anti-fog and scratch-resistant.'}
    ],
    'kids-caps-hats': [
        {'name': 'Kids Baseball Cap', 'price': 499, 'discount': 349, 'description': 'Classic baseball cap for kids. Adjustable strap for perfect fit.'},
        {'name': 'Kids Sun Hat', 'price': 599, 'discount': 449, 'description': 'Wide-brim sun hat for UV protection. Lightweight and breathable for summer.'},
        {'name': 'Kids Winter Hat', 'price': 699, 'discount': 549, 'description': 'Warm winter hat with fleece lining. Keeps kids cozy in cold weather.'},
        {'name': 'Kids Cartoon Cap', 'price': 449, 'discount': 349, 'description': 'Fun cartoon-themed cap with favorite characters. Makes sun protection fun.'}
    ]
}

print("Creating kids accessories subcategories and products...")

# Create subcategories and products
for subcat_data in accessories_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=kids_category,
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
    if subcat_slug in accessories_products:
        products_data = accessories_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=kids_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='kids',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"KIDS-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nKids accessories population completed!")
