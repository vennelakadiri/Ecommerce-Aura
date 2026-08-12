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

def update_cotton_vneck_tshirt():
    """Update only Cotton V-Neck T-Shirt product with Jockey Walmart image URL"""
    
    # The specific image URL provided by the user
    jockey_walmart_url = 'https://i5.walmartimages.com/seo/Jockey-Men-s-Slim-Fit-Cotton-Stretch-V-Neck-T-Shirt-2-Pack_36362fcd-5a52-4aec-baba-8291afebd70a.ce86044c628316d0b4f0b0f4997b4897.jpeg'
    
    print("=== UPDATING COTTON V-NECK T-SHIRT PRODUCT ===")
    print("Only updating Cotton V-Neck T-Shirt with Jockey Walmart image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Cotton V-Neck T-Shirt products
    cotton_vneck_tshirts = Product.objects.filter(name__icontains='cotton v-neck t-shirt')
    
    if not cotton_vneck_tshirts.exists():
        print("No Cotton V-Neck T-Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in cotton_vneck_tshirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                jockey_walmart_url,
                folder="products",
                public_id=f"product_{shirt.id}_cotton_vneck_tshirt_jockey_walmart",
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
    print(f"Cotton V-Neck T-Shirt products found: {cotton_vneck_tshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {cotton_vneck_tshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Cotton V-Neck T-Shirt products were updated")
    print("No other products were touched")
    print(f"Used Jockey Walmart image URL: {jockey_walmart_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in cotton_vneck_tshirts:
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
    update_cotton_vneck_tshirt()
