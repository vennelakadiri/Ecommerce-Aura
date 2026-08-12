import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Get men category and brands
men_category = Category.objects.get(slug='men')
brands = list(Brand.objects.all())

# Men grooming subcategories to create
grooming_subcategories = [
    {'name': 'Trimmers', 'slug': 'trimmers'},
    {'name': 'Beard Oil', 'slug': 'beard-oil'},
    {'name': 'Hair Wax', 'slug': 'hair-wax'}
]

# Product data for each subcategory
grooming_products = {
    'trimmers': [
        {'name': 'Beard Trimmer Pro', 'price': 1999, 'discount': 1499, 'description': 'Professional beard trimmer with precision blades. Perfect for detailed grooming.'},
        {'name': 'Body Trimmer', 'price': 1499, 'discount': 1199, 'description': 'Versatile body trimmer for all-over grooming. Waterproof design for wet use.'},
        {'name': 'Nose Hair Trimmer', 'price': 799, 'discount': 599, 'description': 'Precision nose hair trimmer with safety blades. Gentle and effective.'},
        {'name': 'Multi-Groom Trimmer Kit', 'price': 2499, 'discount': 1999, 'description': 'Complete grooming kit with multiple attachments. All-in-one solution.'}
    ],
    'beard-oil': [
        {'name': 'Tea Tree Beard Oil', 'price': 499, 'discount': 399, 'description': 'Tea tree beard oil for healthy beard growth. Antibacterial and soothing.'},
        {'name': 'Argan Beard Oil', 'price': 599, 'discount': 449, 'description': 'Premium argan beard oil for softness. Rich in vitamin E and antioxidants.'},
        {'name': 'Sandalwood Beard Oil', 'price': 699, 'discount': 549, 'description': 'Luxurious sandalwood beard oil. Classic masculine scent with conditioning benefits.'},
        {'name': 'Jojoba Beard Oil', 'price': 549, 'discount': 399, 'description': 'Natural jojoba beard oil for balanced moisture. Lightweight and non-greasy.'}
    ],
    'hair-wax': [
        {'name': 'Strong Hold Hair Wax', 'price': 399, 'discount': 299, 'description': 'Extra strong hold hair wax for extreme styles. Long-lasting control.'},
        {'name': 'Matte Finish Hair Wax', 'price': 349, 'discount': 249, 'description': 'Matte finish hair wax for natural look. No shine, just hold.'},
        {'name': 'Flexible Hold Hair Wax', 'price': 299, 'discount': 199, 'description': 'Flexible hold hair wax for restyling. Medium hold with natural movement.'},
        {'name': 'High Shine Hair Wax', 'price': 349, 'discount': 249, 'description': 'High shine hair wax for glossy finish. Adds luster and hold.'}
    ]
}

print("Creating Men grooming subcategories and products...")

# Create subcategories and products
for subcat_data in grooming_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=men_category,
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
                    category=men_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='male',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"MENS-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nMen grooming population completed!")
