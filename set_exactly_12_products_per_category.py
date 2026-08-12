import os
import sys
import django
import hashlib

sys.path.insert(0, r"c:\Users\kadirivennela\OneDrive\Miniproject")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Category, SubCategory, Brand, Product, ProductImage, Banner

# High-resolution Unsplash photo mapping dictionary
IMAGE_MAP = {
    # Accessories
    'Premium Wallet': 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=500&h=500&fit=crop&q=80',
    'Designer Sunglasses': 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=500&h=500&fit=crop&q=80',
    'Leather Belt': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop&q=80',
    'Smart Watch Pro': 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&h=500&fit=crop&q=80',
    'Sports Watch Digital': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=500&h=500&fit=crop&q=80',
    'Classic Leather Belt': 'https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=500&h=500&fit=crop&q=80',
    'Leather Key Organizer': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&h=500&fit=crop&q=80',
    'Travel Duffle Bag': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop&q=80',
    'Minimalist Cardholder': 'https://images.unsplash.com/photo-1606503830023-e29f032225ca?w=500&h=500&fit=crop&q=80',
    'Aviator Sunglasses': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop&q=80',
    'Canvas Messenger Bag': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&h=500&fit=crop&q=80',
    'Waterproof Smartband': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500&h=500&fit=crop&q=80',

    # Beauty
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
    'Sunscreen Lotion SPF 50': 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=500&h=500&fit=crop&q=80',

    # Home
    'Floor Lamp': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&h=500&fit=crop&q=80',
    'Decorative Vase': 'https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?w=500&h=500&fit=crop&q=80',
    'Kitchen Storage Set': 'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=500&h=500&fit=crop&q=80',
    'Comfortable Cushions': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop&q=80',
    'Modern Table Lamp': 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=500&h=500&fit=crop&q=80',
    'Decorative Wall Art': 'https://images.unsplash.com/photo-1533158307587-50cd1c35e15?w=500&h=500&fit=crop&q=80',
    'Collapsible Laundry Hamper': 'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=500&h=500&fit=crop&q=80',
    'Luxury Bed Sheet Set': 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=500&h=500&fit=crop&q=80',
    'Ceramic Dinnerware Set': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&h=500&fit=crop&q=80',
    'Plush Bath Towel Set': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=500&h=500&fit=crop&q=80',
    'Scented Candle Pack': 'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=500&h=500&fit=crop&q=80',
    'Wall Clock Modern': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=500&h=500&fit=crop&q=80',

    # Kids
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
    'YK Casual Shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop&q=80',
    'Hot Wheels Car Set': 'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=500&h=500&fit=crop&q=80',

    # Men
    'Wrist Watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&q=80',
    'Casual Sneakers': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop&q=80',
    'Leather Wallet': 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=500&h=500&fit=crop&q=80',
    'Sports Shoes': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop&q=80',
    'Formal Blazer': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop&q=80',
    'Polo T-Shirt': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&h=500&fit=crop&q=80',
    'Slim Fit Jeans': 'https://images.unsplash.com/photo-1542272617-08f086302d36?w=500&h=500&fit=crop&q=80',
    'Classic Oxford Shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop&q=80',
    'Silk Tie': 'https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=500&h=500&fit=crop&q=80',
    'Business Trousers': 'https://images.unsplash.com/photo-1506629082925-2368c7f76df1?w=500&h=500&fit=crop&q=80',
    'Athletic Performance T-Shirt': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=500&h=500&fit=crop&q=80',
    'Traditional Sherwani': 'https://images.unsplash.com/photo-1617137968427-85924c800a22?w=500&h=500&fit=crop&q=80',

    # Women
    'Fashion Sunglasses': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&h=500&fit=crop&q=80',
    'Evening Clutch': 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500&h=500&fit=crop&q=80',
    'Yoga Pants': 'https://images.unsplash.com/photo-1506629082925-2368c7f76df1?w=500&h=500&fit=crop&q=80',
    'Casual T-Shirt': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&h=500&fit=crop&q=80',
    'Fashion Scarf': 'https://images.unsplash.com/photo-1583744983541-9a548a6af254?w=500&h=500&fit=crop&q=80',
    'Stylish Heels': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&h=500&fit=crop&q=80',
    'Designer Handbag': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&h=500&fit=crop&q=80',
    'Floral Summer Dress': 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=500&h=500&fit=crop&q=80',
    'Sport Sandals': 'https://images.unsplash.com/photo-1603808033192-082d6919d3e1?w=500&h=500&fit=crop&q=80',
    'Platform Sandals': 'https://images.unsplash.com/photo-1562273138-f46be4ebdf33?w=500&h=500&fit=crop&q=80',
    'Pencil Skirt': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92c1?w=500&h=500&fit=crop&q=80',
    'Embroidered Kurti': 'https://images.unsplash.com/photo-1617137968427-85924c800a22?w=500&h=500&fit=crop&q=80',

    # TOP BRANDS
    'Silk Soap Delicate Face Wash': 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=500&h=500&fit=crop&q=80',
    'Saffron Dew Moisturizer': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=500&h=500&fit=crop&q=80',
    'Eladi Keram Skin Care Oil': 'https://images.unsplash.com/photo-1567928269937-ae146e45b428?w=500&h=500&fit=crop&q=80',
    'Bringadi Intensive Hair Treatment': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500&h=500&fit=crop&q=80',
    'Kumkumadi Beauty Fluid': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=500&h=500&fit=crop&q=80',
    'Inforcer Anti-Hair Fall Shampoo': 'https://images.unsplash.com/photo-1608248597379-e075e7144e51?w=500&h=500&fit=crop&q=80',
    'Serie Expert Prokeratin Refill': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=500&h=500&fit=crop&q=80',
    'Revitalizing Night Cream': 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=500&h=500&fit=crop&q=80',
    'Organic Face Cleansing Gel': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=500&h=500&fit=crop&q=80',

    # New Arrivals
    'Handbag Collection': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500&h=500&fit=crop&q=80',
    'Summer Collection Dress': 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=500&h=500&fit=crop&q=80',
    'Leather Biker Jacket': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop&q=80',
    'Wireless Headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop&q=80',
    'Velvet Evening Gown': 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=500&h=500&fit=crop&q=80',
    'Minimalist Gold Pendant': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500&h=500&fit=crop&q=80',
    'Urban Streetwear Hoodie': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&h=500&fit=crop&q=80',
    'Premium Chronograph Watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&q=80',
    'Designer Oversized Sunglasses': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&h=500&fit=crop&q=80',
    'Italian Leather Loafers': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop&q=80',
}

