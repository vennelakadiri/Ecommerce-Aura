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

def update_leather_wallets():
    """Update all leather wallet products with the specific Etsy image"""
    
    # Use the specific Etsy image URL provided
    etsy_image_url = 'https://i.etsystatic.com/16971055/r/il/4e0cf5/3021061575/il_1588xN.3021061575_7om9.jpg'
    
    # Find all leather wallet products
    leather_wallets = Product.objects.filter(name__icontains='leather wallet')
    
    print(f'=== UPDATING {leather_wallets.count()} LEATHER WALLET PRODUCTS ===')
    
    for wallet in leather_wallets:
        try:
            print(f'Updating: {wallet.name} (ID: {wallet.id}) - Brand: {wallet.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                etsy_image_url,
                folder='products',
                public_id=f'product_{wallet.id}_leather_wallet_etsy',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=wallet).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=wallet,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_leather_wallets()
