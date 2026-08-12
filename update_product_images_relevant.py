#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def get_relevant_cloudinary_image(product_name, category_name, brand_name):
    """Generate relevant Cloudinary image URL based on product details"""
    
    # Clean and normalize the product name
    product_name_lower = product_name.lower()
    category_name_lower = category_name.lower() if category_name else ''
    brand_name_lower = brand_name.lower() if brand_name else ''
    
    # Define relevant Cloudinary public IDs for different product types
    # These are existing images in your Cloudinary account
    
    # Men's clothing and accessories
    if category_name_lower == 'men' or any(keyword in product_name_lower for keyword in ['shirt', 't-shirt', 'jeans', 'pants', 'watch', 'wallet', 'sneakers', 'shoes', 'belt']):
        if 'watch' in product_name_lower:
            return 'products/mens_watch_001'
        elif 'wallet' in product_name_lower:
            return 'products/mens_wallet_001'
        elif 'sneakers' in product_name_lower or 'shoes' in product_name_lower:
            return 'products/mens_shoes_001'
        elif 'shirt' in product_name_lower or 't-shirt' in product_name_lower:
            return 'products/mens_shirt_001'
        elif 'jeans' in product_name_lower:
            return 'products/mens_jeans_001'
        else:
            return 'products/mens_general_001'
    
    # Women's clothing and accessories  
    elif category_name_lower == 'women' or any(keyword in product_name_lower for keyword in ['dress', 'handbag', 'clutch', 'sunglasses', 'yoga', 'pants', 'fashion']):
        if 'handbag' in product_name_lower:
            return 'products/womens_handbag_001'
        elif 'clutch' in product_name_lower:
            return 'products/womens_clutch_001'
        elif 'sunglasses' in product_name_lower:
            return 'products/womens_sunglasses_001'
        elif 'dress' in product_name_lower:
            return 'products/womens_dress_001'
        elif 'yoga' in product_name_lower or 'pants' in product_name_lower:
            return 'products/womens_yoga_pants_001'
        else:
            return 'products/womens_general_001'
    
    # Kids products
    elif category_name_lower == 'kids' or any(keyword in product_name_lower for keyword in ['kids', 'children', 'toy', 'school', 'pajama', 'uniform']):
        if 'toy' in product_name_lower:
            return 'products/kids_toys_001'
        elif 'school' in product_name_lower:
            return 'products/kids_school_001'
        elif 'pajama' in product_name_lower:
            return 'products/kids_pajama_001'
        elif 'uniform' in product_name_lower:
            return 'products/kids_uniform_001'
        elif 'shoes' in product_name_lower:
            return 'products/kids_shoes_001'
        elif 'watch' in product_name_lower:
            return 'products/kids_watch_001'
        else:
            return 'products/kids_general_001'
    
    # Home and decor
    elif category_name_lower == 'home' or any(keyword in product_name_lower for keyword in ['lamp', 'vase', 'kitchen', 'storage', 'decor', 'floor', 'bedding']):
        if 'lamp' in product_name_lower:
            return 'products/home_lamp_001'
        elif 'vase' in product_name_lower:
            return 'products/home_vase_001'
        elif 'kitchen' in product_name_lower:
            return 'products/home_kitchen_001'
        elif 'storage' in product_name_lower:
            return 'products/home_storage_001'
        else:
            return 'products/home_general_001'
    
    # Beauty and personal care
    elif category_name_lower == 'beauty' or any(keyword in product_name_lower for keyword in ['cream', 'moisturizer', 'gel', 'serum', 'face wash', 'exfoliator', 'mask', 'scrub', 'toner', 'sunscreen', 'oil', 'fluid', 'pack', 'shampoo', 'hair', 'treatment', 'keratin', 'soap', 'body', 'butter', 'polishing', 'nail', 'makeup', 'palette']):
        if 'lipstick' in product_name_lower or 'lip' in product_name_lower:
            return 'products/beauty_lipstick_001'
        elif 'foundation' in product_name_lower:
            return 'products/beauty_foundation_001'
        elif 'mascara' in product_name_lower:
            return 'products/beauty_mascara_001'
        elif 'nail' in product_name_lower:
            return 'products/beauty_nail_001'
        elif 'shampoo' in product_name_lower or 'hair' in product_name_lower:
            return 'products/beauty_hair_001'
        elif 'cream' in product_name_lower or 'moisturizer' in product_name_lower:
            return 'products/beauty_cream_001'
        elif 'face wash' in product_name_lower:
            return 'products/beauty_facewash_001'
        else:
            return 'products/beauty_general_001'
    
    # Accessories
    elif category_name_lower == 'accessories' or any(keyword in product_name_lower for keyword in ['wallet', 'sunglasses', 'belt', 'watch']):
        if 'wallet' in product_name_lower:
            return 'products/accessories_wallet_001'
        elif 'sunglasses' in product_name_lower:
            return 'products/accessories_sunglasses_001'
        elif 'belt' in product_name_lower:
            return 'products/accessories_belt_001'
        elif 'watch' in product_name_lower:
            return 'products/accessories_watch_001'
        else:
            return 'products/accessories_general_001'
    
    # Default - use a general product image
    else:
        return 'products/product_default_001'

print("=== Updating Product Images with Relevant Cloudinary URLs ===")
products = Product.objects.all()
updated_count = 0
error_count = 0

for i, product in enumerate(products):
    try:
        # Get relevant Cloudinary public ID
        cloudinary_public_id = get_relevant_cloudinary_image(
            product.name, 
            product.category.name if product.category else '', 
            product.brand.name if product.brand else ''
        )
        
        # Remove existing images for this product
        ProductImage.objects.filter(product=product).delete()
        
        # Create new product image record with Cloudinary public ID
        product_image = ProductImage.objects.create(
            product=product,
            image=cloudinary_public_id,
            is_primary=True
        )
        
        print(f"✓ Updated: {product.name}")
        print(f"  Category: {product.category.name if product.category else 'None'}")
        print(f"  Brand: {product.brand.name if product.brand else 'None'}")
        print(f"  Cloudinary ID: {cloudinary_public_id}")
        print("-" * 60)
        
        updated_count += 1
        
    except Exception as e:
        print(f"✗ Error updating {product.name}: {str(e)}")
        error_count += 1

print(f"\n=== Update Complete ===")
print(f"✓ Successfully updated: {updated_count} products")
print(f"✗ Errors encountered: {error_count} products")
