import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, Category, Brand, SubCategory

# Get kids category
kids_category = Category.objects.get(slug='kids')

# Brands to create/update
brands_to_create = [
    {'name': 'Max Kids', 'slug': 'max-kids'},
    {'name': 'United Colors Of Benetton', 'slug': 'benetton'},
    {'name': 'YK', 'slug': 'yk'},
    {'name': 'U.S. Polo Assn. Kids', 'slug': 'uspa-kids'}
]

# Create missing brands
for brand_data in brands_to_create:
    brand, created = Brand.objects.get_or_create(
        slug=brand_data['slug'],
        defaults={
            'name': brand_data['name'],
            'is_active': True
        }
    )
    if created:
        print(f"Created brand: {brand.name}")
    else:
        print(f"Brand already exists: {brand.name}")

# Get all relevant brands
all_brands = Brand.objects.filter(slug__in=['max-kids', 'pantaloons', 'benetton', 'yk', 'uspa-kids', 'mothercare', 'hrx'])

# Product data for each brand
brand_products = {
    'max-kids': [
        {'name': 'Max Kids Boys T-Shirt', 'price': 599, 'discount': 449, 'description': 'Stylish boys t-shirt from Max Kids. Comfortable cotton fabric with modern design.'},
        {'name': 'Max Kids Girls Dress', 'price': 899, 'discount': 699, 'description': 'Beautiful girls dress from Max Kids. Perfect for parties and special occasions.'},
        {'name': 'Max Kids Boys Shorts', 'price': 699, 'discount': 549, 'description': 'Comfortable shorts for boys from Max Kids. Ideal for summer and casual wear.'},
        {'name': 'Max Kids Girls Top', 'price': 549, 'discount': 399, 'description': 'Cute girls top from Max Kids. Colorful design with comfortable fit.'}
    ],
    'pantaloons': [
        {'name': 'Pantaloons Boys T-Shirt', 'price': 699, 'discount': 549, 'description': 'Casual boys t-shirt from Pantaloons. Premium cotton with trendy prints.'},
        {'name': 'Pantaloons Girls Skirt', 'price': 799, 'discount': 649, 'description': 'Stylish girls skirt from Pantaloons. Perfect for school and casual outings.'},
        {'name': 'Pantaloons Boys Jeans', 'price': 1299, 'discount': 999, 'description': 'Durable boys jeans from Pantaloons. Comfortable fit with modern styling.'},
        {'name': 'Pantaloons Girls Dress', 'price': 1199, 'discount': 899, 'description': 'Elegant girls dress from Pantaloons. Beautiful design for special occasions.'}
    ],
    'benetton': [
        {'name': 'Benetton Boys Polo Shirt', 'price': 999, 'discount': 799, 'description': 'Classic polo shirt for boys from Benetton. Premium quality with elegant design.'},
        {'name': 'Benetton Girls T-Shirt', 'price': 899, 'discount': 699, 'description': 'Fashionable girls t-shirt from Benetton. Modern design with comfortable fit.'},
        {'name': 'Benetton Boys Shorts', 'price': 899, 'discount': 699, 'description': 'Stylish shorts for boys from Benetton. Perfect for summer activities.'},
        {'name': 'Benetton Girls Dress', 'price': 1399, 'discount': 1099, 'description': 'Sophisticated girls dress from Benetton. Premium fabric and elegant design.'}
    ],
    'yk': [
        {'name': 'YK Boys Casual Shirt', 'price': 899, 'discount': 699, 'description': 'Trendy casual shirt for boys from YK. Modern design with comfortable fit.'},
        {'name': 'YK Girls Top', 'price': 699, 'discount': 549, 'description': 'Stylish girls top from YK. Fashionable design perfect for casual wear.'},
        {'name': 'YK Boys Track Pants', 'price': 799, 'discount': 649, 'description': 'Comfortable track pants for boys from YK. Ideal for sports and casual wear.'},
        {'name': 'YK Girls Skirt', 'price': 749, 'discount': 599, 'description': 'Cute girls skirt from YK. Perfect for school and playtime.'}
    ],
    'uspa-kids': [
        {'name': 'USPA Kids Boys T-Shirt', 'price': 799, 'discount': 649, 'description': 'Premium boys t-shirt from USPA Kids. Classic design with superior quality.'},
        {'name': 'USPA Kids Girls Dress', 'price': 1299, 'discount': 999, 'description': 'Elegant girls dress from USPA Kids. Perfect for parties and special events.'},
        {'name': 'USPA Kids Boys Shorts', 'price': 899, 'discount': 699, 'description': 'Stylish shorts for boys from USPA Kids. Premium fabric and comfortable fit.'},
        {'name': 'USPA Kids Girls Top', 'price': 799, 'discount': 649, 'description': 'Fashionable girls top from USPA Kids. Modern design with elegant styling.'}
    ],
    'mothercare': [
        {'name': 'Mothercare Baby Bodysuit', 'price': 499, 'discount': 399, 'description': 'Soft bodysuit for babies from Mothercare. Gentle on sensitive skin.'},
        {'name': 'Mothercare Infant Sleepsuit', 'price': 699, 'discount': 549, 'description': 'Cozy sleepsuit for infants from Mothercare. Ensures comfortable sleep.'},
        {'name': 'Mothercare Baby Romper', 'price': 799, 'discount': 649, 'description': 'Cute romper for babies from Mothercare. Easy to wear and change.'},
        {'name': 'Mothercare Infant Gift Set', 'price': 1499, 'discount': 1199, 'description': 'Complete gift set for infants from Mothercare. Essential items for newborns.'}
    ],
    'hrx': [
        {'name': 'HRX Boys Sports T-Shirt', 'price': 899, 'discount': 699, 'description': 'Performance sports t-shirt for boys from HRX. Moisture-wicking fabric.'},
        {'name': 'HRX Girls Active Wear Top', 'price': 799, 'discount': 649, 'description': 'Active wear top for girls from HRX. Perfect for sports and fitness.'},
        {'name': 'HRX Boys Track Pants', 'price': 999, 'discount': 799, 'description': 'Athletic track pants for boys from HRX. Designed for performance and comfort.'},
        {'name': 'HRX Girls Sports Shorts', 'price': 749, 'discount': 599, 'description': 'Sports shorts for girls from HRX. Ideal for workouts and activities.'}
    ]
}

# Get existing subcategories to assign products to
subcategories = list(SubCategory.objects.filter(category=kids_category, is_active=True))

print("Creating brand-specific kids products...")

for brand in all_brands:
    if brand.slug in brand_products:
        products_data = brand_products[brand.slug]
        print(f"\nCreating products for {brand.name}:")
        
        for product_data in products_data:
            # Check if product already exists
            existing = Product.objects.filter(name=product_data['name'], brand=brand).first()
            if not existing:
                # Assign to a relevant subcategory
                subcategory = random.choice(subcategories)
                
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=kids_category,
                    subcategory=subcategory,
                    brand=brand,
                    gender='kids',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"KIDS-{brand.slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"  Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"  Already exists: {product_data['name']}")

print("\nBrand-specific kids products population completed!")
