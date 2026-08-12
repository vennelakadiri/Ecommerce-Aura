#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary.config(
    cloud_name='dqthyfxm9',
    api_key='882642629924913',
    api_secret='UZ6jb0sKLxHt1XldpIFtT5cPZvg'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def update_premium_wallet():
    """Update only Premium Wallet product with the provided Leatherman image URL"""
    
    # The specific image URL provided by the user
    leatherman_url = 'https://leathermanpk.com/cdn/shop/files/IMG_8153.jpg?v=1698886761&width=4000'
    
    print("=== UPDATING PREMIUM WALLET PRODUCT ===")
    print("Only updating Premium Wallet with Leatherman image URL")
    print("NOT touching any other products, categories, or home page")
    print("=" * 60)
    print()
    
    # Find Premium Wallet product
    premium_wallets = Product.objects.filter(name__icontains='premium wallet')
    
    if not premium_wallets.exists():
        print("No Premium Wallet product found in the database")
        return
    
    total_updated = 0
    
    for wallet in premium_wallets:
        print(f"Processing: {wallet.name} (ID: {wallet.id})")
        print(f"  Category: {wallet.category.name}")
        print(f"  Brand: {wallet.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=wallet).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                leatherman_url,
                folder="products",
                public_id=f"product_{wallet.id}_premium_wallet_leatherman",
                overwrite=True
            )
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=wallet,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            total_updated += 1
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Premium Wallet products found: {premium_wallets.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {premium_wallets.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Premium Wallet products were updated")
    print("No other products, categories, or home page were touched")
    print(f"Used Leatherman image URL: {leatherman_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for wallet in premium_wallets:
        images = ProductImage.objects.filter(product=wallet)
        if images.exists():
            image = images.first()
            if hasattr(image.image, 'url'):
                image_url = image.image.url
            else:
                image_url = f"https://res.cloudinary.com/dqthyfxm9/image/upload/{image.image}"
            print(f"  {wallet.name}: {image_url}")
    
    print("=" * 60)

if __name__ == "__main__":
    update_premium_wallet()
