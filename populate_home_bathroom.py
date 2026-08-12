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

# Home bathroom subcategories to create
bathroom_subcategories = [
    {'name': 'Bath Towels', 'slug': 'bath-towels'},
    {'name': 'Hand & Face Towels', 'slug': 'hand-face-towels'},
    {'name': 'Beach Towels', 'slug': 'beach-towels'},
    {'name': 'Towels Set', 'slug': 'towels-set'},
    {'name': 'Bath Rugs', 'slug': 'bath-rugs'},
    {'name': 'Bath Robes', 'slug': 'bath-robes'},
    {'name': 'Bathroom Accessories', 'slug': 'bathroom-accessories'},
    {'name': 'Shower Curtains', 'slug': 'shower-curtains'}
]

# Product data for each subcategory
bathroom_products = {
    'bath-towels': [
        {'name': 'Premium Cotton Bath Towel', 'price': 699, 'discount': 549, 'description': 'Luxurious cotton bath towel with superior absorbency. Soft and plush for ultimate comfort.'},
        {'name': 'Quick Dry Bath Towel', 'price': 799, 'discount': 649, 'description': 'Fast-drying bath towel perfect for daily use. Lightweight yet highly absorbent.'},
        {'name': 'Egyptian Cotton Bath Towel', 'price': 999, 'discount': 799, 'description': 'Premium Egyptian cotton bath towel with hotel-quality feel. Extra soft and durable.'},
        {'name': 'Bamboo Fiber Bath Towel', 'price': 899, 'discount': 699, 'description': 'Eco-friendly bamboo fiber bath towel. Naturally antimicrobial and hypoallergenic.'}
    ],
    'hand-face-towels': [
        {'name': 'Soft Cotton Hand Towel', 'price': 299, 'discount': 249, 'description': 'Gentle cotton hand towel for daily use. Highly absorbent and quick drying.'},
        {'name': 'Luxury Face Towel Set', 'price': 499, 'discount': 399, 'description': 'Premium face towel set of 3. Soft on skin with excellent absorbency.'},
        {'name': 'Microfiber Hand Towel', 'price': 349, 'discount': 299, 'description': 'Ultra-absorbent microfiber hand towel. Quick dry and lightweight.'},
        {'name': 'Egyptian Cotton Face Towel', 'price': 399, 'discount': 349, 'description': 'Premium Egyptian cotton face towel. Extra soft and gentle on skin.'}
    ],
    'beach-towels': [
        {'name': 'Large Beach Towel', 'price': 899, 'discount': 699, 'description': 'Spacious beach towel perfect for beach days. Quick-drying and sand-resistant.'},
        {'name': 'Colorful Beach Towel', 'price': 799, 'discount': 649, 'description': 'Vibrant beach towel with fun patterns. Stand out on the beach with style.'},
        {'name': 'Family Beach Towel Set', 'price': 1499, 'discount': 1199, 'description': 'Complete beach towel set for family. Includes 4 different sizes and colors.'},
        {'name': 'Quick Dry Beach Towel', 'price': 699, 'discount': 549, 'description': 'Fast-drying beach towel for active beach days. Lightweight and portable.'}
    ],
    'towels-set': [
        {'name': 'Complete Bathroom Towel Set', 'price': 1999, 'discount': 1599, 'description': 'Complete bathroom towel set with bath, hand, and face towels. Everything you need.'},
        {'name': 'Luxury Towel Set', 'price': 2499, 'discount': 1999, 'description': 'Premium luxury towel set with hotel-quality towels. Elevate your bathroom.'},
        {'name': 'Family Towel Set', 'price': 1799, 'discount': 1399, 'description': 'Practical family towel set with multiple sizes. Perfect for busy households.'},
        {'name': 'Designer Towel Set', 'price': 2299, 'discount': 1799, 'description': 'Stylish designer towel set with modern colors. Fashionable bathroom decor.'}
    ],
    'bath-rugs': [
        {'name': 'Cotton Bath Rug', 'price': 699, 'discount': 549, 'description': 'Soft cotton bath rug for bathroom comfort. Absorbent and non-slip backing.'},
        {'name': 'Memory Foam Bath Rug', 'price': 999, 'discount': 799, 'description': 'Luxurious memory foam bath rug. Extra cushioning for ultimate comfort.'},
        {'name': 'Microfiber Bath Rug', 'price': 799, 'discount': 649, 'description': 'Quick-drying microfiber bath rug. Highly absorbent and easy to clean.'},
        {'name': 'Bamboo Bath Rug', 'price': 899, 'discount': 699, 'description': 'Eco-friendly bamboo bath rug. Naturally antimicrobial and stylish.'}
    ],
    'bath-robes': [
        {'name': 'Luxury Cotton Bath Robe', 'price': 1299, 'discount': 999, 'description': 'Premium cotton bath robe with hood. Spa-quality comfort at home.'},
        {'name': 'Quick Dry Bath Robe', 'price': 999, 'discount': 799, 'description': 'Fast-drying bath robe for daily use. Lightweight and comfortable.'},
        {'name': 'Waffle Bath Robe', 'price': 1199, 'discount': 899, 'description': 'Classic waffle weave bath robe. Traditional style with modern comfort.'},
        {'name': 'Plush Bath Robe', 'price': 1499, 'discount': 1199, 'description': 'Extra plush bath robe for ultimate luxury. Thick and cozy material.'}
    ],
    'bathroom-accessories': [
        {'name': 'Complete Bathroom Accessory Set', 'price': 999, 'discount': 799, 'description': 'Complete bathroom accessory set with soap dispenser, toothbrush holder, and more.'},
        {'name': 'Modern Bathroom Accessories', 'price': 1299, 'discount': 999, 'description': 'Contemporary bathroom accessories with sleek design. Modern and functional.'},
        {'name': 'Luxury Bathroom Set', 'price': 1899, 'discount': 1499, 'description': 'Premium luxury bathroom accessories. High-end materials and design.'},
        {'name': 'Minimalist Bathroom Accessories', 'price': 799, 'discount': 649, 'description': 'Clean minimalist bathroom accessories. Simple and elegant design.'}
    ],
    'shower-curtains': [
        {'name': 'Waterproof Shower Curtain', 'price': 699, 'discount': 549, 'description': 'Durable waterproof shower curtain. Complete bathroom protection.'},
        {'name': 'Fabric Shower Curtain', 'price': 899, 'discount': 699, 'description': 'Elegant fabric shower curtain with liner. Stylish and functional.'},
        {'name': 'Printed Shower Curtain', 'price': 799, 'discount': 649, 'description': 'Decorative printed shower curtain. Adds personality to bathroom.'},
        {'name': 'Luxury Shower Curtain Set', 'price': 1199, 'discount': 999, 'description': 'Premium shower curtain set with accessories. Complete bathroom makeover.'}
    ]
}

print("Creating Home bathroom subcategories and products...")

# Create subcategories and products
for subcat_data in bathroom_subcategories:
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
    if subcat_slug in bathroom_products:
        products_data = bathroom_products[subcat_slug]
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

print("\nHome bathroom population completed!")
