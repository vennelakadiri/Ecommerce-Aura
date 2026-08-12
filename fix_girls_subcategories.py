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

# Check if H&M Girls Dresses subcategory exists
hm_girls_dresses = SubCategory.objects.filter(category=kids_category, slug='handm-girls-dresses').first()
if not hm_girls_dresses:
    print("Creating H&M Girls Dresses subcategory...")
    hm_girls_dresses = SubCategory.objects.create(
        name="H&M Girls Dresses",
        slug="handm-girls-dresses",
        category=kids_category,
        is_active=True
    )
    print(f"Created: {hm_girls_dresses.name}")

# Create H&M Girls Dresses products
hm_dresses_products = [
    {'name': 'H&M Girls Floral Dress', 'price': 1799, 'discount': 1299, 'description': 'Beautiful floral dress with modern design from H&M. Perfect for parties and special occasions.'},
    {'name': 'H&M Girls Summer Dress', 'price': 1599, 'discount': 1099, 'description': 'Lightweight summer dress from H&M. Bright colors and comfortable fabric for hot weather.'},
    {'name': 'H&M Girls Party Dress', 'price': 2299, 'discount': 1699, 'description': 'Elegant party dress from H&M. Stylish design perfect for celebrations and events.'},
    {'name': 'H&M Girls Casual Dress', 'price': 1399, 'discount': 999, 'description': 'Comfortable casual dress from H&M. Perfect for everyday wear and school.'},
    {'name': 'H&M Girls Printed Dress', 'price': 1699, 'discount': 1199, 'description': 'Fun printed dress from H&M with colorful patterns. Stylish and comfortable for girls.'},
]

print("Creating H&M Girls Dresses products...")
for product_data in hm_dresses_products:
    if not Product.objects.filter(name=product_data['name'], subcategory=hm_girls_dresses).exists():
        product = Product.objects.create(
            name=product_data['name'],
            slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and')}-{random.randint(1000, 9999)}",
            description=product_data['description'],
            short_description=product_data['description'][:100] + "...",
            category=kids_category,
            subcategory=hm_girls_dresses,
            brand=Brand.objects.filter(name__icontains='h&m').first() or random.choice(brands),
            gender='kids',
            price=product_data['price'],
            discount_price=product_data['discount'],
            is_active=True,
            is_featured=random.choice([True, False]),
            stock_quantity=random.randint(20, 100),
            sku=f"HM-GIRLS-{random.randint(10000, 99999)}"
        )
        print(f"Created: {product.name}")
    else:
        print(f"Already exists: {product_data['name']}")

# Now check other girls subcategories that might be showing boys products
girls_subcategories_to_check = [
    'clothing-sets',
    'lehenga-choli', 
    'kurta-sets',
    'party-wear',
    'jacket-sweater-and-sweatshirts',
    'innerwear-and-thermals',
    'nightwear-and-loungewear',
    'value-packs'
]

