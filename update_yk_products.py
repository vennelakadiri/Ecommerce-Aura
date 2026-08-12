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

def update_yk_products():
    """Update YK brand products with their correct image URLs from chat data"""
    
    # Define the exact mappings for YK products from chat data
    yk_product_mappings = {
        'YK Boys Track Pants': 'https://assets.myntassets.com/h_200,w_200,c_fill,g_auto/h_1440,q_100,w_1080/v1/assets/images/3466718/2018/8/7/9d28382c-0387-4414-8033-5d4170c0cff61533618321205-YK-Boys-Track-Pants-5941533618321070-1.jpg',
        'YK Girls Top': 'https://assets.myntassets.com/h_200,w_200,c_fill,g_auto/h_1440,q_100,w_1080/v1/assets/images/productimage/2021/4/8/a3a16a7d-8321-4b65-9e00-5e1d52877c531617876534623-1.jpg',
        'YK Boys Casual Shirt': 'https://assets.myntassets.com/h_200,w_200,c_fill,g_auto/h_1440,q_100,w_1080/v1/assets/images/15263490/2022/7/21/37fc3f13-80fa-490a-9d25-9d7395642ee61658401567104YKBoysBlueSolidCasualShirt1.jpg',
    }
    
    print("=== UPDATING YK BRAND PRODUCTS WITH CHAT IMAGES ===")
    print("Only updating: YK Boys Track Pants, YK Girls Top, YK Boys Casual Shirt")
    print()
    
    total_updated = 0
    total_found = 0
    
    for product_name, image_url in yk_product_mappings.items():
        print(f"=== UPDATING {product_name.upper()} ===")
        
        # Find all matching products
        matching_products = Product.objects.filter(name__icontains=product_name.lower())
        
        if not matching_products.exists():
            print(f"  No {product_name} products found")
            print()
            continue
        
        total_found += matching_products.count()
        
        for product in matching_products:
            print(f"Processing: {product.name} (ID: {product.id}) - Category: {product.category.name}")
            
            try:
                # Remove existing images
                ProductImage.objects.filter(product=product).delete()
                print(f"  Removed existing images")
                
                # Upload new image to Cloudinary
                result = cloudinary.uploader.upload(
                    image_url,
                    folder="products",
                    public_id=f"product_{product.id}_{product.name.replace(' ', '_').replace('-', '_').lower()}",
                    overwrite=True
                )
                
                # Create new product image
                product_image = ProductImage.objects.create(
                    product=product,
                    image=result['public_id'],
                    is_primary=True
                )
                
                print(f"  SUCCESS: {result['secure_url']}")
                total_updated += 1
                
            except Exception as e:
                print(f"  ERROR: {str(e)}")
            
            print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Products with matching images: {total_found}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {total_found - total_updated}")
    
    print("\n=== PRODUCTS UPDATED ===")
    for key, url in yk_product_mappings.items():
        products = Product.objects.filter(name__icontains=key.lower())
        if products.exists():
            product = products.first()
            images = ProductImage.objects.filter(product=product)
            if images.exists():
                print(f"  {key}: {images.first().image.url if hasattr(images.first().image, 'url') else str(images.first().image)}")
    
    print("\n=== IMAGE URLS FOUND ===")
    for key, url in yk_product_mappings.items():
        print(f"  {key}:")
        print(f"    {url}")
    print()

if __name__ == "__main__":
    update_yk_products()
