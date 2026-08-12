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

def update_winter_jacket():
    """Update all winter jacket products with the specific Walmart image"""
    
    # Use the specific Walmart image URL provided
    walmart_url = 'https://i5.walmartimages.com/seo/Ierhent-Kid-Big-Boys-Winter-Coats-Jackets-Kids-Lightweight-Padded-Hooded-Puffer-Autumn-and-Winter-Coat-Grey-13-14-Years_51d40446-2594-46b2-ae2f-20ec2d8d1fa1.0778d786bb6a2567a6e83fbe6c869910.jpeg'
    
    # Find all winter jacket products
    winter_jackets = Product.objects.filter(name__icontains='winter jacket')
    
    print(f'=== UPDATING {winter_jackets.count()} WINTER JACKET PRODUCTS ===')
    
    for jacket in winter_jackets:
        try:
            print(f'Updating: {jacket.name} (ID: {jacket.id}) - Brand: {jacket.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                walmart_url,
                folder='products',
                public_id=f'product_{jacket.id}_winter_jacket_walmart',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=jacket).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=jacket,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_winter_jacket()