print("\nChecking girls subcategories for boys products...")
for subcat_slug in girls_subcategories_to_check:
    subcat = SubCategory.objects.filter(category=kids_category, slug=subcat_slug).first()
    if subcat:
        products = Product.objects.filter(subcategory=subcat)
        print(f"\n{subcat.name} ({subcat.slug}): {products.count()} products")
        
        # Check if products have "boys" in their names (indicating wrong gender assignment)
        boys_products = products.filter(name__icontains='boys')
        if boys_products.exists():
            print(f"  WARNING: Found {boys_products.count()} boys products in girls subcategory!")
            for bp in boys_products[:3]:  # Show first 3
                print(f"    - {bp.name}")
            
            # Fix by updating these to be girls products or creating new girls products
            print("  Creating new girls products for this subcategory...")
            if subcat_slug == 'clothing-sets':
                girls_products = [
                    {'name': 'Girls 2-Piece Set', 'price': 1899, 'discount': 1399, 'description': 'Coordinated 2-piece set for girls with t-shirt and skirt. Perfect matching outfit.'},
                    {'name': 'Girls 3-Piece Set', 'price': 2399, 'discount': 1799, 'description': 'Complete 3-piece set for girls with top, skirt, and accessories. Stylish coordinated outfit.'},
                    {'name': 'Girls Summer Set', 'price': 1699, 'discount': 1199, 'description': 'Lightweight summer set for girls with breathable fabrics. Perfect for hot weather.'},
                    {'name': 'Girls Party Wear Set', 'price': 2899, 'discount': 2199, 'description': 'Elegant party wear set for girls. Premium fabrics and stylish design.'},
                ]
            elif subcat_slug == 'lehenga-choli':
                girls_products = [
                    {'name': 'Girls Lehenga Choli', 'price': 2499, 'discount': 1899, 'description': 'Traditional lehenga choli for girls. Beautiful embroidery and elegant design.'},
                    {'name': 'Girls Designer Lehenga', 'price': 3499, 'discount': 2699, 'description': 'Designer lehenga choli for special occasions. Intricate work and premium fabric.'},
                    {'name': 'Girls Simple Lehenga', 'price': 1999, 'discount': 1499, 'description': 'Simple yet elegant lehenga choli. Perfect for festivals and celebrations.'},
                ]
            elif subcat_slug == 'kurta-sets':
                girls_products = [
                    {'name': 'Girls Kurta Set', 'price': 2099, 'discount': 1599, 'description': 'Traditional kurta set for girls. Comfortable and stylish for cultural events.'},
                    {'name': 'Girls Designer Kurta', 'price': 2599, 'discount': 1999, 'description': 'Designer kurta set with modern styling. Perfect for special occasions.'},
                    {'name': 'Girls Cotton Kurta', 'price': 1799, 'discount': 1299, 'description': 'Comfortable cotton kurta set for girls. Breathable fabric for all-day wear.'},
                ]
            elif subcat_slug == 'party-wear':
                girls_products = [
                    {'name': 'Girls Party Dress', 'price': 2799, 'discount': 2099, 'description': 'Elegant party dress for girls. Beautiful design perfect for celebrations.'},
                    {'name': 'Girls Formal Outfit', 'price': 3299, 'discount': 2499, 'description': 'Sophisticated formal outfit for girls. Complete set for special events.'},
                    {'name': 'Girls Evening Wear', 'price': 2999, 'discount': 2299, 'description': 'Stylish evening wear for girls. Modern design with elegant details.'},
                ]
            elif subcat_slug == 'jacket-sweater-and-sweatshirts':
                girls_products = [
                    {'name': 'Girls Denim Jacket', 'price': 2199, 'discount': 1699, 'description': 'Trendy denim jacket for girls. Perfect for layering and casual outings.'},
                    {'name': 'Girls Hooded Sweatshirt', 'price': 1199, 'discount': 899, 'description': 'Cozy hooded sweatshirt for girls. Comfortable and stylish for casual wear.'},
                    {'name': 'Girls Winter Jacket', 'price': 3199, 'discount': 2399, 'description': 'Warm winter jacket for girls. Provides protection from cold weather.'},
                    {'name': 'Girls Cardigan', 'price': 1399, 'discount': 999, 'description': 'Elegant cardigan for girls. Perfect for layering over dresses.'},
                ]
            elif subcat_slug == 'innerwear-and-thermals':
                girls_products = [
                    {'name': 'Girls Camisole Pack', 'price': 699, 'discount': 499, 'description': 'Comfortable camisole pack of 3 for girls. Soft fabric for everyday wear.'},
                    {'name': 'Girls Briefs Pack', 'price': 599, 'discount': 399, 'description': 'Soft briefs pack of 3 for girls. Comfortable and breathable fabric.'},
                    {'name': 'Girls Thermals Set', 'price': 899, 'discount': 699, 'description': 'Warm thermal set for girls. Provides insulation and comfort in cold weather.'},
                ]
            elif subcat_slug == 'nightwear-and-loungewear':
                girls_products = [
                    {'name': 'Girls Night Suit', 'price': 999, 'discount': 799, 'description': 'Comfortable night suit for girls. Soft fabric with pretty design for peaceful sleep.'},
                    {'name': 'Girls Pajama Set', 'price': 899, 'discount': 699, 'description': 'Cute pajama set for girls. Cozy and comfortable for bedtime.'},
                    {'name': 'Girls Night Gown', 'price': 799, 'discount': 599, 'description': 'Elegant night gown for girls. Soft and breathable fabric for restful nights.'},
                ]
            elif subcat_slug == 'value-packs':
                girls_products = [
                    {'name': 'Girls T-Shirt Pack', 'price': 1799, 'discount': 1299, 'description': 'Value pack of 5 colorful t-shirts for girls. Essential basics for everyday wear.'},
                    {'name': 'Girls Leggings Pack', 'price': 1999, 'discount': 1499, 'description': 'Pack of 3 comfortable leggings for girls. Perfect for school and casual wear.'},
                    {'name': 'Girls Innerwear Pack', 'price': 899, 'discount': 699, 'description': 'Complete innerwear pack for girls. Great value for money.'},
                    {'name': 'Girls Socks Pack', 'price': 499, 'discount': 299, 'description': 'Pack of 6 colorful socks for girls. Soft and comfortable for daily wear.'},
                ]
            else:
                girls_products = []
            
            # Create new girls products
            for product_data in girls_products:
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
                        sku=f"GIRLS-{random.randint(10000, 99999)}"
                    )
                    print(f"    Created: {product.name}")
                else:
                    print(f"    Already exists: {product_data['name']}")
        else:
            print("  All products appear to be correctly assigned")

print("\nFix completed!")
