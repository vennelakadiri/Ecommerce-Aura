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

# Home bedding subcategories to create
bedding_subcategories = [
    {'name': 'Home Center Bedsheets', 'slug': 'home-center-bedsheets'},
    {'name': 'Westside Bedsheets', 'slug': 'westside-bedsheets'},
    {'name': 'Raymond Bedsheets', 'slug': 'raymond-bedsheets'},
    {'name': 'Bomba Bedsheets', 'slug': 'bomba-bedsheets'},
    {'name': 'Portico Bedsheets', 'slug': 'portico-bedsheets'},
    {'name': 'Mattress Protectors', 'slug': 'mattress-protectors'},
    {'name': 'Bedding Sets', 'slug': 'bedding-sets'},
    {'name': 'Blankets, Quilts & Dohars', 'slug': 'blankets-quilts-dohars'},
    {'name': 'Pillows & Pillow Covers', 'slug': 'pillows-pillow-covers'},
    {'name': 'Bed Covers', 'slug': 'bed-covers'},
    {'name': 'Diwan Sets', 'slug': 'diwan-sets'},
    {'name': 'Chair Pads & Covers', 'slug': 'chair-pads-covers'},
    {'name': 'Sofa Covers', 'slug': 'sofa-covers'}
]

# Product data for each subcategory
bedding_products = {
    'home-center-bedsheets': [
        {'name': 'Home Center Cotton Bedsheet', 'price': 899, 'discount': 699, 'description': 'Premium cotton bedsheet from Home Center. Soft and comfortable for restful sleep.'},
        {'name': 'Home Center Double Bedsheet', 'price': 1299, 'discount': 999, 'description': 'Spacious double bedsheet from Home Center. Perfect for master bedrooms.'},
        {'name': 'Home Center Printed Bedsheet', 'price': 1099, 'discount': 849, 'description': 'Elegant printed bedsheet from Home Center. Adds style to your bedroom decor.'},
        {'name': 'Home Center King Size Bedsheet', 'price': 1599, 'discount': 1199, 'description': 'Luxurious king size bedsheet from Home Center. Extra comfort for larger beds.'}
    ],
    'westside-bedsheets': [
        {'name': 'Westside Designer Bedsheet', 'price': 1499, 'discount': 1199, 'description': 'Stylish designer bedsheet from Westside. Modern patterns and premium fabric.'},
        {'name': 'Westside Floral Bedsheet', 'price': 1299, 'discount': 999, 'description': 'Beautiful floral bedsheet from Westside. Fresh and vibrant bedroom decor.'},
        {'name': 'Westside Solid Bedsheet', 'price': 999, 'discount': 799, 'description': 'Classic solid color bedsheet from Westside. Timeless elegance for any bedroom.'},
        {'name': 'Westside Striped Bedsheet', 'price': 1199, 'discount': 899, 'description': 'Contemporary striped bedsheet from Westside. Modern design with comfort.'}
    ],
    'raymond-bedsheets': [
        {'name': 'Raymond Premium Cotton Bedsheet', 'price': 1999, 'discount': 1499, 'description': 'Luxurious cotton bedsheet from Raymond. Superior quality and comfort.'},
        {'name': 'Raymond Silk Blend Bedsheet', 'price': 2499, 'discount': 1899, 'description': 'Elegant silk blend bedsheet from Raymond. Premium feel and sheen.'},
        {'name': 'Raymond Classic White Bedsheet', 'price': 1799, 'discount': 1399, 'description': 'Sophisticated white bedsheet from Raymond. Crisp and clean look.'},
        {'name': 'Raymond Designer Collection Bedsheet', 'price': 2999, 'discount': 2299, 'description': 'Exclusive designer bedsheet from Raymond. Luxury and style combined.'}
    ],
    'bomba-bedsheets': [
        {'name': 'Bomba Microfiber Bedsheet', 'price': 799, 'discount': 599, 'description': 'Soft microfiber bedsheet from Bomba. Wrinkle-resistant and easy care.'},
        {'name': 'Bomba Geometric Bedsheet', 'price': 999, 'discount': 749, 'description': 'Modern geometric pattern bedsheet from Bomba. Contemporary bedroom style.'},
        {'name': 'Bomba Kids Bedsheet', 'price': 899, 'discount': 699, 'description': 'Fun colorful bedsheet from Bomba. Perfect for children\'s rooms.'},
        {'name': 'Bomba Luxury Bedsheet', 'price': 1199, 'discount': 899, 'description': 'Premium luxury bedsheet from Bomba. Extra soft and durable.'}
    ],
    'portico-bedsheets': [
        {'name': 'Portico Embroidered Bedsheet', 'price': 1699, 'discount': 1299, 'description': 'Elegant embroidered bedsheet from Portico. Detailed craftsmanship.'},
        {'name': 'Portico Jaipuri Bedsheet', 'price': 1399, 'discount': 1099, 'description': 'Traditional Jaipuri print bedsheet from Portico. Ethnic charm.'},
        {'name': 'Portico Satin Bedsheet', 'price': 1899, 'discount': 1499, 'description': 'Luxurious satin bedsheet from Portico. Smooth and elegant.'},
        {'name': 'Portico Designer Bedsheet', 'price': 2199, 'discount': 1699, 'description': 'Exclusive designer bedsheet from Portico. Premium home decor.'}
    ],
    'mattress-protectors': [
        {'name': 'Waterproof Mattress Protector', 'price': 999, 'discount': 799, 'description': 'Premium waterproof mattress protector. Complete protection against spills.'},
        {'name': 'Cotton Mattress Protector', 'price': 799, 'discount': 649, 'description': 'Soft cotton mattress protector. Breathable and comfortable.'},
        {'name': 'Anti-Allergy Mattress Protector', 'price': 1299, 'discount': 999, 'description': 'Hypoallergenic mattress protector. Perfect for sensitive skin.'},
        {'name': 'Cooling Gel Mattress Protector', 'price': 1499, 'discount': 1199, 'description': 'Advanced cooling gel mattress protector. Regulates temperature.'}
    ],
    'bedding-sets': [
        {'name': 'Complete Bedding Set', 'price': 2999, 'discount': 2299, 'description': 'Complete bedding set with sheets, pillows, and comforter. Everything you need.'},
        {'name': 'Luxury Bedding Set', 'price': 3999, 'discount': 2999, 'description': 'Premium luxury bedding set. High-end materials and design.'},
        {'name': 'Modern Bedding Set', 'price': 2499, 'discount': 1899, 'description': 'Contemporary style bedding set. Modern patterns and colors.'},
        {'name': 'Classic Bedding Set', 'price': 2799, 'discount': 2099, 'description': 'Timeless classic bedding set. Traditional elegance.'}
    ],
    'blankets-quilts-dohars': [
        {'name': 'Winter Quilt', 'price': 1599, 'discount': 1199, 'description': 'Warm winter quilt for cold nights. Cozy and comfortable.'},
        {'name': 'Cotton Blanket', 'price': 899, 'discount': 699, 'description': 'Lightweight cotton blanket. Perfect for all seasons.'},
        {'name': 'Designer Dohar', 'price': 1299, 'discount': 999, 'description': 'Elegant designer dohar. Traditional with modern touch.'},
        {'name': 'Fleece Blanket', 'price': 1099, 'discount': 849, 'description': 'Soft fleece blanket. Extra warmth and comfort.'}
    ],
    'pillows-pillow-covers': [
        {'name': 'Memory Foam Pillow', 'price': 1299, 'discount': 999, 'description': 'Supportive memory foam pillow. Ergonomic neck support.'},
        {'name': 'Cotton Pillow Set', 'price': 799, 'discount': 649, 'description': 'Soft cotton pillow set of 2. Comfortable for all sleepers.'},
        {'name': 'Designer Pillow Covers', 'price': 599, 'discount': 449, 'description': 'Elegant pillow covers set of 2. Stylish bedroom decor.'},
        {'name': 'Luxury Pillow Set', 'price': 1899, 'discount': 1499, 'description': 'Premium luxury pillow set. Hotel-quality comfort.'}
    ],
    'bed-covers': [
        {'name': 'Embroidered Bed Cover', 'price': 1899, 'discount': 1499, 'description': 'Beautiful embroidered bed cover. Adds elegance to bedroom.'},
        {'name': 'Printed Bed Cover', 'price': 1299, 'discount': 999, 'description': 'Stylish printed bed cover. Modern and vibrant.'},
        {'name': 'Silk Bed Cover', 'price': 2499, 'discount': 1899, 'description': 'Luxurious silk bed cover. Premium look and feel.'},
        {'name': 'Cotton Bed Cover', 'price': 999, 'discount': 799, 'description': 'Comfortable cotton bed cover. Practical and stylish.'}
    ],
    'diwan-sets': [
        {'name': 'Traditional Diwan Set', 'price': 1599, 'discount': 1199, 'description': 'Classic traditional diwan set. Ethnic charm and comfort.'},
        {'name': 'Modern Diwan Set', 'price': 1399, 'discount': 1099, 'description': 'Contemporary style diwan set. Clean and modern design.'},
        {'name': 'Luxury Diwan Set', 'price': 2199, 'discount': 1699, 'description': 'Premium luxury diwan set. High-end materials.'},
        {'name': 'Cotton Diwan Set', 'price': 999, 'discount': 799, 'description': 'Comfortable cotton diwan set. Practical and durable.'}
    ],
    'chair-pads-covers': [
        {'name': 'Cushioned Chair Pads', 'price': 699, 'discount': 549, 'description': 'Comfortable cushioned chair pads set of 4. Extra seating comfort.'},
        {'name': 'Dining Chair Covers', 'price': 899, 'discount': 699, 'description': 'Elegant dining chair covers set of 6. Protects and decorates.'},
        {'name': 'Office Chair Cushion', 'price': 799, 'discount': 649, 'description': 'Supportive office chair cushion. Ergonomic design.'},
        {'name': 'Decorative Chair Pads', 'price': 599, 'discount': 449, 'description': 'Stylish decorative chair pads. Adds color to furniture.'}
    ],
    'sofa-covers': [
        {'name': 'Stretch Sofa Cover', 'price': 1899, 'discount': 1499, 'description': 'Flexible stretch sofa cover. Perfect fit for most sofas.'},
        {'name': 'Cotton Sofa Cover', 'price': 1599, 'discount': 1199, 'description': 'Breathable cotton sofa cover. Comfortable and durable.'},
        {'name': 'Waterproof Sofa Cover', 'price': 2199, 'discount': 1699, 'description': 'Protective waterproof sofa cover. Guards against spills.'},
        {'name': 'Designer Sofa Cover', 'price': 2499, 'discount': 1899, 'description': 'Stylish designer sofa cover. Premium home decor.'}
    ]
}

print("Creating Home bedding subcategories and products...")

# Create subcategories and products
for subcat_data in bedding_subcategories:
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
    if subcat_slug in bedding_products:
        products_data = bedding_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and').replace(',', '-')}-{random.randint(1000, 9999)}",
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

print("\nHome bedding population completed!")
