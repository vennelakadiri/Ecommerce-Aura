import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Create TOP BRANDS category if it doesn't exist
top_brands_category, created = Category.objects.get_or_create(
    slug='top-brands',
    defaults={
        'name': 'TOP BRANDS',
        'is_active': True
    }
)

if created:
    print(f"Created category: {top_brands_category.name}")
else:
    print(f"Category already exists: {top_brands_category.name}")

# Get brands for assignment
brands = list(Brand.objects.all())

# Top brands subcategories to create
top_brands_subcategories = [
    {'name': 'Bath & Body Works', 'slug': 'bath-body-works'},
    {'name': 'THE BODY SHOP', 'slug': 'the-body-shop'},
    {'name': 'Biotique', 'slug': 'biotique'},
    {'name': 'Mamaearth', 'slug': 'mamaearth'},
    {'name': 'MCaffeine', 'slug': 'mcaffeine'},
    {'name': 'Lotus Herbals', 'slug': 'lotus-herbals'},
    {'name': 'LOreal Professionnel', 'slug': 'loreal-professionnel'},
    {'name': 'KAMA AYURVEDA', 'slug': 'kama-ayurveda'},
    {'name': 'Forest Essentials', 'slug': 'forest-essentials'}
]

# Product data for each subcategory
top_brands_products = {
    'bath-body-works': [
        {'name': 'Japanese Cherry Blossom Body Lotion', 'price': 799, 'discount': 599, 'description': 'Luxurious body lotion with Japanese cherry blossom scent. 24-hour moisture.'},
        {'name': 'Lavender & Vanilla Bath Bomb', 'price': 399, 'discount': 299, 'description': 'Relaxing bath bomb with lavender and vanilla. Soothing aromatherapy experience.'},
        {'name': 'Eucalyptus Spearmint Body Wash', 'price': 599, 'discount': 449, 'description': 'Refreshing body wash with eucalyptus and spearmint. Invigorating cleanse.'},
        {'name': 'Rose Water & Vanilla Hand Cream', 'price': 349, 'discount': 249, 'description': 'Nourishing hand cream with rose water and vanilla. Non-greasy formula.'}
    ],
    'the-body-shop': [
        {'name': 'Tea Tree Skin Clearing Face Wash', 'price': 499, 'discount': 399, 'description': 'Clearing face wash with tea tree oil. Fights blemishes and impurities.'},
        {'name': 'Vitamin E Moisturizer', 'price': 699, 'discount': 549, 'description': 'Hydrating vitamin E moisturizer. Protects and nourishes skin.'},
        {'name': 'Shea Butter Body Butter', 'price': 799, 'discount': 649, 'description': 'Rich shea butter body butter. Intensive moisture for dry skin.'},
        {'name': 'Moringa Body Scrub', 'price': 699, 'discount': 549, 'description': 'Exfoliating moringa body scrub. Smooths and revitalizes skin.'}
    ],
    'biotique': [
        {'name': 'Bio Walnut Purifying Scrub', 'price': 299, 'discount': 199, 'description': 'Purifying walnut face scrub. Deep cleanses and exfoliates.'},
        {'name': 'Bio Honey Gel Moisturizer', 'price': 349, 'discount': 249, 'description': 'Lightweight honey gel moisturizer. Hydrates without greasiness.'},
        {'name': 'Bio Cucumber Pore Tightening Toner', 'price': 249, 'discount': 149, 'description': 'Cucumber toner for pore tightening. Refreshes and balances skin.'},
        {'name': 'Bio Carrot Sunscreen SPF 50+', 'price': 399, 'discount': 299, 'description': 'Carrot enriched sunscreen SPF 50+. Natural sun protection.'}
    ],
    'mamaearth': [
        {'name': 'Vitamin C Face Wash', 'price': 399, 'discount': 299, 'description': 'Vitamin C face wash for brightening. Removes dirt and impurities.'},
        {'name': 'Tea Tree Face Serum', 'price': 499, 'discount': 399, 'description': 'Tea tree face serum for acne control. Reduces breakouts and inflammation.'},
        {'name': 'Aloe Vera Gel', 'price': 299, 'discount': 199, 'description': 'Pure aloe vera gel for skin soothing. Calms irritated skin.'},
        {'name': 'Ubtan Face Pack', 'price': 349, 'discount': 249, 'description': 'Traditional ubtan face pack. Brightens and exfoliates skin.'}
    ],
    'mcaffeine': [
        {'name': 'Coffee Body Polishing Oil', 'price': 599, 'discount': 449, 'description': 'Coffee-infused body polishing oil. Nourishes and smooths skin.'},
        {'name': 'Naked & Raw Coffee Face Scrub', 'price': 449, 'discount': 349, 'description': 'Pure coffee face scrub. Exfoliates and revitalizes skin.'},
        {'name': 'Choco Coffee Body Butter', 'price': 549, 'discount': 399, 'description': 'Chocolate coffee body butter. Deeply moisturizes and nourishes.'},
        {'name': 'Coffee De Tan Face Mask', 'price': 399, 'discount': 299, 'description': 'Coffee de-tan face mask. Removes tan and brightens complexion.'}
    ],
    'lotus-herbals': [
        {'name': 'Papaya-N-Cream Skin Exfoliator', 'price': 399, 'discount': 299, 'description': 'Papaya cream exfoliator. Gently removes dead skin cells.'},
        {'name': 'Safe Sun Sunscreen SPF 50', 'price': 449, 'discount': 349, 'description': 'Safe sun sunscreen SPF 50. Broad spectrum protection.'},
        {'name': 'White Glow Skin Whitening Cream', 'price': 499, 'discount': 399, 'description': 'Skin whitening cream with natural actives. Brightens complexion.'},
        {'name': 'Basil & Red Sandalwood Soap', 'price': 199, 'discount': 149, 'description': 'Herbal soap with basil and sandalwood. Purifies and refreshes skin.'}
    ],
    'loreal-professionnel': [
        {'name': 'Absolut Repair Mask', 'price': 899, 'discount': 699, 'description': 'Intensive repair mask for damaged hair. Restores hair health.'},
        {'name': 'Vitamino Color Shampoo', 'price': 699, 'discount': 549, 'description': 'Color-protecting shampoo. Preserves hair color vibrancy.'},
        {'name': 'Serie Expert Prokeratin Refill', 'price': 999, 'discount': 799, 'description': 'Keratin refill treatment. Rebuilds hair structure.'},
        {'name': 'Inforcer Anti-Hair Fall Shampoo', 'price': 599, 'discount': 449, 'description': 'Anti-hair fall shampoo. Strengthens weak hair.'}
    ],
    'kama-ayurveda': [
        {'name': 'Kumkumadi Miraculous Beauty Fluid', 'price': 1499, 'discount': 1199, 'description': 'Traditional kumkumadi beauty fluid. Brightens and rejuvenates skin.'},
        {'name': 'Bringadi Intensive Hair Treatment', 'price': 999, 'discount': 799, 'description': 'Ayurvedic hair treatment oil. Nourishes scalp and hair.'},
        {'name': 'Eladi Keram Skin Care Oil', 'price': 799, 'discount': 599, 'description': 'Herbal skin care oil. Moisturizes and protects skin.'},
        {'name': 'Saffron Dew Moisturizer', 'price': 899, 'discount': 699, 'description': 'Luxurious saffron moisturizer. Hydrates and brightens skin.'}
    ],
    'forest-essentials': [
        {'name': 'Tea Tree Clarifying Shampoo', 'price': 799, 'discount': 649, 'description': 'Clarifying tea tree shampoo. Cleanses and balances scalp.'},
        {'name': 'Silk Soap Delicate Face Wash', 'price': 699, 'discount': 549, 'description': 'Gentle silk soap face wash. Cleanses without stripping.'},
        {'name': 'Soundarya Radiance Cream', 'price': 1799, 'discount': 1399, 'description': 'Luxurious radiance cream. Age-defying and brightening.'},
        {'name': 'Tejal Absolute Moisturizer', 'price': 999, 'discount': 799, 'description': 'Intensive moisturizer for dry skin. Long-lasting hydration.'}
    ]
}

print("Creating TOP BRANDS subcategories and products...")

# Create subcategories and products
for subcat_data in top_brands_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=top_brands_category,
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
    if subcat_slug in top_brands_products:
        products_data = top_brands_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and').replace('.', '')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=top_brands_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='unisex',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"TOPBRANDS-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nTOP BRANDS population completed!")
