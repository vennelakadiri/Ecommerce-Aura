import os
import sys
import django
import uuid

sys.path.insert(0, r"c:\Users\kadirivennela\OneDrive\Miniproject")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Category, Brand, Product, ProductImage, Banner

# 1. User-specified custom URLs
USER_URLS = {
    'Minimalist Cardholder': 'https://i.etsystatic.com/49382644/r/il/b900df/5652218918/il_1588xN.5652218918_ba0l.jpg',
    'Premium Wallet': 'https://i.pinimg.com/originals/aa/b7/d9/aab7d9863114e62f9d7f092e2078af92.jpg',
    'Leather Wallet': 'https://theawesomer.com/photos/2024/12/ridge_leather_wallets_4.jpg',
    'Leather Belt': 'https://i5.walmartimages.com/seo/Men-s-Casual-Genuine-Leather-Jeans-Belts-1-1-2-Wide-Work-Dress-Belt-for-Men_5f86c437-61dd-48e1-bd18-504102b775eb.80c45d4a39038e3e7df4f5f0595eb730.jpeg',
    'Classic Leather Belt': 'https://i5.walmartimages.com/seo/Men-s-Casual-Genuine-Leather-Jeans-Belts-1-1-2-Wide-Work-Dress-Belt-for-Men_5f86c437-61dd-48e1-bd18-504102b775eb.80c45d4a39038e3e7df4f5f0595eb730.jpeg',
    'Slim Fit Jeans': 'https://i5.walmartimages.com/seo/Men-s-Lee-Extreme-Motion-MVP-Straight-Leg-Slim-Fit-Jeans-Color-Baritt-Size-42X30_a959aeb5-94df-4a85-a8b4-c5b401822559.98969c530cf8465ddffcfc12a7bd17e1.jpeg',
    'Silk Tie': 'https://media.neimanmarcus.com/f_auto,q_auto/01/nm_4489966_100551_m',
    'Business Trousers': 'https://i5.walmartimages.com/seo/TFEOQRY-Business-Trousers-for-Men-Solid-Color-Button-Down-Full-Length-Pants-Medium-Waist-Trousers-Dark-Gray_3beb93d0-b64c-4125-b412-d7a0aec0e0d8.245f48fbead3aed1d54799909c28e039.jpeg',
    'Evening Clutch': 'https://i.etsystatic.com/40778318/r/il/adcd3b/4681438375/il_fullxfull.4681438375_kjjx.jpg',
    'Yoga Pants': 'https://i5.walmartimages.com/seo/BKQCNKM-Yoga-Pants-Pockets-Women-Flare-Womens-High-Waist-Pant-Soft-Sport-Leggings-Workout-Running-Trousers-Gray-XXL_403959ad-1c23-4876-a93c-b9d457341801.42cd74abefa52f8034b9de3d06eb13c0.jpeg',
    'Fashion Scarf': 'https://i5.walmartimages.com/seo/Baqcunre-Clearance-Silk-Scarf-Scarfs-for-Women-Lightweight-Print-Floral-Pattern-Scarf-Shawl-Fashion-Scarves-Shawls-And-Wraps-for-Spring_e474ed02-cb5a-41cf-8390-3fa4b575826e.9065a0c247b629465c12aa0f1e0336e1.jpeg?odnHeight=576&odnWidth=576&odnBg=FFFFFF',
    'Floral Summer Dress': 'https://www.graceandlace.com/cdn/shop/files/FloralSummerMaxiDress-1.jpg?v=1715707860',
    'Flats': 'https://i5.walmartimages.com/seo/Obtaom-Women-s-Round-Toe-Ballet-Flats-Cute-Textile-Ballerina-Flats-Comfortable-Faux-Leather-Insole-Low-Heels-Dress-Shoes-For-Ladies-Black-US9_a45effbe-dc04-428c-af72-ef845776aef2.8053db39c593949cd798e0dc0f50e99b.jpeg?odnHeight=424&odnWidth=424&odnBg=FFFFFF',
    'Premium Chronograph Watch': 'https://delawrence.pk/cdn/shop/files/IMG_8636.jpg?v=1703853577&width=953',
    'Urban Streetwear Hoodie': 'https://i.pinimg.com/736x/ac/ee/a2/aceea245fd311fe129e3e58ed1107a06.jpg',
    'Summer Collection Dress': 'https://images.esellerpro.com/2355/I/213/505/JM%20D668.jpg'
}

