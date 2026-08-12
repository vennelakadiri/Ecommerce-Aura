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

# Home lighting subcategories to create
lighting_subcategories = [
    {'name': 'Floor Lamps', 'slug': 'floor-lamps'},
    {'name': 'Ceiling Lamps', 'slug': 'ceiling-lamps'},
    {'name': 'Table Lamps', 'slug': 'table-lamps'},
    {'name': 'Wall Lamps', 'slug': 'wall-lamps'},
    {'name': 'Outdoor Lamps', 'slug': 'outdoor-lamps'},
    {'name': 'String Lights', 'slug': 'string-lights'}
]

# Product data for each subcategory
lighting_products = {
    'floor-lamps': [
        {'name': 'Modern Arc Floor Lamp', 'price': 2499, 'discount': 1999, 'description': 'Elegant arc floor lamp with adjustable height. Perfect for reading and ambiance.'},
        {'name': 'Tripod Floor Lamp', 'price': 1999, 'discount': 1599, 'description': 'Stylish tripod floor lamp with minimalist design. Ideal for contemporary spaces.'},
        {'name': 'Traditional Floor Lamp', 'price': 1799, 'discount': 1399, 'description': 'Classic traditional floor lamp with fabric shade. Timeless elegance for any room.'},
        {'name': 'LED Floor Lamp', 'price': 2299, 'discount': 1799, 'description': 'Energy-efficient LED floor lamp with dimmable feature. Modern and sustainable lighting.'}
    ],
    'ceiling-lamps': [
        {'name': 'Modern Ceiling Lamp', 'price': 2999, 'discount': 2299, 'description': 'Contemporary ceiling lamp with sleek design. Perfect centerpiece for modern homes.'},
        {'name': 'Crystal Chandelier', 'price': 4999, 'discount': 3999, 'description': 'Luxurious crystal chandelier for elegant lighting. Adds sophistication to any space.'},
        {'name': 'LED Ceiling Light', 'price': 1999, 'discount': 1599, 'description': 'Energy-efficient LED ceiling light panel. Bright and cost-effective lighting solution.'},
        {'name': 'Traditional Ceiling Lamp', 'price': 2499, 'discount': 1999, 'description': 'Classic ceiling lamp with ornate details. Traditional charm with modern functionality.'}
    ],
    'table-lamps': [
        {'name': 'Modern Table Lamp', 'price': 1299, 'discount': 999, 'description': 'Sleek modern table lamp for desks and side tables. Minimalist design with warm light.'},
        {'name': 'Vintage Table Lamp', 'price': 1499, 'discount': 1199, 'description': 'Retro-style table lamp with classic design. Perfect for nostalgic decor themes.'},
        {'name': 'LED Table Lamp', 'price': 999, 'discount': 799, 'description': 'Energy-efficient LED table lamp with adjustable brightness. Eco-friendly lighting.'},
        {'name': 'Designer Table Lamp', 'price': 1799, 'discount': 1399, 'description': 'Artistic designer table lamp as statement piece. Functional lighting with artistic flair.'}
    ],
    'wall-lamps': [
        {'name': 'Modern Wall Lamp', 'price': 1599, 'discount': 1199, 'description': 'Contemporary wall lamp with clean lines. Perfect for hallways and accent lighting.'},
        {'name': 'Vintage Wall Sconce', 'price': 1899, 'discount': 1499, 'description': 'Classic wall sconce with antique finish. Traditional charm for any wall.'},
        {'name': 'LED Wall Light', 'price': 1299, 'discount': 999, 'description': 'Slim LED wall light for modern spaces. Energy-efficient and stylish illumination.'},
        {'name': 'Adjustable Wall Lamp', 'price': 1799, 'discount': 1399, 'description': 'Flexible wall lamp with adjustable direction. Versatile lighting for reading and ambiance.'}
    ],
    'outdoor-lamps': [
        {'name': 'Garden Solar Lamp', 'price': 999, 'discount': 799, 'description': 'Solar-powered garden lamp for eco-friendly lighting. Automatic dusk-to-dawn operation.'},
        {'name': 'Outdoor Wall Light', 'price': 1499, 'discount': 1199, 'description': 'Weather-resistant outdoor wall light. Durable and stylish exterior lighting.'},
        {'name': 'Pathway Light Set', 'price': 1999, 'discount': 1599, 'description': 'Set of 4 pathway lights for garden illumination. Solar-powered with stake installation.'},
        {'name': 'Security Flood Light', 'price': 1799, 'discount': 1399, 'description': 'Motion-activated security flood light. Bright illumination for safety and security.'}
    ],
    'string-lights': [
        {'name': 'Fairy String Lights', 'price': 699, 'discount': 549, 'description': 'Delicate fairy string lights for magical ambiance. Perfect for parties and decoration.'},
        {'name': 'LED String Lights', 'price': 799, 'discount': 649, 'description': 'Energy-efficient LED string lights with multiple colors. Versatile decorative lighting.'},
        {'name': 'Solar String Lights', 'price': 899, 'discount': 699, 'description': 'Solar-powered string lights for outdoor decoration. Eco-friendly and convenient.'},
        {'name': 'Vintage Bulb String Lights', 'price': 999, 'discount': 799, 'description': 'Retro-style string lights with vintage bulbs. Nostalgic charm for any space.'}
    ]
}

print("Creating Home lighting subcategories and products...")

# Create subcategories and products
for subcat_data in lighting_subcategories:
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
    if subcat_slug in lighting_products:
        products_data = lighting_products[subcat_slug]
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

print("\nHome lighting population completed!")
