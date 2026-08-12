#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.api
import cloudinary.uploader
import re

# Configure Cloudinary with provided credentials
cloudinary.config(
    cloud_name='dqthyfxm9',
    api_key='882642629924913',
    api_secret='UZ6jb0sKLxHt1XldpIFtT5cPZvg'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def search_cloudinary_images(product_name):
    """Search Cloudinary for relevant images based on product name"""
    
    # Clean and prepare search terms
    name_lower = product_name.lower()
    
    # Extract keywords from product name
    keywords = []
    
    # Common product keywords and their search terms
    keyword_mapping = {
        'shirt': ['shirt', 'tshirt', 't-shirt', 'top'],
        't-shirt': ['shirt', 'tshirt', 't-shirt', 'top'],
        'jeans': ['jeans', 'denim', 'pants'],
        'pants': ['pants', 'trousers', 'bottoms'],
        'dress': ['dress', 'gown', 'outfit'],
        'watch': ['watch', 'timepiece', 'wrist'],
        'wallet': ['wallet', 'purse', 'leather'],
        'shoes': ['shoes', 'footwear', 'sneakers', 'boots'],
        'sneakers': ['sneakers', 'shoes', 'footwear'],
        'bag': ['bag', 'handbag', 'purse', 'tote'],
        'handbag': ['handbag', 'bag', 'purse', 'tote'],
        'clutch': ['clutch', 'bag', 'purse'],
        'sunglasses': ['sunglasses', 'shades', 'eyewear'],
        'belt': ['belt', 'leather', 'accessory'],
        'jacket': ['jacket', 'coat', 'outerwear'],
        'toy': ['toy', 'game', 'play'],
        'school': ['school', 'education', 'backpack'],
        'pajama': ['pajama', 'sleepwear', 'night'],
        'uniform': ['uniform', 'school', 'clothes'],
        'lamp': ['lamp', 'light', 'decoration'],
        'vase': ['vase', 'decoration', 'home'],
        'kitchen': ['kitchen', 'cook', 'home'],
        'storage': ['storage', 'organizer', 'home'],
        'cushion': ['cushion', 'pillow', 'home'],
        'cream': ['cream', 'beauty', 'skincare'],
        'moisturizer': ['moisturizer', 'cream', 'skincare'],
        'lipstick': ['lipstick', 'lip', 'makeup'],
        'nail': ['nail', 'polish', 'manicure'],
        'shampoo': ['shampoo', 'hair', 'care'],
        'perfume': ['perfume', 'fragrance', 'scent'],
        'soap': ['soap', 'wash', 'clean'],
    }
    
    # Find matching keywords
    for keyword, search_terms in keyword_mapping.items():
        if keyword in name_lower:
            keywords.extend(search_terms)
    
    # If no specific keywords found, use generic terms
    if not keywords:
        keywords = ['product', 'item', 'fashion']
    
    print(f"Searching for: {product_name}")
    print(f"Keywords: {keywords}")
    
    # Search Cloudinary for each keyword
    for keyword in keywords[:3]:  # Try first 3 keywords
        try:
            # Search for images with this keyword
            result = cloudinary.api.resources(
                type='upload',
                prefix=keyword,
                max_results=10,
                resource_type='image'
            )
            
            if result.get('resources'):
                # Return the first relevant image found
                image = result['resources'][0]
                public_id = image['public_id']
                secure_url = image['secure_url']
                print(f"  Found: {public_id}")
                return public_id, secure_url
                
        except Exception as e:
            print(f"  Error searching for '{keyword}': {str(e)}")
            continue
    
    # If no images found, return None
    print(f"  No images found for {product_name}")
    return None, None

def update_product_images():
    """Update all product images with relevant Cloudinary images"""
    
    print("=== Searching and Updating Product Images ===")
    products = Product.objects.all()
    updated_count = 0
    not_found_count = 0
    
    for i, product in enumerate(products):
        print(f"\n[{i+1}/{products.count()}] Processing: {product.name}")
        
        # Search for relevant image
        public_id, secure_url = search_cloudinary_images(product.name)
        
        if public_id:
            try:
                # Remove existing images for this product
                ProductImage.objects.filter(product=product).delete()
                
                # Create new product image record
                product_image = ProductImage.objects.create(
                    product=product,
                    image=public_id,
                    is_primary=True
                )
                
                print(f"  SUCCESS: Updated with {public_id}")
                updated_count += 1
                
            except Exception as e:
                print(f"  ERROR: Failed to update product: {str(e)}")
                not_found_count += 1
        else:
            print(f"  NOT FOUND: No suitable image found")
            not_found_count += 1
    
    print(f"\n=== Update Summary ===")
    print(f"Successfully updated: {updated_count} products")
    print(f"No images found: {not_found_count} products")
    print(f"Total processed: {products.count()} products")

if __name__ == "__main__":
    update_product_images()
