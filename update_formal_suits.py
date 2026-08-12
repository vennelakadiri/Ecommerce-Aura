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

def update_formal_suits():
    """Update all formal suit products with the specific Reviewtique image"""
    
    # Use the specific Reviewtique image URL provided
    reviewtique_url = 'https://www.reviewtique.com/wp-content/uploads/2024/12/formal-suits-men.webp'
    
    # Find all formal suit products
    formal_suits = Product.objects.filter(name__icontains='formal suit')
    
    print(f'=== UPDATING {formal_suits.count()} FORMAL SUIT PRODUCTS ===')
    
    for suit in formal_suits:
        try:
            print(f'Updating: {suit.name} (ID: {suit.id}) - Brand: {suit.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                reviewtique_url,
                folder='products',
                public_id=f'product_{suit.id}_formal_suit_reviewtique',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=suit).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=suit,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_formal_suits()
