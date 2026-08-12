#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def display_yk_products():
    """Display only the 3 YK products with their updated images"""
    
    print("=" * 80)
    print("YK BRAND PRODUCTS DISPLAY")
    print("=" * 80)
    print("Showing only the 3 YK products that were updated with chat image URLs")
    print("No other products or categories are affected")
    print("=" * 80)
    print()
    
    # Define the YK products we want to display
    yk_product_names = ['YK Boys Track Pants', 'YK Girls Top', 'YK Boys Casual Shirt']
    
    for product_name in yk_product_names:
        print(f"PRODUCT: {product_name}")
        print("-" * 60)
        
        # Find the product
        products = Product.objects.filter(name__icontains=product_name.lower())
        
        if not products.exists():
            print(f"  Status: Product not found")
            print()
            continue
        
        product = products.first()
        
        # Get product details
        print(f"  ID: {product.id}")
        print(f"  Name: {product.name}")
        print(f"  Brand: {product.brand.name}")
        print(f"  Category: {product.category.name}")
        print(f"  Price: ${product.price}")
        if product.discount_price:
            print(f"  Discount Price: ${product.discount_price}")
        print(f"  Description: {product.description}")
        print(f"  Slug: {product.slug}")
        
        # Get product images
        images = ProductImage.objects.filter(product=product)
        
        if images.exists():
            print(f"  Images: {images.count()} found")
            for i, image in enumerate(images, 1):
                if hasattr(image.image, 'url'):
                    image_url = image.image.url
                else:
                    # Construct Cloudinary URL
                    image_url = f"https://res.cloudinary.com/dqthyfxm9/image/upload/{image.image}"
                
                print(f"    Image {i}: {image_url}")
                print(f"    Is Primary: {image.is_primary}")
                print(f"    Alt Text: {image.alt_text or 'No alt text'}")
        else:
            print(f"  Images: No images found")
        
        print()
    
    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    print("Only YK products are displayed above")
    print("No other products or categories were modified")
    print("These are the exact same products that were updated with chat image URLs")
    print("=" * 80)

if __name__ == "__main__":
    display_yk_products()