NEW_PRODUCTS_BY_CATEGORY = {
    'Accessories': [
        ('Leather Key Organizer', 'jack-jones', 'Men', 29.99, None, 'leather-key-organizer'),
        ('Travel Duffle Bag', 'puma', 'unisex', 79.99, 64.99, 'travel-duffle-bag'),
        ('Minimalist Cardholder', 'levis', 'unisex', 24.99, None, 'minimalist-cardholder'),
        ('Aviator Sunglasses', 'ray-ban', 'unisex', 129.99, 99.99, 'aviator-sunglasses'),
    ],
    'New Arrivals': [
        ('Leather Biker Jacket', 'zara', 'unisex', 149.99, 119.99, 'leather-biker-jacket'),
        ('Wireless Headphones', 'sony', 'unisex', 199.99, 159.99, 'wireless-headphones'),
        ('Velvet Evening Gown', 'vero-moda', 'women', 129.99, None, 'velvet-evening-gown'),
        ('Minimalist Gold Pendant', 'tanishq', 'women', 249.99, 219.99, 'minimalist-gold-pendant'),
        ('Urban Streetwear Hoodie', 'puma', 'men', 69.99, 54.99, 'urban-streetwear-hoodie'),
        ('Premium Chronograph Watch', 'casio', 'men', 189.99, None, 'premium-chronograph-watch'),
        ('Designer Oversized Sunglasses', 'ray-ban', 'women', 139.99, 109.99, 'designer-oversized-sunglasses'),
        ('Italian Leather Loafers', 'steve-madden', 'men', 119.99, 94.99, 'italian-leather-loafers'),
    ]
}

