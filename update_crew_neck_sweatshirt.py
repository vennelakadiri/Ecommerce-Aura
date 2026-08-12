#!/usr/bin/env python
import os
import django
import requests
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def download_image_from_url(url, filename):
    """Download image from URL and save to media folder"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Save to media folder
        media_products_dir = os.path.join('media', 'products')
        if not os.path.exists(media_products_dir):
            os.makedirs(media_products_dir, exist_ok=True)
        
        file_path = os.path.join(media_products_dir, filename)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")
        return False

print("=== Updating Crew Neck Sweatshirt Product Image ===")

# Find the Crew Neck Sweatshirt product
try:
    product = Product.objects.get(name__icontains='Crew Neck Sweatshirt')
    
    if product:
        print(f"Found product: {product.name}")
        print(f"Current slug: {product.slug}")
        print(f"Product ID: {product.id}")
        
        # Download the new image
        image_url = "https://i5.walmartimages.com/seo/Hanes-Men-s-and-Big-Men-s-Ultimate-Cotton-Heavyweight-Sweatshirt-Sizes-S-3XL_0a2cf96c-5600-408a-917f-5951ced0ae31.79b434f20b47ea95c35e79ca5baeb18c.jpeg"
        filename = f"crew_neck_sweatshirt_walmart_{product.id}.jpeg"
        
        if download_image_from_url(image_url, filename):
            # Remove existing images
            ProductImage.objects.filter(product=product).delete()
            
            # Create new product image record
            with open(f"media/products/{filename}", 'rb') as f:
                product_image = ProductImage.objects.create(
                    product=product,
                    image=File(f, name=filename)
                )
            
            print(f"✅ Updated product image: {filename}")
            print(f"Product: {product.name}")
            print(f"New image URL: /media/products/{filename}")
        else:
            print(f"❌ Failed to download image from URL")
    else:
        print("❌ Crew Neck Sweatshirt product not found")

print("=== Update Complete ===")
