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

def update_graphic_print_tshirt():
    """Update only Graphic Print T-Shirt product with Jiomart image URL"""
    
    # The specific image URL provided by the user
    jiomart_url = 'https://www.jiomart.com/images/product/500x630/441180508_olive/graphic-print-crew-neck-t-shirt-model-441180508_olive-0-202206091410.jpg'
    
    print("=== UPDATING GRAPHIC PRINT T-SHIRT PRODUCT ===")
    print("Only updating Graphic Print T-Shirt with Jiomart image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Graphic Print T-Shirt products
    graphic_print_tshirts = Product.objects.filter(name__icontains='graphic print t-shirt')
    
    if not graphic_print_tshirts.exists():
        print("No Graphic Print T-Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in graphic_print_tshirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                jiomart_url,
                folder="products",
                public_id=f"product_{shirt.id}_graphic_print_tshirt_jiomart",
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
    print(f"Graphic Print T-Shirt products found: {graphic_print_tshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {graphic_print_tshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Graphic Print T-Shirt products were updated")
    print("No other products were touched")
    print(f"Used Jiomart image URL: {jiomart_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in graphic_print_tshirts:
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
    update_graphic_print_tshirt()
