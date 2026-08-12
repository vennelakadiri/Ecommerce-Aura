import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Get home category and brands
home_category = Category.objects.get(slug='home')
brands = list(Brand.objects.all())

# Home floor covering subcategories to create
floor_subcategories = [
    {'name': 'Floor Runners', 'slug': 'floor-runners'},
    {'name': 'Carpets', 'slug': 'carpets'},
    {'name': 'Floor Mats & Dhurries', 'slug': 'floor-mats-dhurries'},
    {'name': 'Door Mats', 'slug': 'door-mats'}
]

# Product data for each subcategory
floor_products = {
    'floor-runners': [
        {'name': 'Modern Floor Runner', 'price': 1299, 'discount': 999, 'description': 'Stylish modern floor runner for hallways and corridors. Durable and easy to clean.'},
        {'name': 'Traditional Floor Runner', 'price': 1599, 'discount': 1199, 'description': 'Elegant traditional floor runner with classic patterns. Perfect for entryways.'},
        {'name': 'Printed Floor Runner', 'price': 999, 'discount': 749, 'description': 'Colorful printed floor runner for living spaces. Adds vibrancy to any room.'},
        {'name': 'Luxury Floor Runner', 'price': 1899, 'discount': 1499, 'description': 'Premium luxury floor runner with high-quality materials. Sophisticated home decor.'}
    ],
    'carpets': [
        {'name': 'Living Room Carpet', 'price': 3999, 'discount': 2999, 'description': 'Spacious living room carpet for comfort and style. Soft and plush underfoot.'},
        {'name': 'Bedroom Carpet', 'price': 3499, 'discount': 2599, 'description': 'Cozy bedroom carpet for warm and comfortable mornings. Perfect size for bedrooms.'},
        {'name': 'Modern Area Carpet', 'price': 2999, 'discount': 2299, 'description': 'Contemporary area carpet for any room. Modern design with neutral colors.'},
        {'name': 'Traditional Persian Carpet', 'price': 4999, 'discount': 3999, 'description': 'Authentic Persian-style carpet with intricate patterns. Timeless elegance.'}
    ],
    'floor-mats-dhurries': [
        {'name': 'Cotton Floor Mat', 'price': 699, 'discount': 549, 'description': 'Soft cotton floor mat for bedrooms and living areas. Breathable and comfortable.'},
        {'name': 'Traditional Dhurrie', 'price': 1299, 'discount': 999, 'description': 'Classic handwoven dhurrie with ethnic patterns. Traditional Indian craftsmanship.'},
        {'name': 'Modern Floor Mat', 'price': 899, 'discount': 699, 'description': 'Contemporary floor mat with geometric designs. Perfect for modern homes.'},
        {'name': 'Jute Floor Mat', 'price': 799, 'discount': 649, 'description': 'Eco-friendly jute floor mat. Natural fibers for sustainable home decor.'}
    ],
    'door-mats': [
        {'name': 'Welcome Door Mat', 'price': 399, 'discount': 299, 'description': 'Classic welcome door mat for entryways. Durable and weather-resistant.'},
        {'name': 'Coir Door Mat', 'price': 449, 'discount': 349, 'description': 'Natural coir door mat for effective dirt cleaning. Eco-friendly material.'},
        {'name': 'Printed Door Mat', 'price': 499, 'discount': 399, 'description': 'Decorative printed door mat with colorful designs. Adds charm to entrances.'},
        {'name': 'Heavy Duty Door Mat', 'price': 599, 'discount': 449, 'description': 'Commercial-grade heavy duty door mat. Maximum durability for high traffic areas.'}
    ]
}

print("Creating Home floor covering subcategories and products...")

# Create subcategories and products
for subcat_data in floor_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=home_category,
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
    if subcat_slug in floor_products:
        products_data = floor_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=home_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='unisex',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"HOME-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nHome floor covering population completed!")
