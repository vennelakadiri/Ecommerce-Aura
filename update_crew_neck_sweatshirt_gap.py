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

def update_crew_neck_sweatshirt():
    """Update only Crew Neck Sweatshirt product with Gap image URL"""
    
    # The specific image URL provided by the user
    gap_url = 'https://www1.assets-gap.com/webcontent/0016/506/161/cn16506161.jpg'
    
    print("=== UPDATING CREW NECK SWEATSHIRT PRODUCT ===")
    print("Only updating Crew Neck Sweatshirt with Gap image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Crew Neck Sweatshirt products
    crew_neck_sweatshirts = Product.objects.filter(name__icontains='crew neck sweatshirt')
    
    if not crew_neck_sweatshirts.exists():
        print("No Crew Neck Sweatshirt product found in the database")
        return
    
    total_updated = 0
    
    for sweatshirt in crew_neck_sweatshirts:
        print(f"Processing: {sweatshirt.name} (ID: {sweatshirt.id})")
        print(f"  Category: {sweatshirt.category.name}")
        print(f"  Brand: {sweatshirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=sweatshirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                gap_url,
                folder="products",
                public_id=f"product_{sweatshirt.id}_crew_neck_sweatshirt_gap",
                overwrite=True
            )
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=sweatshirt,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            total_updated += 1
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Crew Neck Sweatshirt products found: {crew_neck_sweatshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {crew_neck_sweatshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Crew Neck Sweatshirt products were updated")
    print("No other products were touched")
    print(f"Used Gap image URL: {gap_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for sweatshirt in crew_neck_sweatshirts:
        images = ProductImage.objects.filter(product=sweatshirt)
        if images.exists():
            image = images.first()
            if hasattr(image.image, 'url'):
                image_url = image.image.url
            else:
                image_url = f"https://res.cloudinary.com/dqthyfxm9/image/upload/{image.image}"
            print(f"  {sweatshirt.name}: {image_url}")
    
    print("=" * 60)

if __name__ == "__main__":
    update_crew_neck_sweatshirt()