# General high-resolution images for items not in USER_URLS
GENERAL_IMAGE_MAP = {
    'Designer Sunglasses': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=500&h=500&fit=crop&q=80',
    'Smart Watch Pro': 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&h=500&fit=crop&q=80',
    'Sports Watch Digital': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=500&h=500&fit=crop&q=80',
    'Travel Duffle Bag': 'https://images.unsplash.com/photo-1547949003-9792a18a2601?w=500&h=500&fit=crop&q=80',
    'Aviator Sunglasses': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop&q=80',
    'Canvas Messenger Bag': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&h=500&fit=crop&q=80',
    'Waterproof Smartband': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500&h=500&fit=crop&q=80',
    'Nail Polish Set': 'https://images.unsplash.com/photo-1610990837682-c590686d7015?w=500&h=500&fit=crop&q=80',
    'Makeup Palette': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=500&h=500&fit=crop&q=80',
    'Hair Care Set': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500&h=500&fit=crop&q=80',
    'Premium Lipstick': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=500&h=500&fit=crop&q=80',
    'Designer Perfume': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=500&h=500&fit=crop&q=80',
    'Luxury Face Cream': 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=500&h=500&fit=crop&q=80',
    'Travel Makeup Kit': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500&h=500&fit=crop&q=80',
    'Tejal Absolute Moisturizer': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=500&h=500&fit=crop&q=80',
    'Soundarya Radiance Cream': 'https://images.unsplash.com/photo-1567928269937-ae146e45b428?w=500&h=500&fit=crop&q=80',
    'Tea Tree Clarifying Shampoo': 'https://images.unsplash.com/photo-1608248597379-e075e7144e51?w=500&h=500&fit=crop&q=80',
    'Matte Foundation': 'https://images.unsplash.com/photo-1625093742435-6fa192b6fb10?w=500&h=500&fit=crop&q=80',
    'Sunscreen Lotion SPF 50': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=500&h=500&fit=crop&q=80',
    'Floor Lamp': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop&q=80',
    'Decorative Vase': 'https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?w=500&h=500&fit=crop&q=80',
    'Kitchen Storage Set': 'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=500&h=500&fit=crop&q=80',
    'Comfortable Cushions': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop&q=80',
    'Modern Table Lamp': 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=500&h=500&fit=crop&q=80',
    'Decorative Wall Art': 'https://images.unsplash.com/photo-1533158307587-50cd1c35e15?w=500&h=500&fit=crop&q=80',
    'Collapsible Laundry Hamper': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500&h=500&fit=crop&q=80',
    'Luxury Bed Sheet Set': 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=500&h=500&fit=crop&q=80',
    'Waterproof Laundry Bag': 'https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?w=500&h=500&fit=crop&q=80',
    'Canvas Laundry Bag': 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=500&h=500&fit=crop&q=80',
    'Heavy Duty Hooks': 'https://images.unsplash.com/photo-1585412727339-54e4ba3bbf9a?w=500&h=500&fit=crop&q=80',
    'Adhesive Hooks Set': 'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=500&h=500&fit=crop&q=80',
    'Pajama Set': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500&h=500&fit=crop&q=80',
    'Kids Watch': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=500&h=500&fit=crop&q=80',
    'School Bag': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&h=500&fit=crop&q=80',
    'Winter Jacket': 'https://images.unsplash.com/photo-1544923246-77307dd654cb?w=500&h=500&fit=crop&q=80',
    'Kids Shoes': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop&q=80',
    'Toy Set': 'https://images.unsplash.com/photo-1515488344751-661a8d1e8de1?w=500&h=500&fit=crop&q=80',
    'School Uniform': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&h=500&fit=crop&q=80',
    'Kids T-Shirt': 'https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?w=500&h=500&fit=crop&q=80',
    'YK Girls Skirt': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92c1?w=500&h=500&fit=crop&q=80',
    'YK Boys Track Pants': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&h=500&fit=crop&q=80',
    'YK Girls Top': 'https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=500&h=500&fit=crop&q=80',
    'YK Boys Casual Shirt': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&h=500&fit=crop&q=80',
    'Wrist Watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&q=80',
    'Casual Sneakers': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop&q=80',
    'Sports Shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop&q=80',
    'Formal Blazer': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop&q=80',
    'Polo T-Shirt': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&h=500&fit=crop&q=80',
    'Classic Oxford Shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop&q=80',
    'Dress Shirt': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&h=500&fit=crop&q=80',
    'Formal Suit': 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop&q=80',
    'Italian Leather Loafers': 'https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=500&h=500&fit=crop&q=80',
    'Designer Oversized Sunglasses': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop&q=80',
    'Minimalist Gold Pendant': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&h=500&fit=crop&q=80',
    'Velvet Evening Gown': 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=500&h=500&fit=crop&q=80',
    'Wireless Headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop&q=80',
    'Leather Biker Jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop&q=80',
    'Handbag Collection': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&h=500&fit=crop&q=80',
    'Silk Soap Delicate Face Wash': 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=500&h=500&fit=crop&q=80',
    'Saffron Dew Moisturizer': 'https://images.unsplash.com/photo-1617897903246-719242758050?w=500&h=500&fit=crop&q=80',
    'Eladi Keram Skin Care Oil': 'https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=500&h=500&fit=crop&q=80',
    'Bringadi Intensive Hair Treatment': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500&h=500&fit=crop&q=80',
    'Kumkumadi Miraculous Beauty Fluid': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&h=500&fit=crop&q=80',
    'Inforcer Anti-Hair Fall Shampoo': 'https://images.unsplash.com/photo-1585232351009-aa87416fca90?w=500&h=500&fit=crop&q=80',
    'Serie Expert Prokeratin Refill': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=500&h=500&fit=crop&q=80',
    'Vitamino Color Shampoo': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500&h=500&fit=crop&q=80',
    'Absolut Repair Mask': 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=500&h=500&fit=crop&q=80',
    'Fashion Sunglasses': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&h=500&fit=crop&q=80',
    'Stylish Heels': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&h=500&fit=crop&q=80',
    'Designer Handbag': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&h=500&fit=crop&q=80',
    'Sport Sandals': 'https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=500&h=500&fit=crop&q=80',
    'Walking Sneakers': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&h=500&fit=crop&q=80',
    'Platform Sandals': 'https://images.unsplash.com/photo-1562273138-f46be4ebdf33?w=500&h=500&fit=crop&q=80'
}

