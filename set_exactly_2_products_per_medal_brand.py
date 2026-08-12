import os
import sys
import django
import uuid

sys.path.insert(0, r"c:\Users\kadirivennela\OneDrive\Miniproject")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand, Product, ProductImage, Category

MEDAL_BRANDS = [
    'levis', 'puma', 'hm', 'zara', 'nike', 'tanishq', 'biba',
    'jack-jones', 'uspa', 'tommy', 'only', 'allen-solly',
    'vero-moda', 'steve-madden', 'skechers', 'van-heusen'
]

BRAND_PRODUCTS_CONFIG = {
    'levis': [
        ('Slim Fit Jeans', 'https://i5.walmartimages.com/seo/Men-s-Lee-Extreme-Motion-MVP-Straight-Leg-Slim-Fit-Jeans-Color-Baritt-Size-42X30_a959aeb5-94df-4a85-a8b4-c5b401822559.98969c530cf8465ddffcfc12a7bd17e1.jpeg', 'Men'),
        ('Minimalist Cardholder', 'https://i.etsystatic.com/49382644/r/il/b900df/5652218918/il_1588xN.5652218918_ba0l.jpg', 'Accessories')
    ],
    'puma': [
        ('Urban Streetwear Hoodie', 'https://i.pinimg.com/736x/ac/ee/a2/aceea245fd311fe129e3e58ed1107a06.jpg', 'New Arrivals'),
        ('Travel Duffle Bag', 'https://images.unsplash.com/photo-1547949003-9792a18a2601?w=500&h=500&fit=crop&q=80', 'Accessories')
    ],
    'hm': [
        ('Casual T-Shirt', 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&h=500&fit=crop&q=80', 'Women'),
        ('Canvas Laundry Bag', 'https://images.unsplash.com/photo-1544816155-12df9643f363?w=500&h=500&fit=crop&q=80', 'Home')
    ],
    'zara': [
        ('Leather Biker Jacket', 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop&q=80', 'New Arrivals'),
        ('Zara Tailored Blazer', 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=500&h=500&fit=crop&q=80', 'Women')
    ],
    'nike': [
        ('Sports Shoes', 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop&q=80', 'Men'),
        ('Yoga Pants', 'https://i5.walmartimages.com/seo/BKQCNKM-Yoga-Pants-Pockets-Women-Flare-Womens-High-Waist-Pant-Soft-Sport-Leggings-Workout-Running-Trousers-Gray-XXL_403959ad-1c23-4876-a93c-b9d457341801.42cd74abefa52f8034b9de3d06eb13c0.jpeg', 'Women')
    ],
    'tanishq': [
        ('Minimalist Gold Pendant', 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&h=500&fit=crop&q=80', 'New Arrivals'),
        ('Gold Diamond Necklace', 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500&h=500&fit=crop&q=80', 'Women')
    ],
    'biba': [
        ('Embroidered Kurti', 'https://images.unsplash.com/photo-1617137968427-85924c800a22?w=500&h=500&fit=crop&q=80', 'Women'),
        ('Designer Salwar Suit', 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?w=500&h=500&fit=crop&q=80', 'Women')
    ],
    'jack-jones': [
        ('Leather Belt', 'https://i5.walmartimages.com/seo/Men-s-Casual-Genuine-Leather-Jeans-Belts-1-1-2-Wide-Work-Dress-Belt-for-Men_5f86c437-61dd-48e1-bd18-504102b775eb.80c45d4a39038e3e7df4f5f0595eb730.jpeg', 'Accessories'),
        ('Leather Key Organizer', 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&h=500&fit=crop&q=80', 'Accessories')
    ],
    'uspa': [
        ('Polo T-Shirt', 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&h=500&fit=crop&q=80', 'Men'),
        ('USPA Casual Shirt', 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop&q=80', 'Men')
    ],
    'tommy': [
        ('Tommy Leather Wallet', 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=500&h=500&fit=crop&q=80', 'Men'),
        ('Tommy Casual Polo', 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&h=500&fit=crop&q=80', 'Men')
    ],
    'only': [
        ('Floral Summer Dress', 'https://www.graceandlace.com/cdn/shop/files/FloralSummerMaxiDress-1.jpg?v=1715707860', 'Women'),
        ('Summer Collection Dress', 'https://images.esellerpro.com/2355/I/213/505/JM%20D668.jpg', 'New Arrivals')
    ],
    'allen-solly': [
        ('Classic Oxford Shirt', 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop&q=80', 'Men'),
        ('Formal Trousers', 'https://images.unsplash.com/photo-1506629082925-2368c7f76df1?w=500&h=500&fit=crop&q=80', 'Men')
    ],
    'vero-moda': [
        ('Velvet Evening Gown', 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=500&h=500&fit=crop&q=80', 'New Arrivals'),
        ('Fashion Scarf', 'https://i5.walmartimages.com/seo/Baqcunre-Clearance-Silk-Scarf-Scarfs-for-Women-Lightweight-Print-Floral-Pattern-Scarf-Shawl-Fashion-Scarves-Shawls-And-Wraps-for-Spring_e474ed02-cb5a-41cf-8390-3fa4b575826e.9065a0c247b629465c12aa0f1e0336e1.jpeg?odnHeight=576&odnWidth=576&odnBg=FFFFFF', 'Women')
    ],
    'steve-madden': [
        ('Italian Leather Loafers', 'https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=500&h=500&fit=crop&q=80', 'New Arrivals'),
        ('Flats', 'https://i5.walmartimages.com/seo/Obtaom-Women-s-Round-Toe-Ballet-Flats-Cute-Textile-Ballerina-Flats-Comfortable-Faux-Leather-Insole-Low-Heels-Dress-Shoes-For-Ladies-Black-US9_a45effbe-dc04-428c-af72-ef845776aef2.8053db39c593949cd798e0dc0f50e99b.jpeg?odnHeight=424&odnWidth=424&odnBg=FFFFFF', 'Women')
    ],
    'skechers': [
        ('Sport Sandals', 'https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=500&h=500&fit=crop&q=80', 'Women'),
        ('Walking Sneakers', 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&h=500&fit=crop&q=80', 'Women')
    ],
    'van-heusen': [
        ('Silk Tie', 'https://media.neimanmarcus.com/f_auto,q_auto/01/nm_4489966_100551_m', 'Men'),
        ('Business Trousers', 'https://i5.walmartimages.com/seo/TFEOQRY-Business-Trousers-for-Men-Solid-Color-Button-Down-Full-Length-Pants-Medium-Waist-Trousers-Dark-Gray_3beb93d0-b64c-4125-b412-d7a0aec0e0d8.245f48fbead3aed1d54799909c28e039.jpeg', 'Men')
    ]
}

def set_exactly_2_products_per_brand():
    print("=" * 60)
    print("ENFORCING EXACTLY 2 PRODUCTS PER FEATURED BRAND UNDER 'MEDAL WORTHY BRANDS TO BAG'")
    print("=" * 60)

    for bslug in MEDAL_BRANDS:
        try:
            brand = Brand.objects.get(slug=bslug)
        except Brand.DoesNotExist:
            brand = Brand.objects.create(name=bslug.replace('-', ' ').title(), slug=bslug)

        print(f"\nBrand: '{brand.name}' (slug: {bslug})")
        target_items = BRAND_PRODUCTS_CONFIG.get(bslug, [])

        kept_products = []
        for pname, img_url, cat_name in target_items:
            # Try finding existing product for this brand first
            prod = Product.objects.filter(brand=brand, name__iexact=pname).first()
            if not prod:
                prod = Product.objects.filter(name__iexact=pname).first()
            
            if not prod:
                category = Category.objects.get(name=cat_name)
                unique_sku = f"SKU-{bslug.upper()}-{uuid.uuid4().hex[:6].upper()}"
                unique_slug = f"{bslug}-{pname.lower().replace(' ', '-')}-{uuid.uuid4().hex[:4]}"
                prod = Product.objects.create(
                    name=pname,
                    slug=unique_slug,
                    description=f"{pname} by {brand.name}",
                    short_description=f"Premium {pname}",
                    category=category,
                    brand=brand,
                    price=49.99,
                    is_active=True,
                    sku=unique_sku
                )
            else:
                prod.brand = brand
                prod.is_active = True
                prod.save()

            # Set exact relevant image URL
            ProductImage.objects.filter(product=prod).delete()
            ProductImage.objects.create(
                product=prod,
                image=img_url,
                alt_text=prod.name,
                is_primary=True
            )
            kept_products.append(prod)

        # Deactivate all other products for this brand so count is EXACTLY 2
        kept_ids = set(p.id for p in kept_products)
        other_brand_prods = Product.objects.filter(brand=brand)
        for p in other_brand_prods:
            if p.id not in kept_ids:
                p.is_active = False
                p.save()

        active_count = Product.objects.filter(brand=brand, is_active=True).count()
        print(f"  Result: Brand '{brand.name}' now has EXACTLY {active_count} active products.")

    print("\n" + "=" * 60)
    print("VERIFICATION FOR ALL 16 FEATURED BRANDS:")
    print("=" * 60)
    for bslug in MEDAL_BRANDS:
        try:
            brand = Brand.objects.get(slug=bslug)
            active_prods = Product.objects.filter(brand=brand, is_active=True)
            print(f"Brand '{brand.name}' ({bslug}) -> {active_prods.count()} active products:")
            for p in active_prods:
                img = p.images.first()
                url = img.image if img else 'NO_IMAGE'
                print(f"   - [ID {p.id:4d}] '{p.name}' -> {url}")
        except Brand.DoesNotExist:
            print(f"Brand slug '{bslug}' NOT FOUND")
    print("=" * 60)

if __name__ == '__main__':
    set_exactly_2_products_per_brand()