def set_exactly_12_products():
    print("=" * 60)
    print("ENFORCING EXACTLY 12 PRODUCTS PER CATEGORY")
    print("=" * 60)

    categories = Category.objects.all()

    for cat in categories:
        print(f"\nProcessing Category: {cat.name} ({cat.slug})")

        # Step 1: Check if new products need to be created to reach 12
        existing_products = list(Product.objects.filter(category=cat))
        
        if len(existing_products) < 12:
            needed = 12 - len(existing_products)
            print(f"  Category has {len(existing_products)} products. Adding {needed} new products...")
            
            new_defs = NEW_PRODUCTS_BY_CATEGORY.get(cat.name, [])
            default_brand = Brand.objects.first()

            for i in range(needed):
                if i < len(new_defs):
                    pname, bslug, gender, price, dprice, pslug = new_defs[i]
                    try:
                        brand = Brand.objects.get(slug=bslug)
                    except Brand.DoesNotExist:
                        brand = default_brand
                else:
                    pname = f"{cat.name} Featured Product {i+1}"
                    brand = default_brand
                    gender = 'unisex'
                    price = 49.99
                    dprice = 39.99
                    pslug = f"{cat.slug}-featured-{i+1}"

                new_prod, created = Product.objects.get_or_create(
                    slug=pslug,
                    defaults={
                        'name': pname,
                        'description': f"High quality {pname} from {cat.name} collection.",
                        'short_description': f"Premium {pname}",
                        'category': cat,
                        'brand': brand,
                        'gender': gender,
                        'price': price,
                        'discount_price': dprice,
                        'is_active': True,
                        'stock_quantity': 50,
                        'sku': f"SKU-{cat.slug[:3].upper()}-{i+100}"
                    }
                )
                if not created:
                    new_prod.is_active = True
                    new_prod.category = cat
                    new_prod.save()
            
            # Refresh list
            existing_products = list(Product.objects.filter(category=cat))

        # Step 2: Pick 12 representative products for this category
        # Ensure we pick distinct names/subcategories if available
        seen_names = set()
        selected_products = []
        
        for p in existing_products:
            if p.name not in seen_names:
                seen_names.add(p.name)
                selected_products.append(p)
            if len(selected_products) == 12:
                break
                
        # If distinct names were fewer than 12, fill remaining
        if len(selected_products) < 12:
            for p in existing_products:
                if p not in selected_products:
                    selected_products.append(p)
                if len(selected_products) == 12:
                    break

        selected_ids = set(p.id for p in selected_products)

        # Step 3: Activate selected 12 products, deactivate/delete all other products in this category
        cat_products = Product.objects.filter(category=cat)
        for p in cat_products:
            if p.id in selected_ids:
                p.is_active = True
                p.save()
            else:
                # Deactivate surplus products so they don't show up in customer view
                p.is_active = False
                p.save()

        # Step 4: Ensure every kept product has an accurate, high-quality image URL
        for p in selected_products:
            # Check custom IMAGE_MAP or construct clean fallback
            if p.name in IMAGE_MAP:
                img_url = IMAGE_MAP[p.name]
            else:
                # Hash for consistent beautiful photo
                h = int(hashlib.md5(f"{p.id}_{p.name}".encode('utf-8')).hexdigest(), 16)
                img_url = f"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&q=80&v={h%10000}"
            
            ProductImage.objects.filter(product=p).delete()
            ProductImage.objects.create(
                product=p,
                image=img_url,
                alt_text=p.name,
                is_primary=True
            )

        active_count = Product.objects.filter(category=cat, is_active=True).count()
        print(f"  Result: Category '{cat.name}' now has EXACTLY {active_count} active products.")

    print("\n" + "=" * 60)
    print("SUMMARY OF ALL CATEGORIES AFTER UPDATE:")
    print("=" * 60)
    for cat in Category.objects.all():
        active_prods = Product.objects.filter(category=cat, is_active=True)
        print(f"Category: {cat.name} ({cat.slug}) -> Active Products: {active_prods.count()}")
        for p in active_prods:
            img = p.images.first()
            img_src = img.image if img else 'NO_IMAGE'
            print(f"   - [{p.id}] {p.name} (${p.get_final_price()}) | Image: {img_src}")

if __name__ == '__main__':
    set_exactly_12_products()