# 12 Products configuration for each Category
CATEGORY_EXACT_12 = {
    'Accessories': [
        'Premium Wallet', 'Designer Sunglasses', 'Leather Belt', 'Smart Watch Pro',
        'Sports Watch Digital', 'Classic Leather Belt', 'Leather Key Organizer',
        'Travel Duffle Bag', 'Minimalist Cardholder', 'Aviator Sunglasses',
        'Canvas Messenger Bag', 'Waterproof Smartband'
    ],
    'Beauty': [
        'Nail Polish Set', 'Makeup Palette', 'Hair Care Set', 'Premium Lipstick',
        'Designer Perfume', 'Luxury Face Cream', 'Travel Makeup Kit', 'Tejal Absolute Moisturizer',
        'Soundarya Radiance Cream', 'Tea Tree Clarifying Shampoo', 'Matte Foundation', 'Sunscreen Lotion SPF 50'
    ],
    'Home': [
        'Floor Lamp', 'Decorative Vase', 'Kitchen Storage Set', 'Comfortable Cushions',
        'Modern Table Lamp', 'Decorative Wall Art', 'Collapsible Laundry Hamper', 'Luxury Bed Sheet Set',
        'Waterproof Laundry Bag', 'Canvas Laundry Bag', 'Heavy Duty Hooks', 'Adhesive Hooks Set'
    ],
    'Kids': [
        'Pajama Set', 'Kids Watch', 'School Bag', 'Winter Jacket',
        'Kids Shoes', 'Toy Set', 'School Uniform', 'Kids T-Shirt',
        'YK Girls Skirt', 'YK Boys Track Pants', 'YK Girls Top', 'YK Boys Casual Shirt'
    ],
    'Men': [
        'Wrist Watch', 'Casual Sneakers', 'Leather Wallet', 'Sports Shoes',
        'Formal Blazer', 'Polo T-Shirt', 'Slim Fit Jeans', 'Classic Oxford Shirt',
        'Silk Tie', 'Business Trousers', 'Dress Shirt', 'Formal Suit'
    ],
    'New Arrivals': [
        'Italian Leather Loafers', 'Designer Oversized Sunglasses', 'Premium Chronograph Watch',
        'Urban Streetwear Hoodie', 'Minimalist Gold Pendant', 'Velvet Evening Gown',
        'Wireless Headphones', 'Leather Biker Jacket', 'Handbag Collection',
        'Casual Sneakers', 'Smart Watch Pro', 'Summer Collection Dress'
    ],
    'TOP BRANDS': [
        'Tejal Absolute Moisturizer', 'Soundarya Radiance Cream', 'Silk Soap Delicate Face Wash',
        'Tea Tree Clarifying Shampoo', 'Saffron Dew Moisturizer', 'Eladi Keram Skin Care Oil',
        'Bringadi Intensive Hair Treatment', 'Kumkumadi Miraculous Beauty Fluid',
        'Inforcer Anti-Hair Fall Shampoo', 'Serie Expert Prokeratin Refill',
        'Vitamino Color Shampoo', 'Absolut Repair Mask'
    ],
    'Women': [
        'Fashion Sunglasses', 'Evening Clutch', 'Yoga Pants', 'Casual T-Shirt',
        'Fashion Scarf', 'Stylish Heels', 'Designer Handbag', 'Floral Summer Dress',
        'Sport Sandals', 'Walking Sneakers', 'Platform Sandals', 'Flats'
    ]
}

