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

# Home decor subcategories to create
decor_subcategories = [
    {'name': 'Plants & Planters', 'slug': 'plants-planters'},
    {'name': 'Aromas & Candles', 'slug': 'aromas-candles'},
    {'name': 'Clocks', 'slug': 'clocks'},
    {'name': 'Mirrors', 'slug': 'mirrors'},
    {'name': 'Wall Décor', 'slug': 'wall-decor'},
    {'name': 'Festive Decor', 'slug': 'festive-decor'},
    {'name': 'Pooja Essentials', 'slug': 'pooja-essentials'},
    {'name': 'Wall Shelves', 'slug': 'wall-shelves'},
    {'name': 'Fountains', 'slug': 'fountains'},
    {'name': 'Showpieces & Vases', 'slug': 'showpieces-vases'},
    {'name': 'Ottoman', 'slug': 'ottoman'}
]

# Product data for each subcategory
decor_products = {
    'plants-planters': [
        {'name': 'Indoor Plant Set', 'price': 1299, 'discount': 999, 'description': 'Set of 3 indoor plants with decorative planters. Perfect for home decoration.'},
        {'name': 'Ceramic Planter Set', 'price': 899, 'discount': 699, 'description': 'Elegant ceramic planter set of 3. Modern design for indoor plants.'},
        {'name': 'Artificial Plant Collection', 'price': 999, 'discount': 799, 'description': 'Lifelike artificial plants for maintenance-free greenery.'},
        {'name': 'Hanging Plant Planter', 'price': 799, 'discount': 649, 'description': 'Stylish hanging planter for cascading plants. Space-saving solution.'}
    ],
    'aromas-candles': [
        {'name': 'Scented Candle Set', 'price': 699, 'discount': 549, 'description': 'Luxurious scented candle set of 3. Aromatic home fragrance.'},
        {'name': 'Aroma Diffuser', 'price': 1299, 'discount': 999, 'description': 'Electric aroma diffuser with essential oils. Relaxing home ambiance.'},
        {'name': 'Decorative Candles', 'price': 899, 'discount': 699, 'description': 'Beautiful decorative candles for home decoration. Elegant and fragrant.'},
        {'name': 'Essential Oil Set', 'price': 999, 'discount': 799, 'description': 'Complete essential oil collection for aromatherapy. Natural fragrances.'}
    ],
    'clocks': [
        {'name': 'Wall Clock Modern', 'price': 999, 'discount': 799, 'description': 'Contemporary wall clock with minimalist design. Perfect for modern homes.'},
        {'name': 'Vintage Wall Clock', 'price': 1199, 'discount': 999, 'description': 'Classic vintage-style wall clock. Timeless elegance.'},
        {'name': 'Digital Table Clock', 'price': 699, 'discount': 549, 'description': 'Modern digital table clock with multiple features. Functional and stylish.'},
        {'name': 'Grandfather Clock', 'price': 4999, 'discount': 3999, 'description': 'Traditional grandfather clock for luxury homes. Classic timepiece.'}
    ],
    'mirrors': [
        {'name': 'Decorative Wall Mirror', 'price': 1599, 'discount': 1299, 'description': 'Elegant decorative wall mirror with ornate frame. Adds depth to rooms.'},
        {'name': 'Full Length Mirror', 'price': 1999, 'discount': 1599, 'description': 'Practical full-length mirror with stand. Perfect for bedrooms.'},
        {'name': 'Round Vanity Mirror', 'price': 899, 'discount': 699, 'description': 'Stylish round vanity mirror for dressing areas. Chic and functional.'},
        {'name': 'Modern Wall Mirror Set', 'price': 2299, 'discount': 1799, 'description': 'Set of 3 modern wall mirrors. Contemporary home decor.'}
    ],
    'wall-decor': [
        {'name': 'Abstract Wall Art', 'price': 1899, 'discount': 1499, 'description': 'Modern abstract wall art set. Contemporary home decoration.'},
        {'name': 'Canvas Painting Set', 'price': 2499, 'discount': 1999, 'description': 'Beautiful canvas painting set of 3. Artistic home decor.'},
        {'name': 'Wall Decor Stickers', 'price': 699, 'discount': 549, 'description': 'Creative wall decor stickers pack. Easy to apply and remove.'},
        {'name': 'Metal Wall Art', 'price': 1599, 'discount': 1299, 'description': 'Elegant metal wall art piece. Sophisticated home decoration.'}
    ],
    'festive-decor': [
        {'name': 'Festival Light Set', 'price': 999, 'discount': 799, 'description': 'Colorful festival light set for celebrations. Bright and festive.'},
        {'name': 'Decorative Lantern Set', 'price': 1299, 'discount': 999, 'description': 'Traditional decorative lantern set. Perfect for festive occasions.'},
        {'name': 'Festival Hanging Decor', 'price': 799, 'discount': 649, 'description': 'Colorful hanging festival decorations. Joyful celebration decor.'},
        {'name': 'Festive Door Decoration', 'price': 899, 'discount': 699, 'description': 'Beautiful festive door decoration set. Welcoming entrance decor.'}
    ],
    'pooja-essentials': [
        {'name': 'Pooja Thali Set', 'price': 999, 'discount': 799, 'description': 'Complete pooja thali set with all essentials. Traditional worship items.'},
        {'name': 'Brass Diya Set', 'price': 799, 'discount': 649, 'description': 'Elegant brass diya set of 5. Traditional lighting for prayers.'},
        {'name': 'Pooja Idol Set', 'price': 1299, 'discount': 999, 'description': 'Beautiful pooja idol set for worship. Spiritual home decor.'},
        {'name': 'Incense Holder Set', 'price': 699, 'discount': 549, 'description': 'Decorative incense holder set. Aromatic prayer ambiance.'}
    ],
    'wall-shelves': [
        {'name': 'Floating Wall Shelves', 'price': 1499, 'discount': 1199, 'description': 'Modern floating wall shelves set. Space-saving storage solution.'},
        {'name': 'Wooden Wall Shelf', 'price': 1799, 'discount': 1399, 'description': 'Elegant wooden wall shelf with compartments. Classic storage design.'},
        {'name': 'Decorative Wall Shelves', 'price': 1299, 'discount': 999, 'description': 'Stylish decorative wall shelves. Functional home decoration.'},
        {'name': 'Corner Wall Shelf', 'price': 999, 'discount': 799, 'description': 'Space-efficient corner wall shelf. Maximizes room space.'}
    ],
    'fountains': [
        {'name': 'Tabletop Fountain', 'price': 1999, 'discount': 1599, 'description': 'Relaxing tabletop fountain with water flow. Soothing home ambiance.'},
        {'name': 'Indoor Water Fountain', 'price': 2999, 'discount': 2299, 'description': 'Elegant indoor water fountain. Tranquil home decoration.'},
        {'name': 'Garden Fountain', 'price': 3999, 'discount': 2999, 'description': 'Beautiful garden water fountain. Outdoor decor centerpiece.'},
        {'name': 'Wall Mounted Fountain', 'price': 2499, 'discount': 1999, 'description': 'Space-saving wall mounted fountain. Modern water feature.'}
    ],
    'showpieces-vases': [
        {'name': 'Crystal Vase Set', 'price': 1599, 'discount': 1299, 'description': 'Elegant crystal vase set of 3. Luxury home decoration.'},
        {'name': 'Ceramic Showpiece', 'price': 999, 'discount': 799, 'description': 'Artistic ceramic showpiece. Unique home decor item.'},
        {'name': 'Glass Vase Collection', 'price': 1299, 'discount': 999, 'description': 'Beautiful glass vase collection. Elegant flower display.'},
        {'name': 'Decorative Showpiece Set', 'price': 1899, 'discount': 1499, 'description': 'Stylish decorative showpiece set. Contemporary home art.'}
    ],
    'ottoman': [
        {'name': 'Fabric Ottoman', 'price': 2999, 'discount': 2299, 'description': 'Comfortable fabric ottoman with storage. Multi-functional furniture.'},
        {'name': 'Leather Ottoman', 'price': 3999, 'discount': 2999, 'description': 'Luxury leather ottoman footrest. Premium home furniture.'},
        {'name': 'Storage Ottoman', 'price': 2499, 'discount': 1999, 'description': 'Practical storage ottoman with hidden compartment. Space-saving solution.'},
        {'name': 'Round Ottoman', 'price': 2799, 'discount': 2199, 'description': 'Stylish round ottoman with cushioned top. Modern home accent.'}
    ]
}

print("Creating Home decor subcategories and products...")

# Create subcategories and products
for subcat_data in decor_subcategories:
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
    if subcat_slug in decor_products:
        products_data = decor_products[subcat_slug]
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

print("\nHome decor population completed!")
