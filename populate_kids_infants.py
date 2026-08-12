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

# Infants subcategories to create
infants_subcategories = [
    {'name': 'Bodysuits', 'slug': 'bodysuits'},
    {'name': 'Rompers & Sleepsuits', 'slug': 'rompers-sleepsuits'},
    {'name': 'Infants Sets', 'slug': 'infants-sets'},
    {'name': 'Tshirts & Tops', 'slug': 'infants-tops'},
    {'name': 'Dresses', 'slug': 'infants-dresses'},
    {'name': 'Bottom wear', 'slug': 'infants-bottom-wear'},
    {'name': 'Winter Wear', 'slug': 'infants-winter-wear'},
    {'name': 'Innerwear & Sleepwear', 'slug': 'infants-innerwear'},
    {'name': 'Infant Care', 'slug': 'infant-care'}
]

# Product data for each subcategory
infants_products = {
    'bodysuits': [
        {'name': 'Infant Cotton Bodysuit Set', 'price': 599, 'discount': 449, 'description': 'Soft cotton bodysuit set of 5 for infants. Snap closure for easy diaper changes.'},
        {'name': 'Infant Organic Bodysuit Pack', 'price': 799, 'discount': 599, 'description': 'Organic cotton bodysuit pack of 3. Hypoallergenic and gentle on baby skin.'},
        {'name': 'Infant Sleeveless Bodysuit', 'price': 449, 'discount': 349, 'description': 'Comfortable sleeveless bodysuit for warm weather. Breathable fabric for infants.'},
        {'name': 'Infant Long Sleeve Bodysuit', 'price': 699, 'discount': 549, 'description': 'Long sleeve bodysuit for cooler weather. Full coverage and warmth for infants.'}
    ],
    'rompers-sleepsuits': [
        {'name': 'Infant Cotton Romper', 'price': 899, 'discount': 699, 'description': 'Soft cotton romper for infants. One-piece design for comfort and ease of dressing.'},
        {'name': 'Infant Sleepsuit Set', 'price': 999, 'discount': 799, 'description': 'Cozy sleepsuit set of 2 for infants. Full coverage for peaceful sleep.'},
        {'name': 'Infant Summer Romper', 'price': 799, 'discount': 599, 'description': 'Lightweight summer romper. Breathable fabric for hot weather comfort.'},
        {'name': 'Infant Winter Sleepsuit', 'price': 1199, 'discount': 899, 'description': 'Warm winter sleepsuit with fleece lining. Keeps infants cozy in cold weather.'}
    ],
    'infants-sets': [
        {'name': 'Infant 3-Piece Clothing Set', 'price': 1299, 'discount': 999, 'description': 'Complete 3-piece clothing set for infants. Includes bodysuit, pants, and hat.'},
        {'name': 'Infant Newborn Gift Set', 'price': 1599, 'discount': 1199, 'description': 'Premium newborn gift set with multiple outfits. Perfect baby shower gift.'},
        {'name': 'Infant Everyday Set', 'price': 999, 'discount': 749, 'description': 'Practical everyday clothing set for infants. Mix and match pieces for versatility.'},
        {'name': 'Infant Party Wear Set', 'price': 1899, 'discount': 1499, 'description': 'Elegant party wear set for special occasions. Dress up your little one in style.'}
    ],
    'infants-tops': [
        {'name': 'Infant Cotton T-Shirt', 'price': 449, 'discount': 349, 'description': 'Soft cotton t-shirt for infants. Comfortable and breathable for everyday wear.'},
        {'name': 'Infant Sleeveless Top', 'price': 399, 'discount': 299, 'description': 'Lightweight sleeveless top for infants. Perfect for warm weather and layering.'},
        {'name': 'Infant Graphic Tee', 'price': 549, 'discount': 449, 'description': 'Fun graphic tee with cute prints. Adds personality to infant outfits.'},
        {'name': 'Infant Polo Shirt', 'price': 699, 'discount': 549, 'description': 'Classic polo shirt for infants. Smart casual look for little ones.'}
    ],
    'infants-dresses': [
        {'name': 'Infant Cotton Dress', 'price': 799, 'discount': 599, 'description': 'Soft cotton dress for infant girls. Comfortable and adorable for everyday wear.'},
        {'name': 'Infant Party Dress', 'price': 1299, 'discount': 999, 'description': 'Elegant party dress for special occasions. Beautiful design for little princesses.'},
        {'name': 'Infant Summer Dress', 'price': 699, 'discount': 549, 'description': 'Lightweight summer dress for infants. Keeps baby cool and comfortable in hot weather.'},
        {'name': 'Infant Floral Dress', 'price': 899, 'discount': 699, 'description': 'Pretty floral print dress for infant girls. Sweet and charming design.'}
    ],
    'infants-bottom-wear': [
        {'name': 'Infant Cotton Pants', 'price': 599, 'discount': 449, 'description': 'Soft cotton pants for infants. Comfortable and practical for everyday wear.'},
        {'name': 'Infant Shorts Set', 'price': 499, 'discount': 399, 'description': 'Set of 2 shorts for infants. Perfect for warm weather and active play.'},
        {'name': 'Infant Leggings', 'price': 699, 'discount': 549, 'description': 'Stretchy leggings for infants. Comfortable fit and easy movement.'},
        {'name': 'Infant Track Pants', 'price': 799, 'discount': 599, 'description': 'Cozy track pants for infants. Soft fabric and comfortable elastic waist.'}
    ],
    'infants-winter-wear': [
        {'name': 'Infant Winter Jacket', 'price': 1599, 'discount': 1199, 'description': 'Warm winter jacket for infants. Windproof and water-resistant outer layer.'},
        {'name': 'Infant Fleece Sweater', 'price': 999, 'discount': 799, 'description': 'Cozy fleece sweater for infants. Extra warmth and comfort in cold weather.'},
        {'name': 'Infant Snowsuit', 'price': 1899, 'discount': 1499, 'description': 'Full snowsuit for winter protection. Complete coverage for outdoor activities.'},
        {'name': 'Infant Thermal Set', 'price': 1199, 'discount': 899, 'description': 'Thermal underwear set for infants. Base layer for extreme cold weather.'}
    ],
    'infants-innerwear': [
        {'name': 'Infant Innerwear Set', 'price': 699, 'discount': 549, 'description': 'Soft innerwear set of 3 for infants. Comfortable base layer for all seasons.'},
        {'name': 'Infant Sleepwear Set', 'price': 799, 'discount': 699, 'description': 'Cozy sleepwear set for infants. Ensures comfortable and peaceful sleep.'},
        {'name': 'Infant Undershirt Pack', 'price': 549, 'discount': 449, 'description': 'Pack of 3 undershirts for infants. Soft fabric for sensitive skin.'},
        {'name': 'Infant Diaper Cover Set', 'price': 499, 'discount': 399, 'description': 'Decorative diaper cover set of 4. Adds style to infant outfits.'}
    ],
    'infant-care': [
        {'name': 'Infant Care Kit', 'price': 999, 'discount': 799, 'description': 'Complete infant care kit with essentials. Includes grooming items and care products.'},
        {'name': 'Infant Bath Set', 'price': 799, 'discount': 599, 'description': 'Gentle bath set for infants. Hypoallergenic products for baby bath time.'},
        {'name': 'Infant Feeding Set', 'price': 1199, 'discount': 899, 'description': 'Complete feeding set for infants. Includes bottles, spoons, and accessories.'},
        {'name': 'Infant Grooming Set', 'price': 699, 'discount': 549, 'description': 'Essential grooming set for infants. Includes brush, comb, and nail care items.'}
    ]
}

print("Creating kids infants subcategories and products...")

# Create subcategories and products
for subcat_data in infants_subcategories:
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
    if subcat_slug in infants_products:
        products_data = infants_products[subcat_slug]
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

print("\nKids infants population completed!")
