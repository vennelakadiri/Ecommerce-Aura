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

# Home storage subcategories to create
storage_subcategories = [
    {'name': 'Bins', 'slug': 'bins'},
    {'name': 'Hangers', 'slug': 'hangers'},
    {'name': 'Organisers', 'slug': 'organisers'},
    {'name': 'Hooks & Holders', 'slug': 'hooks-holders'},
    {'name': 'Laundry Bags', 'slug': 'laundry-bags'}
]

# Product data for each subcategory
storage_products = {
    'bins': [
        {'name': 'Plastic Storage Bin Set', 'price': 1299, 'discount': 999, 'description': 'Set of 3 plastic storage bins with lids. Durable and stackable organization.'},
        {'name': 'Kitchen Waste Bin', 'price': 899, 'discount': 699, 'description': 'Modern kitchen waste bin with pedal. Hands-free operation and sleek design.'},
        {'name': 'Recycling Bin Set', 'price': 1599, 'discount': 1199, 'description': 'Color-coded recycling bin set for waste separation. Eco-friendly solution.'},
        {'name': 'Decorative Storage Bin', 'price': 999, 'discount': 799, 'description': 'Stylish decorative storage bin for home organization. Functional and aesthetic.'}
    ],
    'hangers': [
        {'name': 'Velvet Hangers Set', 'price': 699, 'discount': 549, 'description': 'Premium velvet hangers set of 20. Non-slip and gentle on clothes.'},
        {'name': 'Wooden Hangers Collection', 'price': 999, 'discount': 799, 'description': 'Elegant wooden hangers for suits and coats. Luxury wardrobe organization.'},
        {'name': 'Space Saving Hangers', 'price': 799, 'discount': 649, 'description': 'Innovative space-saving hangers. Maximizes closet storage capacity.'},
        {'name': 'Kids Hangers Set', 'price': 499, 'discount': 399, 'description': 'Colorful hangers set for children\'s clothes. Perfect size for kids\' wardrobe.'}
    ],
    'organisers': [
        {'name': 'Closet Organiser Set', 'price': 1499, 'discount': 1199, 'description': 'Complete closet organizer system. Efficient wardrobe management.'},
        {'name': 'Drawer Organiser', 'price': 699, 'discount': 549, 'description': 'Adjustable drawer organizer for various items. Customizable storage solution.'},
        {'name': 'Shoe Organiser Rack', 'price': 999, 'discount': 799, 'description': 'Multi-tier shoe organizer rack. Keeps footwear organized and accessible.'},
        {'name': 'Desk Organiser Set', 'price': 799, 'discount': 649, 'description': 'Comprehensive desk organizer for office supplies. Productive workspace solution.'}
    ],
    'hooks-holders': [
        {'name': 'Wall Hook Set', 'price': 499, 'discount': 399, 'description': 'Set of 6 wall hooks for hanging items. Versatile storage solution.'},
        {'name': 'Over Door Hooks', 'price': 699, 'discount': 549, 'description': 'Over-the-door hooks for additional storage. No drilling required.'},
        {'name': 'Adhesive Hooks Set', 'price': 399, 'discount': 299, 'description': 'Damage-free adhesive hooks for walls. Easy to install and remove.'},
        {'name': 'Heavy Duty Hooks', 'price': 799, 'discount': 649, 'description': 'Industrial strength hooks for heavy items. Maximum weight capacity.'}
    ],
    'laundry-bags': [
        {'name': 'Canvas Laundry Bag', 'price': 699, 'discount': 549, 'description': 'Durable canvas laundry bag with drawstring. Large capacity for laundry.'},
        {'name': 'Waterproof Laundry Bag', 'price': 799, 'discount': 649, 'description': 'Waterproof laundry bag for wet clothes. Protects floors from moisture.'},
        {'name': 'Collapsible Laundry Hamper', 'price': 999, 'discount': 799, 'description': 'Foldable laundry hamper with lid. Space-saving when not in use.'},
        {'name': 'Designer Laundry Bag', 'price': 899, 'discount': 699, 'description': 'Stylish designer laundry bag. Combines functionality with aesthetics.'}
    ]
}

print("Creating Home storage subcategories and products...")

# Create subcategories and products
for subcat_data in storage_subcategories:
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
    if subcat_slug in storage_products:
        products_data = storage_products[subcat_slug]
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

print("\nHome storage population completed!")
