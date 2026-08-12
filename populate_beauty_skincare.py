import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Get beauty category and brands
beauty_category = Category.objects.get(slug='beauty')
brands = list(Brand.objects.all())

# Beauty skincare subcategories to create
skincare_subcategories = [
    {'name': 'Face Moisturiser', 'slug': 'face-moisturiser'},
    {'name': 'Cleanser', 'slug': 'cleanser'},
    {'name': 'Masks & Peel', 'slug': 'masks-peel'},
    {'name': 'Sunscreen', 'slug': 'sunscreen'},
    {'name': 'Serum', 'slug': 'serum'},
    {'name': 'Face Wash', 'slug': 'face-wash'},
    {'name': 'Eye Cream', 'slug': 'eye-cream'},
    {'name': 'Lip Balm', 'slug': 'lip-balm'},
    {'name': 'Body Lotion', 'slug': 'body-lotion'},
    {'name': 'Body Wash', 'slug': 'body-wash'},
    {'name': 'Body Scrub', 'slug': 'body-scrub'},
    {'name': 'Hand Cream', 'slug': 'hand-cream'}
]

# Product data for each subcategory
skincare_products = {
    'face-moisturiser': [
        {'name': 'Hydrating Face Moisturiser', 'price': 699, 'discount': 549, 'description': 'Deep hydrating moisturizer with hyaluronic acid. 24-hour moisture lock.'},
        {'name': 'Anti-Aging Face Moisturiser', 'price': 899, 'discount': 699, 'description': 'Anti-aging moisturizer with retinol. Reduces fine lines and wrinkles.'},
        {'name': 'Oil-Free Face Moisturiser', 'price': 599, 'discount': 449, 'description': 'Lightweight oil-free moisturizer for oily skin. Non-greasy formula.'},
        {'name': 'Vitamin C Face Moisturiser', 'price': 799, 'discount': 599, 'description': 'Brightening vitamin C moisturizer. Evens skin tone and adds radiance.'}
    ],
    'cleanser': [
        {'name': 'Gentle Face Cleanser', 'price': 499, 'discount': 399, 'description': 'Mild daily face cleanser for all skin types. pH balanced formula.'},
        {'name': 'Deep Cleansing Foam', 'price': 549, 'discount': 449, 'description': 'Deep cleansing foam removes impurities. Refreshing and purifying.'},
        {'name': 'Micellar Water Cleanser', 'price': 449, 'discount': 349, 'description': 'Micellar water cleanser for sensitive skin. No-rinse formula.'},
        {'name': 'Exfoliating Cleanser', 'price': 599, 'discount': 449, 'description': 'Gentle exfoliating cleanser with natural beads. Smooths skin texture.'}
    ],
    'masks-peel': [
        {'name': 'Hydrating Face Mask', 'price': 399, 'discount': 299, 'description': 'Intensive hydrating face mask. Instant moisture boost.'},
        {'name': 'Clay Detox Mask', 'price': 449, 'discount': 349, 'description': 'Deep cleansing clay mask. Removes toxins and impurities.'},
        {'name': 'Peel Off Mask', 'price': 349, 'discount': 249, 'description': 'Exfoliating peel-off mask. Removes dead skin cells.'},
        {'name': 'Overnight Sleeping Mask', 'price': 549, 'discount': 399, 'description': 'Overnight recovery mask. Wake up to refreshed skin.'}
    ],
    'sunscreen': [
        {'name': 'SPF 50 Sunscreen', 'price': 599, 'discount': 449, 'description': 'Broad spectrum SPF 50 sunscreen. Maximum sun protection.'},
        {'name': 'Matte Finish Sunscreen', 'price': 549, 'discount': 399, 'description': 'Oil-free matte sunscreen. Non-shiny protection.'},
        {'name': 'Tinted Sunscreen', 'price': 649, 'discount': 499, 'description': 'Tinted sunscreen with light coverage. Natural-looking protection.'},
        {'name': 'Waterproof Sunscreen', 'price': 699, 'discount': 549, 'description': 'Water-resistant sunscreen for outdoor activities. Long-lasting protection.'}
    ],
    'serum': [
        {'name': 'Vitamin C Serum', 'price': 899, 'discount': 699, 'description': 'Brightening vitamin C serum. Reduces dark spots and pigmentation.'},
        {'name': 'Hyaluronic Acid Serum', 'price': 799, 'discount': 599, 'description': 'Hydrating hyaluronic acid serum. Plumps and moisturizes skin.'},
        {'name': 'Retinol Serum', 'price': 999, 'discount': 799, 'description': 'Anti-aging retinol serum. Improves skin texture and tone.'},
        {'name': 'Niacinamide Serum', 'price': 699, 'discount': 549, 'description': 'Pore-refining niacinamide serum. Minimizes pores and controls oil.'}
    ],
    'face-wash': [
        {'name': 'Gentle Face Wash', 'price': 349, 'discount': 249, 'description': 'Mild daily face wash for sensitive skin. Cleanses without stripping.'},
        {'name': 'Foaming Face Wash', 'price': 399, 'discount': 299, 'description': 'Rich foaming face wash for deep cleansing. Refreshing formula.'},
        {'name': 'Herbal Face Wash', 'price': 449, 'discount': 349, 'description': 'Natural herbal face wash with botanical extracts. Gentle cleansing.'},
        {'name': 'Anti-Acne Face Wash', 'price': 499, 'discount': 399, 'description': 'Acne-fighting face wash with salicylic acid. Clears breakouts.'}
    ],
    'eye-cream': [
        {'name': 'Anti-Wrinkle Eye Cream', 'price': 799, 'discount': 599, 'description': 'Anti-aging eye cream for fine lines. Reduces crow\'s feet.'},
        {'name': 'Dark Circle Eye Cream', 'price': 699, 'discount': 549, 'description': 'Brightening eye cream for dark circles. Vitamin C formula.'},
        {'name': 'Hydrating Eye Cream', 'price': 599, 'discount': 449, 'description': 'Moisturizing eye cream for dry eyes. Hyaluronic acid enriched.'},
        {'name': 'Under Eye Gel', 'price': 649, 'discount': 499, 'description': 'Cooling under eye gel. Reduces puffiness and refreshes.'}
    ],
    'lip-balm': [
        {'name': 'Moisturizing Lip Balm', 'price': 199, 'discount': 149, 'description': 'Deep moisturizing lip balm with shea butter. Long-lasting hydration.'},
        {'name': 'SPF Lip Balm', 'price': 249, 'discount': 199, 'description': 'Sun protection lip balm with SPF 15. UV protection for lips.'},
        {'name': 'Tinted Lip Balm', 'price': 299, 'discount': 199, 'description': 'Tinted lip balm with natural color. Subtle enhancement.'},
        {'name': 'Medicated Lip Balm', 'price': 199, 'discount': 149, 'description': 'Healing medicated lip balm. Soothes chapped lips.'}
    ],
    'body-lotion': [
        {'name': 'Deep Moisture Body Lotion', 'price': 449, 'discount': 349, 'description': 'Intensive moisturizing body lotion. 24-hour hydration.'},
        {'name': 'Lightweight Body Lotion', 'price': 399, 'discount': 299, 'description': 'Quick-absorbing lightweight body lotion. Non-greasy formula.'},
        {'name': 'Aloe Vera Body Lotion', 'price': 349, 'discount': 249, 'description': 'Soothing aloe vera body lotion. Calms and moisturizes skin.'},
        {'name': 'Firming Body Lotion', 'price': 549, 'discount': 399, 'description': 'Skin-firming body lotion with collagen. Improves skin elasticity.'}
    ],
    'body-wash': [
        {'name': 'Moisturizing Body Wash', 'price': 349, 'discount': 249, 'description': 'Hydrating body wash with glycerin. Cleanses without drying.'},
        {'name': 'Exfoliating Body Wash', 'price': 399, 'discount': 299, 'description': 'Gentle exfoliating body wash. Removes dead skin cells.'},
        {'name': 'Herbal Body Wash', 'price': 449, 'discount': 349, 'description': 'Natural herbal body wash. Botanical ingredients for gentle cleansing.'},
        {'name': 'Antibacterial Body Wash', 'price': 399, 'discount': 299, 'description': 'Antibacterial body wash for clean skin. Protects against germs.'}
    ],
    'body-scrub': [
        {'name': 'Sugar Body Scrub', 'price': 399, 'discount': 299, 'description': 'Exfoliating sugar body scrub. Smooths and softens skin.'},
        {'name': 'Salt Body Scrub', 'price': 349, 'discount': 249, 'description': 'Detoxifying salt body scrub. Purifies and revitalizes skin.'},
        {'name': 'Coffee Body Scrub', 'price': 449, 'discount': 349, 'description': 'Cellulite-reducing coffee body scrub. Stimulates circulation.'},
        {'name': 'Herbal Body Scrub', 'price': 399, 'discount': 299, 'description': 'Natural herbal body scrub. Gentle exfoliation with botanicals.'}
    ],
    'hand-cream': [
        {'name': 'Intensive Hand Cream', 'price': 299, 'discount': 199, 'description': 'Deep moisturizing hand cream for dry hands. Long-lasting protection.'},
        {'name': 'Antibacterial Hand Cream', 'price': 349, 'discount': 249, 'description': 'Protective antibacterial hand cream. Kills germs while moisturizing.'},
        {'name': 'Rapid Absorption Hand Cream', 'price': 249, 'discount': 199, 'description': 'Quick-absorbing hand cream. Non-greasy formula.'},
        {'name': 'Night Repair Hand Cream', 'price': 399, 'discount': 299, 'description': 'Overnight repair hand cream. Restores dry hands while sleeping.'}
    ]
}

print("Creating Beauty skincare subcategories and products...")

# Create subcategories and products
for subcat_data in skincare_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=beauty_category,
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
    if subcat_slug in skincare_products:
        products_data = skincare_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=beauty_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='unisex',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"BEAUTY-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nBeauty skincare population completed!")