# 16 Medal Brands config (Exactly 2 active products each)
MEDAL_BRANDS_CONFIG = {
    'levis': [('Slim Fit Jeans', 'Men'), ('Minimalist Cardholder', 'Accessories')],
    'puma': [('Urban Streetwear Hoodie', 'New Arrivals'), ('Travel Duffle Bag', 'Accessories')],
    'hm': [('Casual T-Shirt', 'Women'), ('Canvas Laundry Bag', 'Home')],
    'zara': [('Leather Biker Jacket', 'New Arrivals'), ('Formal Blazer', 'Men')],
    'nike': [('Sports Shoes', 'Men'), ('Yoga Pants', 'Women')],
    'tanishq': [('Minimalist Gold Pendant', 'New Arrivals'), ('Designer Perfume', 'Beauty')],
    'biba': [('Floral Summer Dress', 'Women'), ('Fashion Scarf', 'Women')],
    'jack-jones': [('Leather Belt', 'Accessories'), ('Leather Key Organizer', 'Accessories')],
    'uspa': [('Polo T-Shirt', 'Men'), ('Classic Oxford Shirt', 'Men')],
    'tommy': [('Leather Wallet', 'Men'), ('Polo T-Shirt', 'Men')],
    'only': [('Floral Summer Dress', 'Women'), ('Summer Collection Dress', 'New Arrivals')],
    'allen-solly': [('Classic Oxford Shirt', 'Men'), ('Business Trousers', 'Men')],
    'vero-moda': [('Velvet Evening Gown', 'New Arrivals'), ('Fashion Scarf', 'Women')],
    'steve-madden': [('Italian Leather Loafers', 'New Arrivals'), ('Flats', 'Women')],
    'skechers': [('Sport Sandals', 'Women'), ('Walking Sneakers', 'Women')],
    'van-heusen': [('Silk Tie', 'Men'), ('Business Trousers', 'Men')]
}

