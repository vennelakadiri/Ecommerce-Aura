#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
import django
django.setup()

from store.models import Category, SubCategory, Product, Brand
from decimal import Decimal

def create_kids_products():
    print("=== CREATING ALL KIDS PRODUCTS ===")
    
    kids_cat = Category.objects.get(slug='kids')
    
    brands_data = {
        'hm': Brand.objects.get_or_create(slug='hm', defaults={'name': 'H&M'})[0],
        'uspa-kids': Brand.objects.get_or_create(slug='uspa-kids', defaults={'name': 'USPA'})[0],
        'hrx': Brand.objects.get_or_create(slug='hrx', defaults={'name': 'HRX'})[0],
        'pantaloons': Brand.objects.get_or_create(slug='pantaloons', defaults={'name': 'Pantaloons'})[0],
        'gap': Brand.objects.get_or_create(slug='gap', defaults={'name': 'Gap'})[0],
        'zara': Brand.objects.get_or_create(slug='zara', defaults={'name': 'Zara'})[0],
        'mothercare': Brand.objects.get_or_create(slug='mothercare', defaults={'name': 'Mothercare'})[0],
        'nike': Brand.objects.get_or_create(slug='nike', defaults={'name': 'Nike'})[0],
        'adidas': Brand.objects.get_or_create(slug='adidas', defaults={'name': 'Adidas'})[0],
        'puma': Brand.objects.get_or_create(slug='puma', defaults={'name': 'Puma'})[0],
        'reebok': Brand.objects.get_or_create(slug='reebok', defaults={'name': 'Reebok'})[0],
        'under-armour': Brand.objects.get_or_create(slug='under-armour', defaults={'name': 'Under Armour'})[0],
    }
    
    # Boys clothing products
    boys_products = {
        'boys-tshirts-hm': ('H&M Boys T-Shirts', brands_data['hm'], [
            ('Graphic Print T-Shirt', 'Cool graphic print t-shirt for boys', Decimal('799.00'), Decimal('639.00')),
            ('Striped Cotton T-Shirt', 'Comfortable striped cotton t-shirt', Decimal('899.00'), Decimal('719.00')),
            ('Polo Neck T-Shirt', 'Classic polo neck t-shirt', Decimal('999.00'), Decimal('799.00')),
            ('Solid Color T-Shirt', 'Basic solid color t-shirt', Decimal('699.00'), Decimal('559.00')),
            ('Sports Logo T-Shirt', 'Athletic sports logo t-shirt', Decimal('1099.00'), Decimal('879.00')),
        ]),
        'boys-tshirts-uspa': ('USPA Boys T-Shirts', brands_data['uspa-kids'], [
            ('Active Sports T-Shirt', 'Performance active sports t-shirt', Decimal('899.00'), Decimal('719.00')),
            ('Cotton Blend T-Shirt', 'Soft cotton blend t-shirt', Decimal('799.00'), Decimal('639.00')),
            ('Summer Print T-Shirt', 'Vibrant summer print t-shirt', Decimal('999.00'), Decimal('799.00')),
            ('Athletic Fit T-Shirt', 'Athletic fit performance t-shirt', Decimal('1199.00'), Decimal('959.00')),
            ('Casual Day T-Shirt', 'Comfortable casual day t-shirt', Decimal('699.00'), Decimal('559.00')),
        ]),
        'boys-tshirts-hrx': ('HRX Boys T-Shirts', brands_data['hrx'], [
            ('Training T-Shirt', 'Professional training t-shirt', Decimal('1099.00'), Decimal('879.00')),
            ('Performance T-Shirt', 'High-performance training t-shirt', Decimal('1299.00'), Decimal('1039.00')),
            ('Quick Dry T-Shirt', 'Quick-dry fabric t-shirt', Decimal('999.00'), Decimal('799.00')),
            ('Athletic T-Shirt', 'Athletic performance t-shirt', Decimal('899.00'), Decimal('719.00')),
            ('Sportswear T-Shirt', 'Premium sportswear T-shirt', Decimal('1499.00'), Decimal('1199.00')),
        ]),
        'boys-tshirts-pantaloons': ('Pantaloons Boys T-Shirts', brands_data['pantaloons'], [
            ('Casual Cotton T-Shirt', 'Everyday casual cotton t-shirt', Decimal('799.00'), Decimal('639.00')),
            ('Printed T-Shirt', 'Fun printed design t-shirt', Decimal('899.00'), Decimal('719.00')),
            ('Solid Color T-Shirt', 'Classic solid color t-shirt', Decimal('699.00'), Decimal('559.00')),
            ('Striped T-Shirt', 'Trendy striped pattern t-shirt', Decimal('999.00'), Decimal('799.00')),
            ('Graphic T-Shirt', 'Cool graphic design t-shirt', Decimal('1099.00'), Decimal('879.00')),
        ]),
        'boys-shirts': ('Boys Shirts', brands_data['gap'], [
            ('Formal Dress Shirt', 'Elegant formal dress shirt', Decimal('1299.00'), Decimal('1039.00')),
            ('Casual Button Shirt', 'Comfortable casual button shirt', Decimal('999.00'), Decimal('799.00')),
            ('Checkered Shirt', 'Classic checkered pattern shirt', Decimal('1199.00'), Decimal('959.00')),
            ('Plaid Shirt', 'Trendy plaid pattern shirt', Decimal('1099.00'), Decimal('879.00')),
            ('Denim Shirt', 'Stylish denim shirt', Decimal('1399.00'), Decimal('1119.00')),
        ]),
        'boys-shorts': ('Boys Shorts', brands_data['nike'], [
            ('Athletic Shorts', 'Performance athletic shorts', Decimal('899.00'), Decimal('719.00')),
            ('Cargo Shorts', 'Functional cargo shorts', Decimal('999.00'), Decimal('799.00')),
            ('Denim Shorts', 'Casual denim shorts', Decimal('1099.00'), Decimal('879.00')),
            ('Board Shorts', 'Beach-ready board shorts', Decimal('799.00'), Decimal('639.00')),
            ('Sports Shorts', 'Quick-dry sports shorts', Decimal('1199.00'), Decimal('959.00')),
        ]),
        'boys-jeans': ('Boys Jeans', brands_data['gap'], [
            ('Slim Fit Jeans', 'Modern slim fit jeans', Decimal('1599.00'), Decimal('1279.00')),
            ('Regular Fit Jeans', 'Classic regular fit jeans', Decimal('1499.00'), Decimal('1199.00')),
            ('Bootcut Jeans', 'Traditional bootcut jeans', Decimal('1699.00'), Decimal('1359.00')),
            ('Straight Leg Jeans', 'Straight leg style jeans', Decimal('1399.00'), Decimal('1119.00')),
            ('Distressed Jeans', 'Fashion distressed jeans', Decimal('1799.00'), Decimal('1439.00')),
        ]),
        'boys-trousers': ('Boys Trousers', brands_data['hm'], [
            ('Chino Trousers', 'Classic chino trousers', Decimal('1299.00'), Decimal('1039.00')),
            ('Formal Trousers', 'Elegant formal trousers', Decimal('1499.00'), Decimal('1199.00')),
            ('Casual Trousers', 'Comfortable casual trousers', Decimal('1199.00'), Decimal('959.00')),
            ('Cotton Trousers', 'Soft cotton trousers', Decimal('1099.00'), Decimal('879.00')),
            ('Dress Trousers', 'Formal dress trousers', Decimal('1699.00'), Decimal('1359.00')),
        ]),
        'boys-sets': ('Boys Clothing Sets', brands_data['zara'], [
            ('T-Shirt & Shorts Set', 'Complete t-shirt and shorts set', Decimal('1799.00'), Decimal('1439.00')),
            ('Shirt & Pants Set', 'Formal shirt and pants set', Decimal('2199.00'), Decimal('1759.00')),
            ('Casual Outfit Set', 'Casual everyday outfit set', Decimal('1999.00'), Decimal('1599.00')),
            ('Party Wear Set', 'Stylish party wear set', Decimal('2499.00'), Decimal('1999.00')),
            ('School Uniform Set', 'Complete school uniform set', Decimal('1599.00'), Decimal('1279.00')),
        ]),
        'boys-ethnic': ('Boys Ethnic Wear', brands_data['pantaloons'], [
            ('Kurta Pyjama Set', 'Traditional kurta pyjama set', Decimal('1999.00'), Decimal('1599.00')),
            ('Sherwani Set', 'Elegant sherwani set', Decimal('2999.00'), Decimal('2399.00')),
            ('Nehru Jacket Set', 'Classic nehru jacket set', Decimal('2499.00'), Decimal('1999.00')),
            ('Dhoti Kurta Set', 'Traditional dhoti kurta set', Decimal('1799.00'), Decimal('1439.00')),
            ('Ethnic Party Wear', 'Festive ethnic party wear', Decimal('3299.00'), Decimal('2639.00')),
        ]),
        'boys-track-pants': ('Track Pants & Pyjamas', brands_data['nike'], [
            ('Track Pants', 'Athletic track pants', Decimal('999.00'), Decimal('799.00')),
            ('Cotton Pyjamas', 'Comfortable cotton pyjamas', Decimal('799.00'), Decimal('639.00')),
            ('Fleece Track Pants', 'Warm fleece track pants', Decimal('1299.00'), Decimal('1039.00')),
            ('Lounge Pants', 'Relaxed lounge pants', Decimal('899.00'), Decimal('719.00')),
            ('Sleep Pyjamas', 'Cozy sleep pyjamas', Decimal('699.00'), Decimal('559.00')),
        ]),
        'boys-jackets': ('Jacket, Sweater & Sweatshirts', brands_data['adidas'], [
            ('Winter Jacket', 'Warm winter jacket', Decimal('2499.00'), Decimal('1999.00')),
            ('Hooded Sweatshirt', 'Comfortable hooded sweatshirt', Decimal('1299.00'), Decimal('1039.00')),
            ('Knit Sweater', 'Cozy knit sweater', Decimal('1599.00'), Decimal('1279.00')),
            ('Windbreaker Jacket', 'Lightweight windbreaker jacket', Decimal('1899.00'), Decimal('1519.00')),
            ('Fleece Jacket', 'Soft fleece jacket', Decimal('1999.00'), Decimal('1599.00')),
        ]),
        'boys-party': ('Boys Party Wear', brands_data['zara'], [
            ('Party Suit', 'Elegant party suit', Decimal('3499.00'), Decimal('2799.00')),
            ('Formal Blazer', 'Stylish formal blazer', Decimal('2999.00'), Decimal('2399.00')),
            ('Dress Shirt Set', 'Complete dress shirt set', Decimal('1999.00'), Decimal('1599.00')),
            ('Party Outfit', 'Trendy party outfit', Decimal('2499.00'), Decimal('1999.00')),
            ('Festive Wear', 'Traditional festive wear', Decimal('2799.00'), Decimal('2239.00')),
        ]),
        'boys-innerwear': ('Boys Innerwear & Thermals', brands_data['gap'], [
            ('Cotton Briefs Pack', 'Pack of cotton briefs', Decimal('599.00'), Decimal('479.00')),
            ('Thermal Wear Set', 'Warm thermal wear set', Decimal('999.00'), Decimal('799.00')),
            ('Boxer Briefs Pack', 'Pack of boxer briefs', Decimal('699.00'), Decimal('559.00')),
            ('Vest Undershirt', 'Comfortable vest undershirt', Decimal('499.00'), Decimal('399.00')),
            ('Long Johns Set', 'Warm long johns set', Decimal('1299.00'), Decimal('1039.00')),
        ]),
        'boys-nightwear': ('Boys Nightwear & Loungewear', brands_data['hm'], [
            ('Pajama Set', 'Comfortable pajama set', Decimal('899.00'), Decimal('719.00')),
            ('Lounge Shorts Set', 'Casual lounge shorts set', Decimal('799.00'), Decimal('639.00')),
            ('Sleep Shirt', 'Cozy sleep shirt', Decimal('699.00'), Decimal('559.00')),
            ('Lounge Pants', 'Relaxed lounge pants', Decimal('999.00'), Decimal('799.00')),
            ('Night Suit Set', 'Complete night suit set', Decimal('1099.00'), Decimal('879.00')),
        ]),
        'boys-value-packs': ('Boys Value Packs', brands_data['gap'], [
            ('3 T-Shirt Pack', 'Pack of 3 t-shirts', Decimal('1999.00'), Decimal('1599.00')),
            ('2 Shorts Pack', 'Pack of 2 shorts', Decimal('1599.00'), Decimal('1279.00')),
            ('Mix Clothing Pack', 'Mixed clothing value pack', Decimal('2499.00'), Decimal('1999.00')),
            ('School Essentials Pack', 'School essentials clothing pack', Decimal('2999.00'), Decimal('2399.00')),
            ('Seasonal Pack', 'Seasonal clothing pack', Decimal('3499.00'), Decimal('2799.00')),
        ]),
    }
    
    # Girls clothing products
    girls_products = {
        'girls-dresses-zara': ('Zara Girls Dresses', brands_data['zara'], [
            ('Floral Print Dress', 'Beautiful floral print dress', Decimal('1299.00'), Decimal('1039.00')),
            ('Party Dress', 'Elegant party dress', Decimal('1599.00'), Decimal('1279.00')),
            ('Summer Dress', 'Light summer dress', Decimal('1199.00'), Decimal('959.00')),
            ('Casual Day Dress', 'Comfortable casual day dress', Decimal('999.00'), Decimal('799.00')),
            ('Formal Dress', 'Classic formal dress', Decimal('1899.00'), Decimal('1519.00')),
        ]),
        'girls-dresses-uspa': ('USPA Girls Dresses', brands_data['uspa-kids'], [
            ('Sporty Dress', 'Athletic sporty dress', Decimal('1199.00'), Decimal('959.00')),
            ('Cotton Summer Dress', 'Breathable cotton summer dress', Decimal('1099.00'), Decimal('879.00')),
            ('Printed Party Dress', 'Fun printed party dress', Decimal('1399.00'), Decimal('1119.00')),
            ('Casual Knit Dress', 'Comfortable casual knit dress', Decimal('999.00'), Decimal('799.00')),
            ('Elegant Evening Dress', 'Stylish evening dress', Decimal('1699.00'), Decimal('1359.00')),
        ]),
        'girls-dresses-mothercare': ('Mothercare Girls Dresses', brands_data['mothercare'], [
            ('Baby Girl Dress', 'Cute baby girl dress', Decimal('899.00'), Decimal('719.00')),
            ('Toddler Party Dress', 'Adorable toddler party dress', Decimal('1099.00'), Decimal('879.00')),
            ('Floral Summer Dress', 'Sweet floral summer dress', Decimal('999.00'), Decimal('799.00')),
            ('Princess Dress', 'Beautiful princess dress', Decimal('1299.00'), Decimal('1039.00')),
            ('Special Occasion Dress', 'Elegant special occasion dress', Decimal('1499.00'), Decimal('1199.00')),
        ]),
        'girls-tops': ('Girls Tops', brands_data['hm'], [
            ('Cotton Top', 'Soft cotton top', Decimal('799.00'), Decimal('639.00')),
            ('Printed T-Shirt', 'Fun printed t-shirt', Decimal('699.00'), Decimal('559.00')),
            ('Tank Top', 'Casual tank top', Decimal('599.00'), Decimal('479.00')),
            ('Graphic Top', 'Cool graphic top', Decimal('899.00'), Decimal('719.00')),
            ('Blouse Top', 'Elegant blouse top', Decimal('999.00'), Decimal('799.00')),
        ]),
        'girls-tshirts': ('Girls T-Shirts', brands_data['gap'], [
            ('Girls Graphic Tee', 'Fun girls graphic t-shirt', Decimal('699.00'), Decimal('559.00')),
            ('Cotton Casual Tee', 'Comfortable cotton casual tee', Decimal('599.00'), Decimal('479.00')),
            ('Printed Girls Tee', 'Colorful printed girls tee', Decimal('799.00'), Decimal('639.00')),
            ('Girls Logo Tee', 'Girls logo t-shirt', Decimal('899.00'), Decimal('719.00')),
            ('Girls Sports Tee', 'Athletic girls sports tee', Decimal('999.00'), Decimal('799.00')),
        ]),
        'girls-sets': ('Girls Clothing Sets', brands_data['zara'], [
            ('Top & Skirt Set', 'Cute top and skirt set', Decimal('1599.00'), Decimal('1279.00')),
            ('Dress & Cardigan Set', 'Elegant dress and cardigan set', Decimal('1899.00'), Decimal('1519.00')),
            ('Casual Outfit Set', 'Comfortable casual outfit set', Decimal('1399.00'), Decimal('1119.00')),
            ('Party Set', 'Stylish party set', Decimal('2199.00'), Decimal('1759.00')),
            ('School Set', 'Complete school set', Decimal('1799.00'), Decimal('1439.00')),
        ]),
        'girls-lehenga': ('Girls Lehenga Choli', brands_data['pantaloons'], [
            ('Girls Lehenga Set', 'Traditional girls lehenga set', Decimal('2499.00'), Decimal('1999.00')),
            ('Kids Lehenga', 'Cute kids lehenga', Decimal('1999.00'), Decimal('1599.00')),
            ('Party Lehenga', 'Festive party lehenga', Decimal('2999.00'), Decimal('2399.00')),
            ('Simple Lehenga', 'Simple elegant lehenga', Decimal('1799.00'), Decimal('1439.00')),
            ('Designer Lehenga', 'Designer girls lehenga', Decimal('3499.00'), Decimal('2799.00')),
        ]),
        'girls-kurta': ('Girls Kurta Sets', brands_data['pantaloons'], [
            ('Girls Kurta Set', 'Traditional girls kurta set', Decimal('1899.00'), Decimal('1519.00')),
            ('Kids Kurta', 'Cute kids kurta', Decimal('1599.00'), Decimal('1279.00')),
            ('Party Kurta', 'Festive party kurta', Decimal('2299.00'), Decimal('1839.00')),
            ('Simple Kurta', 'Simple elegant kurta', Decimal('1399.00'), Decimal('1119.00')),
            ('Designer Kurta', 'Designer girls kurta', Decimal('2799.00'), Decimal('2239.00')),
        ]),
        'girls-party': ('Girls Party Wear', brands_data['zara'], [
            ('Party Gown', 'Elegant party gown', Decimal('2499.00'), Decimal('1999.00')),
            ('Cocktail Dress', 'Stylish cocktail dress', Decimal('2199.00'), Decimal('1759.00')),
            ('Birthday Dress', 'Special birthday dress', Decimal('1899.00'), Decimal('1519.00')),
            ('Festival Outfit', 'Traditional festival outfit', Decimal('2999.00'), Decimal('2399.00')),
            ('Party Set', 'Complete party set', Decimal('3299.00'), Decimal('2639.00')),
        ]),
        'girls-dungarees': ('Girls Dungarees & Jumpsuits', brands_data['hm'], [
            ('Denim Dungarees', 'Casual denim dungarees', Decimal('999.00'), Decimal('799.00')),
            ('Printed Jumpsuit', 'Fun printed jumpsuit', Decimal('1199.00'), Decimal('959.00')),
            ('Cotton Dungarees', 'Comfortable cotton dungarees', Decimal('899.00'), Decimal('719.00')),
            ('Girls Jumpsuit', 'Cute girls jumpsuit', Decimal('1099.00'), Decimal('879.00')),
            ('Play Dungarees', 'Playful dungarees', Decimal('1299.00'), Decimal('1039.00')),
        ]),
        'girls-skirts': ('Girls Skirts & Shorts', brands_data['gap'], [
            ('Cotton Skirt', 'Comfortable cotton skirt', Decimal('799.00'), Decimal('639.00')),
            ('Denim Skirt', 'Casual denim skirt', Decimal('899.00'), Decimal('719.00')),
            ('Short Skirt', 'Trendy short skirt', Decimal('699.00'), Decimal('559.00')),
            ('Girls Shorts', 'Cute girls shorts', Decimal('599.00'), Decimal('479.00')),
            ('Play Skirt', 'Fun play skirt', Decimal('799.00'), Decimal('639.00')),
        ]),
        'girls-leggings': ('Girls Tights & Leggings', brands_data['nike'], [
            ('Cotton Leggings', 'Soft cotton leggings', Decimal('699.00'), Decimal('559.00')),
            ('Printed Tights', 'Colorful printed tights', Decimal('799.00'), Decimal('639.00')),
            ('Athletic Leggings', 'Performance athletic leggings', Decimal('899.00'), Decimal('719.00')),
            ('Girls Tights', 'Comfortable girls tights', Decimal('599.00'), Decimal('479.00')),
            ('Play Leggings', 'Fun play leggings', Decimal('699.00'), Decimal('559.00')),
        ]),
        'girls-jeans': ('Girls Jeans, Trousers & Capris', brands_data['hm'], [
            ('Girls Slim Jeans', 'Girls slim fit jeans', Decimal('1299.00'), Decimal('1039.00')),
            ('Girls Capris', 'Cute girls capris', Decimal('999.00'), Decimal('799.00')),
            ('Girls Trousers', 'Girls casual trousers', Decimal('1099.00'), Decimal('879.00')),
            ('Girls Bootcut Jeans', 'Girls bootcut jeans', Decimal('1199.00'), Decimal('959.00')),
            ('Girls Straight Jeans', 'Girls straight leg jeans', Decimal('1399.00'), Decimal('1119.00')),
        ]),
        'girls-jackets': ('Girls Jacket, Sweater & Sweatshirts', brands_data['gap'], [
            ('Girls Winter Jacket', 'Warm girls winter jacket', Decimal('1999.00'), Decimal('1599.00')),
            ('Girls Sweatshirt', 'Cute girls sweatshirt', Decimal('899.00'), Decimal('719.00')),
            ('Girls Sweater', 'Cozy girls sweater', Decimal('1299.00'), Decimal('1039.00')),
            ('Girls Hoodie', 'Girls casual hoodie', Decimal('999.00'), Decimal('799.00')),
            ('Girls Cardigan', 'Girls stylish cardigan', Decimal('1499.00'), Decimal('1199.00')),
        ]),
        'girls-innerwear': ('Girls Innerwear & Thermals', brands_data['gap'], [
            ('Girls Briefs Pack', 'Pack of girls briefs', Decimal('499.00'), Decimal('399.00')),
            ('Girls Camisole Set', 'Girls camisole set', Decimal('599.00'), Decimal('479.00')),
            ('Girls Thermal Set', 'Girls thermal wear set', Decimal('799.00'), Decimal('639.00')),
            ('Girls Underwear Set', 'Girls underwear set', Decimal('699.00'), Decimal('559.00')),
            ('Girls Sleep Set', 'Girls sleep set', Decimal('599.00'), Decimal('479.00')),
        ]),
        'girls-nightwear': ('Girls Nightwear & Loungewear', brands_data['hm'], [
            ('Girls Nightgown', 'Cute girls nightgown', Decimal('799.00'), Decimal('639.00')),
            ('Girls Pajama Set', 'Girls pajama set', Decimal('699.00'), Decimal('559.00')),
            ('Girls Lounge Set', 'Girls lounge set', Decimal('899.00'), Decimal('719.00')),
            ('Girls Sleep Shorts', 'Girls sleep shorts', Decimal('599.00'), Decimal('479.00')),
            ('Girls Night Set', 'Girls night set', Decimal('999.00'), Decimal('799.00')),
        ]),
        'girls-packs': ('Girls Value Packs', brands_data['gap'], [
            ('Girls 3 Dress Pack', 'Pack of 3 girls dresses', Decimal('2999.00'), Decimal('2399.00')),
            ('Girls 2 Top Pack', 'Pack of 2 girls tops', Decimal('1599.00'), Decimal('1279.00')),
            ('Girls Mix Pack', 'Girls mix clothing pack', Decimal('2499.00'), Decimal('1999.00')),
            ('Girls School Pack', 'Girls school essentials pack', Decimal('3499.00'), Decimal('2799.00')),
            ('Girls Seasonal Pack', 'Girls seasonal pack', Decimal('3999.00'), Decimal('3199.00')),
        ]),
    }
    
    # Combine all products
    all_products = {**boys_products, **girls_products}
    
    # Create products for each subcategory
    for sub_slug, (sub_name, brand, products_data) in all_products.items():
        # Get or create subcategory
        subcategory, created = SubCategory.objects.get_or_create(
            slug=sub_slug,
            category=kids_cat,
            defaults={'name': sub_name}
        )
        
        if created:
            print(f"Created subcategory: {sub_name}")
        else:
            print(f"Using existing subcategory: {sub_name}")
        
        # Check current product count
        current_count = Product.objects.filter(subcategory=subcategory, is_active=True).count()
        needed_count = max(0, 4 - current_count)
        
        print(f"  Current products: {current_count}")
        
        if needed_count > 0:
            print(f"  Adding {needed_count} more products:")
            for i, (name, description, price, discounted_price) in enumerate(products_data):
                if i >= current_count:  # Only add if we don't already have this many products
                    product, created = Product.objects.get_or_create(
                        slug=f"{sub_slug}-{i+1}",
                        defaults={
                            'name': name,
                            'description': description,
                            'short_description': f"{name} - {sub_name}",
                            'category': kids_cat,
                            'subcategory': subcategory,
                            'brand': brand,
                            'gender': kids_cat.slug,
                            'price': price,
                            'discounted_price': discounted_price,
                            'sku': f"{sub_slug.upper()}-{i+1:04d}",
                            'stock_quantity': 50,
                            'is_active': True,
                        }
                    )
                    if created:
                        print(f"    Created: {name} (₹{price:.2f} → ₹{discounted_price:.2f})")
        else:
            print(f"  Already has {current_count}+ products")
    
    print("\n=== COMPLETED ===")
    print("All kids products created successfully!")

if __name__ == "__main__":
    create_kids_products()
