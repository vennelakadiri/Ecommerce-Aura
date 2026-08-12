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

def update_athletic_performance_tshirt():
    """Update only Athletic Performance T-Shirt product with Walmart APEXFWDT image URL"""
    
    # The specific image URL provided by the user
    apexfwdt_url = 'https://i5.walmartimages.com/seo/APEXFWDT-Summer-Clearance-Gym-Ready-Quick-Dry-T-Shirts-Men-s-Muscle-Fit-Workout-Shirts-Long-Sleeve-UPF-40-Performance-Top-Summer-Saving-M-Army-Green_0ddd98c0-aa06-410e-aaaf-7a26fbdcdd14.ed351abbf65f496dc363ae10f90da419.jpeg'
    
    print("=== UPDATING ATHLETIC PERFORMANCE T-SHIRT PRODUCT ===")
    print("Only updating Athletic Performance T-Shirt with Walmart APEXFWDT image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Athletic Performance T-Shirt products
    athletic_tshirts = Product.objects.filter(name__icontains='athletic performance t-shirt')
    
    if not athletic_tshirts.exists():
        print("No Athletic Performance T-Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in athletic_tshirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                apexfwdt_url,
                folder="products",
                public_id=f"product_{shirt.id}_athletic_performance_tshirt_apexfwdt",
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
    print(f"Athletic Performance T-Shirt products found: {athletic_tshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {athletic_tshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Athletic Performance T-Shirt products were updated")
    print("No other products were touched")
    print(f"Used Walmart APEXFWDT image URL: {apexfwdt_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in athletic_tshirts:
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
    update_athletic_performance_tshirt()