def execute_master_fix():
    print("=" * 60)
    print("MASTER FIX: EXACTLY 12 PRODUCTS PER CATEGORY & EXACTLY 2 PER BRAND")
    print("=" * 60)

    # Deactivate all products first
    Product.objects.all().update(is_active=False)

    # Step 1: Enforce EXACTLY 12 products per Category
    for cname, target_pnames in CATEGORY_EXACT_12.items():
        cat = Category.objects.get(name=cname)
        print(f"\nProcessing Category: {cat.name}")

        active_in_cat = []
        for pname in target_pnames:
            prod = Product.objects.filter(category=cat, name__iexact=pname).first()
            if not prod:
                prod = Product.objects.filter(name__iexact=pname).first()
            if not prod:
                default_brand = Brand.objects.first()
                unique_sku = f"SKU-{cat.slug[:3].upper()}-{uuid.uuid4().hex[:6].upper()}"
                unique_slug = f"{cat.slug}-{pname.lower().replace(' ', '-')}-{uuid.uuid4().hex[:4]}"
                prod = Product.objects.create(
                    name=pname,
                    slug=unique_slug,
                    description=f"Premium {pname} in {cat.name}",
                    short_description=f"High quality {pname}",
                    category=cat,
                    brand=default_brand,
                    price=49.99,
                    is_active=True,
                    sku=unique_sku
                )
            else:
                prod.category = cat
                prod.is_active = True
                prod.save()

            # Set image URL
            img_url = USER_URLS.get(pname, GENERAL_IMAGE_MAP.get(pname, "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=500&h=500&fit=crop&q=80"))
            ProductImage.objects.filter(product=prod).delete()
            ProductImage.objects.create(
                product=prod,
                image=img_url,
                alt_text=prod.name,
                is_primary=True
            )
            active_in_cat.append(prod)

        active_count = Product.objects.filter(category=cat, is_active=True).count()
        print(f"  Category '{cat.name}' now has EXACTLY {active_count} active products.")

    # Step 2: Ensure 16 Medal Brands have EXACTLY 2 active products
    for bslug, brand_target in MEDAL_BRANDS_CONFIG.items():
        try:
            brand = Brand.objects.get(slug=bslug)
        except Brand.DoesNotExist:
            brand = Brand.objects.create(name=bslug.replace('-', ' ').title(), slug=bslug)

        # Assign brand to these 2 specific products
        brand_prods = []
        for pname, cat_name in brand_target:
            prod = Product.objects.filter(name__iexact=pname, is_active=True).first()
            if prod:
                prod.brand = brand
                prod.save()
                brand_prods.append(prod)

        # Deactivate all other products for this brand
        b_active = Product.objects.filter(brand=brand, is_active=True)
        if b_active.count() > 2:
            keep_ids = set(p.id for p in brand_prods[:2])
            for p in b_active:
                if p.id not in keep_ids:
                    p.is_active = False
                    p.save()

    # Step 3: Re-apply user custom URLs for absolute 100% accuracy
    for pname, target_url in USER_URLS.items():
        prods = Product.objects.filter(name__iexact=pname, is_active=True)
        for p in prods:
            ProductImage.objects.filter(product=p).delete()
            ProductImage.objects.create(
                product=p,
                image=target_url,
                alt_text=p.name,
                is_primary=True
            )

    # Verification
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION: ALL 8 CATEGORIES")
    print("=" * 60)
    for cat in Category.objects.all():
        active_count = Product.objects.filter(category=cat, is_active=True).count()
        print(f"Category '{cat.name:<20}' -> EXACTLY {active_count} active products")

    print("\n" + "=" * 60)
    print("FINAL VERIFICATION: ALL 16 MEDAL BRANDS")
    print("=" * 60)
    for bslug in MEDAL_BRANDS_CONFIG.keys():
        try:
            brand = Brand.objects.get(slug=bslug)
            active_count = Product.objects.filter(brand=brand, is_active=True).count()
            print(f"Brand '{brand.name:<25}' ({bslug}) -> EXACTLY {active_count} active products")
        except Brand.DoesNotExist:
            pass

    # Verify Banners
    banners = Banner.objects.all()
    print("\n" + "=" * 60)
    print(f"VERIFIED BANNERS COUNT: {banners.count()} (100% UNTOUCHED)")
    for b in banners:
        print(f"  Banner ID {b.id}: '{b.title}' -> {b.image}")
    print("=" * 60)

if __name__ == '__main__':
    execute_master_fix()
