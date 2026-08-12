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

# Footwear subcategories to create
footwear_subcategories = [
    {'name': 'Kids Casual Shoes', 'slug': 'kids-casual-shoes'},
    {'name': 'Kids Flipflops', 'slug': 'kids-flipflops'},
    {'name': 'Kids Sports Shoes', 'slug': 'kids-sports-shoes'},
    {'name': 'Kids Flats', 'slug': 'kids-flats'},
    {'name': 'Kids Sandals', 'slug': 'kids-sandals'},
    {'name': 'Kids Heels', 'slug': 'kids-heels'},
    {'name': 'Kids School Shoes', 'slug': 'kids-school-shoes'},
    {'name': 'Kids Socks', 'slug': 'kids-socks'}
]

# Product data for each subcategory
footwear_products = {
    'kids-casual-shoes': [
        {'name': 'Kids Canvas Sneakers', 'price': 899, 'discount': 699, 'description': 'Comfortable canvas sneakers for everyday wear. Perfect for school and play.'},
        {'name': 'Kids Loafers', 'price': 1299, 'discount': 999, 'description': 'Stylish loafers for kids. Easy to wear and comfortable for all-day use.'},
        {'name': 'Kids Boat Shoes', 'price': 1499, 'discount': 1199, 'description': 'Classic boat shoes for kids. Great for casual outings and family gatherings.'},
        {'name': 'Kids Slip-on Shoes', 'price': 799, 'discount': 599, 'description': 'Convenient slip-on shoes for kids. Easy to put on and take off independently.'}
    ],
    'kids-flipflops': [
        {'name': 'Kids Beach Flipflops', 'price': 399, 'discount': 299, 'description': 'Colorful beach flipflops for kids. Water-resistant and perfect for summer fun.'},
        {'name': 'Kids Pool Flipflops', 'price': 499, 'discount': 399, 'description': 'Quick-drying pool flipflops. Non-slip sole for safety around water.'},
        {'name': 'Kids Garden Flipflops', 'price': 449, 'discount': 349, 'description': 'Durable garden flipflops for kids. Comfortable for outdoor activities.'},
        {'name': 'Kids Cartoon Flipflops', 'price': 599, 'discount': 449, 'description': 'Fun cartoon-themed flipflops. Features popular characters kids love.'}
    ],
    'kids-sports-shoes': [
        {'name': 'Kids Running Shoes', 'price': 1899, 'discount': 1499, 'description': 'Professional running shoes for kids. Excellent support and cushioning for active children.'},
        {'name': 'Kids Basketball Shoes', 'price': 2299, 'discount': 1799, 'description': 'High-performance basketball shoes. Great ankle support and grip for court sports.'},
        {'name': 'Kids Soccer Shoes', 'price': 1599, 'discount': 1199, 'description': 'Soccer cleats for kids. Designed for optimal traction on grass fields.'},
        {'name': 'Kids Training Shoes', 'price': 1399, 'discount': 999, 'description': 'Versatile training shoes for kids. Perfect for gym class and sports activities.'}
    ],
    'kids-flats': [
        {'name': 'Girls Ballet Flats', 'price': 899, 'discount': 699, 'description': 'Elegant ballet flats for girls. Comfortable and stylish for school and special occasions.'},
        {'name': 'Girls Mary Jane Flats', 'price': 999, 'discount': 799, 'description': 'Classic Mary Jane flats with strap. Traditional style with modern comfort.'},
        {'name': 'Girls Patent Flats', 'price': 1199, 'discount': 899, 'description': 'Shiny patent leather flats. Perfect for parties and formal events.'},
        {'name': 'Girls Canvas Flats', 'price': 799, 'discount': 599, 'description': 'Lightweight canvas flats. Breathable and comfortable for everyday wear.'}
    ],
    'kids-sandals': [
        {'name': 'Kids Sports Sandals', 'price': 999, 'discount': 799, 'description': 'Active sports sandals with straps. Great for hiking and outdoor adventures.'},
        {'name': 'Kids Summer Sandals', 'price': 899, 'discount': 699, 'description': 'Breathable summer sandals. Keeps feet cool and comfortable in hot weather.'},
        {'name': 'Kids Leather Sandals', 'price': 1299, 'discount': 999, 'description': 'Premium leather sandals. Durable and stylish for all-day wear.'},
        {'name': 'Kids Water Sandals', 'price': 1099, 'discount': 899, 'description': 'Water-friendly sandals for beach and pool activities. Quick-drying material.'}
    ],
    'kids-heels': [
        {'name': 'Girls Party Heels', 'price': 1599, 'discount': 1199, 'description': 'Elegant party heels for girls. Low heel design for special occasions.'},
        {'name': 'Girls Wedge Heels', 'price': 1799, 'discount': 1399, 'description': 'Comfortable wedge heels. Stylish yet stable for growing feet.'},
        {'name': 'Girls Dress Heels', 'price': 1999, 'discount': 1499, 'description': 'Formal dress heels for special events. Sophisticated design for young ladies.'},
        {'name': 'Girls Block Heels', 'price': 1699, 'discount': 1299, 'description': 'Stable block heel design. Comfortable and safe for beginners to heels.'}
    ],
    'kids-school-shoes': [
        {'name': 'Kids School Uniform Shoes', 'price': 1299, 'discount': 999, 'description': 'Durable uniform shoes for school. Built to withstand daily wear and tear.'},
        {'name': 'Kids Black School Shoes', 'price': 1199, 'discount': 899, 'description': 'Classic black school shoes. Formal design meets comfort for all-day wear.'},
        {'name': 'Kids White School Shoes', 'price': 1099, 'discount': 799, 'description': 'Clean white school shoes. Perfect for schools with strict uniform requirements.'},
        {'name': 'Kids Formal School Shoes', 'price': 1399, 'discount': 999, 'description': 'Premium formal school shoes. Quality materials for long-lasting performance.'}
    ],
    'kids-socks': [
        {'name': 'Kids Cotton Socks Pack', 'price': 499, 'discount': 399, 'description': 'Pack of 6 soft cotton socks. Breathable and comfortable for everyday wear.'},
        {'name': 'Kids Sports Socks Pack', 'price': 599, 'discount': 449, 'description': 'Athletic socks pack of 4. Moisture-wicking material for active kids.'},
        {'name': 'Kids Colorful Socks Pack', 'price': 449, 'discount': 349, 'description': 'Fun colorful socks pack of 6. Bright patterns and colors kids love.'},
        {'name': 'Kids School Socks Pack', 'price': 399, 'discount': 299, 'description': 'Plain school socks pack of 6. Classic colors for school uniforms.'}
    ]
}

print("Creating kids footwear subcategories and products...")

# Create subcategories and products
for subcat_data in footwear_subcategories:
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
    if subcat_slug in footwear_products:
        products_data = footwear_products[subcat_slug]
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

print("\nKids footwear population completed!")
