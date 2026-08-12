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

def update_cotton_tshirt():
    """Update only Cotton T-Shirt product with Hanes Walmart image URL"""
    
    # The specific image URL provided by the user
    hanes_walmart_url = 'https://i5.walmartimages.com/seo/Hanes-Originals-Men-s-Cotton-T-Shirt-Red-River-Clay-L_8b777cc9-c614-491b-b1e3-ad8f1a0846b0.4901b9914f0e9b290175b6b2a481e6c5.jpeg'
    
    print("=== UPDATING COTTON T-SHIRT PRODUCT ===")
    print("Only updating Cotton T-Shirt with Hanes Walmart image URL")
    print("NOT touching any other products or home page")
    print("=" * 60)
    print()
    
    # Find Cotton T-Shirt products
    cotton_tshirts = Product.objects.filter(name__icontains='cotton t-shirt')
    
    if not cotton_tshirts.exists():
        print("No Cotton T-Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in cotton_tshirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                hanes_walmart_url,
                folder="products",
                public_id=f"product_{shirt.id}_cotton_tshirt_hanes_walmart",
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
    print(f"Cotton T-Shirt products found: {cotton_tshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {cotton_tshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Cotton T-Shirt products were updated")
    print("No other products or home page were touched")
    print(f"Used Hanes Walmart image URL: {hanes_walmart_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in cotton_tshirts:
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
    update_cotton_tshirt()
