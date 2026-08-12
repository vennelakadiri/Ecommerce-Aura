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

# Home kitchen/dining subcategories to create
kitchen_subcategories = [
    {'name': 'Table Runners', 'slug': 'table-runners'},
    {'name': 'Dinnerware & Serveware', 'slug': 'dinnerware-serveware'},
    {'name': 'Cups and Mugs', 'slug': 'cups-mugs'},
    {'name': 'Bakeware & Cookware', 'slug': 'bakeware-cookware'},
    {'name': 'Kitchen Storage & Tools', 'slug': 'kitchen-storage-tools'},
    {'name': 'Bar & Drinkware', 'slug': 'bar-drinkware'},
    {'name': 'Table Covers & Furnishings', 'slug': 'table-covers-furnishings'}
]

# Product data for each subcategory
kitchen_products = {
    'table-runners': [
        {'name': 'Elegant Table Runner', 'price': 899, 'discount': 699, 'description': 'Beautiful table runner with elegant patterns. Perfect for dining table decoration.'},
        {'name': 'Cotton Table Runner', 'price': 699, 'discount': 549, 'description': 'Soft cotton table runner for daily use. Durable and easy to maintain.'},
        {'name': 'Embroidered Table Runner', 'price': 1299, 'discount': 999, 'description': 'Intricately embroidered table runner. Adds sophistication to dining.'},
        {'name': 'Printed Table Runner', 'price': 799, 'discount': 649, 'description': 'Colorful printed table runner. Vibrant design for festive occasions.'}
    ],
    'dinnerware-serveware': [
        {'name': 'Ceramic Dinnerware Set', 'price': 2999, 'discount': 2299, 'description': 'Complete ceramic dinnerware set for 6 people. Elegant and durable.'},
        {'name': 'Porcelain Serveware Set', 'price': 3499, 'discount': 2799, 'description': 'Premium porcelain serveware collection. Perfect for entertaining guests.'},
        {'name': 'Stainless Steel Cutlery Set', 'price': 1999, 'discount': 1599, 'description': 'Complete stainless steel cutlery set. Rust-resistant and elegant.'},
        {'name': 'Glass Dinnerware Set', 'price': 2499, 'discount': 1999, 'description': 'Beautiful glass dinnerware set. Modern and sophisticated dining.'}
    ],
    'cups-mugs': [
        {'name': 'Ceramic Coffee Mug Set', 'price': 899, 'discount': 699, 'description': 'Set of 4 ceramic coffee mugs. Perfect for morning coffee.'},
        {'name': 'Glass Tea Cups Set', 'price': 799, 'discount': 649, 'description': 'Elegant glass tea cups set. Ideal for tea time.'},
        {'name': 'Porcelain Mugs Collection', 'price': 999, 'discount': 799, 'description': 'Premium porcelain mugs with modern designs.'},
        {'name': 'Travel Mug Set', 'price': 699, 'discount': 549, 'description': 'Insulated travel mugs for on-the-go beverages. Keeps drinks hot/cold.'}
    ],
    'bakeware-cookware': [
        {'name': 'Non-Stick Cookware Set', 'price': 3999, 'discount': 2999, 'description': 'Complete non-stick cookware set. Healthy cooking with less oil.'},
        {'name': 'Stainless Steel Cookware', 'price': 4999, 'discount': 3999, 'description': 'Premium stainless steel cookware set. Professional grade cooking.'},
        {'name': 'Bakeware Set', 'price': 1999, 'discount': 1599, 'description': 'Complete bakeware set for baking enthusiasts. Various sizes and shapes.'},
        {'name': 'Ceramic Cookware Set', 'price': 3499, 'discount': 2799, 'description': 'Eco-friendly ceramic cookware set. Non-toxic and durable.'}
    ],
    'kitchen-storage-tools': [
        {'name': 'Food Storage Container Set', 'price': 999, 'discount': 799, 'description': 'Complete food storage container set. Airtight and stackable.'},
        {'name': 'Kitchen Tool Set', 'price': 1299, 'discount': 999, 'description': 'Comprehensive kitchen tool set. Essential utensils for cooking.'},
        {'name': 'Spice Rack Organizer', 'price': 799, 'discount': 649, 'description': 'Compact spice rack organizer. Efficient kitchen storage.'},
        {'name': 'Cutting Board Set', 'price': 899, 'discount': 699, 'description': 'Set of cutting boards in different sizes. Hygienic food preparation.'}
    ],
    'bar-drinkware': [
        {'name': 'Wine Glass Set', 'price': 1499, 'discount': 1199, 'description': 'Elegant wine glass set of 6. Perfect for wine enthusiasts.'},
        {'name': 'Cocktail Shaker Set', 'price': 999, 'discount': 799, 'description': 'Complete cocktail shaker set. Professional bar tools.'},
        {'name': 'Whiskey Glass Set', 'price': 1299, 'discount': 999, 'description': 'Premium whiskey glasses set. Classic design for connoisseurs.'},
        {'name': 'Beer Mug Collection', 'price': 899, 'discount': 699, 'description': 'Stylish beer mug set. Perfect for beer lovers.'}
    ],
    'table-covers-furnishings': [
        {'name': 'Tablecloth Set', 'price': 1299, 'discount': 999, 'description': 'Elegant tablecloth set for dining table. Premium fabric and design.'},
        {'name': 'Placemat Set', 'price': 699, 'discount': 549, 'description': 'Set of decorative placemats. Protects table and adds style.'},
        {'name': 'Napkin Rings Set', 'price': 799, 'discount': 649, 'description': 'Elegant napkin rings set. Sophisticated table setting.'},
        {'name': 'Table Cover Set', 'price': 999, 'discount': 799, 'description': 'Protective table cover set. Durable and stylish.'}
    ]
}

print("Creating Home kitchen/dining subcategories and products...")

# Create subcategories and products
for subcat_data in kitchen_subcategories:
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
    if subcat_slug in kitchen_products:
        products_data = kitchen_products[subcat_slug]
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

print("\nHome kitchen/dining population completed!")
