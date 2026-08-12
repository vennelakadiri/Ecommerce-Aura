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

# Beauty hair care subcategories to create
haircare_subcategories = [
    {'name': 'Shampoo', 'slug': 'shampoo'},
    {'name': 'Conditioner', 'slug': 'conditioner'},
    {'name': 'Hair Cream', 'slug': 'hair-cream'},
    {'name': 'Hair Oil', 'slug': 'hair-oil'},
    {'name': 'Hair Gel', 'slug': 'hair-gel'},
    {'name': 'Hair Color', 'slug': 'hair-color'},
    {'name': 'Hair Serum', 'slug': 'hair-serum'},
    {'name': 'Hair Accessory', 'slug': 'hair-accessory'}
]

# Product data for each subcategory
haircare_products = {
    'shampoo': [
        {'name': 'Anti-Dandruff Shampoo', 'price': 399, 'discount': 299, 'description': 'Effective anti-dandruff shampoo with zinc pyrithione. Controls flakes and itching.'},
        {'name': 'Moisturizing Shampoo', 'price': 349, 'discount': 249, 'description': 'Hydrating shampoo for dry hair. Contains natural oils and vitamins.'},
        {'name': 'Volumizing Shampoo', 'price': 399, 'discount': 299, 'description': 'Volume-boosting shampoo for fine hair. Adds body and fullness.'},
        {'name': 'Color Protection Shampoo', 'price': 449, 'discount': 349, 'description': 'Color-safe shampoo for treated hair. Protects and prolongs color.'}
    ],
    'conditioner': [
        {'name': 'Deep Conditioning Treatment', 'price': 449, 'discount': 349, 'description': 'Intensive deep conditioner for damaged hair. Restores moisture and shine.'},
        {'name': 'Leave-In Conditioner', 'price': 399, 'discount': 299, 'description': 'Lightweight leave-in conditioner. No-rinse formula for easy styling.'},
        {'name': 'Smoothing Conditioner', 'price': 349, 'discount': 249, 'description': 'Frizz-control smoothing conditioner. Silky smooth finish.'},
        {'name': 'Protein Conditioner', 'price': 399, 'discount': 299, 'description': 'Protein-rich conditioner for strengthening. Repairs damaged hair.'}
    ],
    'hair-cream': [
        {'name': 'Hair Styling Cream', 'price': 299, 'discount': 199, 'description': 'Versatile styling cream for all hair types. Medium hold with natural finish.'},
        {'name': 'Anti-Frizz Hair Cream', 'price': 349, 'discount': 249, 'description': 'Frizz-control cream for humid weather. Long-lasting smoothness.'},
        {'name': 'Heat Protection Cream', 'price': 399, 'discount': 299, 'description': 'Thermal protection cream before styling. Guards against heat damage.'},
        {'name': 'Leave-In Hair Cream', 'price': 349, 'discount': 249, 'description': 'Nourishing leave-in cream. Daily moisture and protection.'}
    ],
    'hair-oil': [
        {'name': 'Argan Hair Oil', 'price': 449, 'discount': 349, 'description': 'Pure argan oil for hair nourishment. Rich in vitamin E and antioxidants.'},
        {'name': 'Coconut Hair Oil', 'price': 349, 'discount': 249, 'description': 'Natural coconut oil for hair growth. Deep conditioning treatment.'},
        {'name': 'Almond Hair Oil', 'price': 399, 'discount': 299, 'description': 'Sweet almond oil for scalp health. Nourishes and strengthens hair.'},
        {'name': 'Hair Growth Oil', 'price': 499, 'discount': 399, 'description': 'Promoting hair growth oil blend. Stimulates follicles for thicker hair.'}
    ],
    'hair-gel': [
        {'name': 'Strong Hold Hair Gel', 'price': 249, 'discount': 199, 'description': 'Maximum hold gel for extreme styles. Long-lasting control.'},
        {'name': 'Light Hold Hair Gel', 'price': 199, 'discount': 149, 'description': 'Flexible light hold gel. Natural movement and shine.'},
        {'name': 'Wet Look Hair Gel', 'price': 299, 'discount': 199, 'description': 'High-shine wet look gel. Glossy finish for styling.'},
        {'name': 'Styling Hair Gel', 'price': 249, 'discount': 199, 'description': 'All-purpose styling gel. Medium hold for everyday use.'}
    ],
    'hair-color': [
        {'name': 'Permanent Hair Color', 'price': 299, 'discount': 249, 'description': 'Long-lasting permanent hair color. Ammonia-free formula.'},
        {'name': 'Semi-Permanent Hair Color', 'price': 249, 'discount': 199, 'description': 'Temporary semi-permanent hair color. Washes out gradually.'},
        {'name': 'Hair Highlights Kit', 'price': 399, 'discount': 299, 'description': 'DIY hair highlighting kit. Professional results at home.'},
        {'name': 'Root Touch-Up Color', 'price': 199, 'discount': 149, 'description': 'Quick root touch-up color. Covers gray roots between coloring.'}
    ],
    'hair-serum': [
        {'name': 'Frizz Control Hair Serum', 'price': 449, 'discount': 349, 'description': 'Anti-frizz serum for smooth hair. Controls flyaways and humidity.'},
        {'name': 'Hair Growth Serum', 'price': 549, 'discount': 449, 'description': 'Stimulating hair growth serum. Promotes thicker, fuller hair.'},
        {'name': 'Silk Protein Hair Serum', 'price': 499, 'discount': 399, 'description': 'Silk protein serum for shine. Adds gloss and smoothness.'},
        {'name': 'Heat Protectant Serum', 'price': 399, 'discount': 299, 'description': 'Thermal protectant serum before styling. Prevents heat damage.'}
    ],
    'hair-accessory': [
        {'name': 'Hair Brush Set', 'price': 499, 'discount': 399, 'description': 'Complete hair brush set. Includes various brush types for styling.'},
        {'name': 'Hair Tie Set', 'price': 199, 'discount': 149, 'description': 'Assorted hair ties and bands. Gentle on hair, no damage.'},
        {'name': 'Hair Clips Set', 'price': 249, 'discount': 199, 'description': 'Decorative hair clips set. Stylish accessories for all occasions.'},
        {'name': 'Hair Dryer', 'price': 999, 'discount': 799, 'description': 'Professional hair dryer with multiple heat settings. Fast drying.'}
    ]
}

print("Creating Beauty hair care subcategories and products...")

# Create subcategories and products
for subcat_data in haircare_subcategories:
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
    if subcat_slug in haircare_products:
        products_data = haircare_products[subcat_slug]
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

print("\nBeauty hair care population completed!")
