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

def update_polo_tshirt():
    """Update only Polo T-Shirt product with Walmart image URL"""
    
    # The specific image URL provided by the user
    walmart_url = 'https://i5.walmartimages.com/asr/13f75afa-28aa-4b63-a977-ad7ea2e1b0ae.c8a0e77158317905a9214dfd984b5f87.jpeg'
    
    print("=== UPDATING POLO T-SHIRT PRODUCT ===")
    print("Only updating Polo T-Shirt with Walmart image URL")
    print("NOT touching any other products or home page")
    print("=" * 60)
    print()
    
    # Find Polo T-Shirt products
    polo_tshirts = Product.objects.filter(name__icontains='polo t-shirt')
    
    if not polo_tshirts.exists():
        print("No Polo T-Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in polo_tshirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                walmart_url,
                folder="products",
                public_id=f"product_{shirt.id}_polo_tshirt_walmart",
                overwrite=True
            )
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=shirt,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            total_updated += 1
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Polo T-Shirt products found: {polo_tshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {polo_tshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Polo T-Shirt products were updated")
    print("No other products or home page were touched")
    print(f"Used Walmart image URL: {walmart_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in polo_tshirts:
        images = ProductImage.objects.filter(product=shirt)
        if images.exists():
            image = images.first()
            if hasattr(image.image, 'url'):
                image_url = image.image.url
            else:
                image_url = f"https://res.cloudinary.com/dqthyfxm9/image/upload/{image.image}"
            print(f"  {shirt.name}: {image_url}")
    
    print("=" * 60)

if __name__ == "__main__":
    update_polo_tshirt()
