import os
import sys
import django

sys.path.insert(0, r"c:\Users\kadirivennela\OneDrive\Miniproject")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage, Banner

# Full dictionary of user-specified URLs
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

def apply_user_urls():
    print("=" * 60)
    print("APPLYING ALL USER SPECIFIED IMAGE URLS TO ALL MATCHING PRODUCTS")
    print("=" * 60)
    
    total_updated = 0
    for name, target_url in USER_URLS.items():
        # Match both active and inactive products matching the name exactly or partially
        products = Product.objects.filter(name__iexact=name)
        if not products.exists():
            products = Product.objects.filter(name__icontains=name)
            
        print(f"\nProcessing '{name}' ({products.count()} matching products found):")
        for p in products:
            # Delete existing images and create new ProductImage with exact user URL
            ProductImage.objects.filter(product=p).delete()
            ProductImage.objects.create(
                product=p,
                image=target_url,
                alt_text=p.name,
                is_primary=True
            )
            total_updated += 1
            print(f"  -> Updated ID {p.id:4d} | Active: {str(p.is_active):<5} | Category: {p.category.name:<15} | Name: '{p.name}'")
            print(f"     URL: {target_url}")

    print("=" * 60)
    print(f"SUCCESSFULLY UPDATED {total_updated} PRODUCT RECORDS WITH SPECIFIED CUSTOM URLS.")
    
    # Verify Banners
    banners = Banner.objects.all()
    print(f"Verified Banners Count: {banners.count()} (UNTOUCHED)")
    for b in banners:
        print(f"  Banner {b.id}: {b.title} -> {b.image}")
    print("=" * 60)

if __name__ == '__main__':
    apply_user_urls()
