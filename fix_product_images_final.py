#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader

# Configure Cloudinary with provided credentials
cloudinary.config(
    cloud_name='dqthyfxm9',
    api_key='882642629924913',
    api_secret='UZ6jb0sKLxHt1XldpIFtT5cPZvg'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def get_working_image_url(product_name, category_name):
    """Return working image URLs based on product type"""
    
    name_lower = product_name.lower()
    category_lower = category_name.lower() if category_name else ''
    
    # Use working external URLs that actually exist
    if category_lower == 'men' or any(keyword in name_lower for keyword in ['shirt', 't-shirt', 'jeans', 'pants', 'watch', 'wallet', 'sneakers', 'shoes', 'belt']):
        if 'watch' in name_lower:
            return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
        elif 'wallet' in name_lower:
            return 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=400&h=300&fit=crop'
        elif 'shoes' in name_lower or 'sneakers' in name_lower:
            return 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop'
        elif 'shirt' in name_lower or 't-shirt' in name_lower:
            return 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop'
        elif 'jeans' in name_lower:
            return 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=300&fit=crop'
    
    elif category_lower == 'women' or any(keyword in name_lower for keyword in ['dress', 'handbag', 'clutch', 'sunglasses', 'yoga', 'pants', 'fashion']):
        if 'handbag' in name_lower:
            return 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'
        elif 'clutch' in name_lower:
            return 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=300&fit=crop'
        elif 'sunglasses' in name_lower:
            return 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400&h=300&fit=crop'
        elif 'dress' in name_lower:
            return 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=300&fit=crop'
    
    elif category_lower == 'kids' or any(keyword in name_lower for keyword in ['kids', 'children', 'toy', 'school', 'pajama', 'uniform']):
        if 'toy' in name_lower:
            return 'https://images.unsplash.com/photo-1515488344751-661a8d1e8de1?w=400&h=300&fit=crop'
        elif 'school' in name_lower:
            return 'https://images.unsplash.com/photo-1588072428504-1a848e2e1af3?w=400&h=300&fit=crop'
        elif 'pajama' in name_lower:
            return 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=300&fit=crop'
        elif 'shoes' in name_lower:
            return 'https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1514091189623-a2a7585aae13?w=400&h=300&fit=crop'
    
    elif category_lower == 'home' or any(keyword in name_lower for keyword in ['lamp', 'vase', 'kitchen', 'storage', 'decor', 'floor', 'bedding']):
        if 'lamp' in name_lower:
            return 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop'
        elif 'vase' in name_lower:
            return 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop'
        elif 'kitchen' in name_lower:
            return 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop'
    
    elif category_lower == 'beauty' or any(keyword in name_lower for keyword in ['cream', 'moisturizer', 'gel', 'serum', 'face wash', 'exfoliator', 'mask', 'scrub', 'toner', 'sunscreen', 'oil', 'fluid', 'pack', 'shampoo', 'hair', 'treatment', 'keratin', 'soap', 'body', 'butter', 'polishing', 'nail', 'makeup', 'palette']):
        if 'lipstick' in name_lower or 'lip' in name_lower:
            return 'https://images.unsplash.com/photo-1596462502278-27d4415415f2?w=400&h=300&fit=crop'
        elif 'nail' in name_lower:
            return 'https://images.unsplash.com/photo-1610990837682-c590686d7015?w=400&h=300&fit=crop'
        elif 'shampoo' in name_lower or 'hair' in name_lower:
            return 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop'
        elif 'cream' in name_lower or 'moisturizer' in name_lower:
            return 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop'
    
    elif category_lower == 'accessories' or any(keyword in name_lower for keyword in ['wallet', 'sunglasses', 'belt', 'watch']):
        if 'wallet' in name_lower:
            return 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=400&h=300&fit=crop'
        elif 'sunglasses' in name_lower:
            return 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400&h=300&fit=crop'
        elif 'belt' in name_lower:
            return 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=300&fit=crop'
        elif 'watch' in name_lower:
            return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1524863479829-916d8e77f114?w=400&h=300&fit=crop'
    
    else:
        return 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop'

def update_all_products():
    """Update all products with working image URLs"""
    
    print("=== Updating All Products with Working Images ===")
    products = Product.objects.all()
    updated_count = 0
    
    for i, product in enumerate(products):
        print(f"[{i+1}/{products.count()}] {product.name}")
        
        try:
            # Get working image URL
            image_url = get_working_image_url(product.name, product.category.name if product.category else '')
            
            # Remove existing images
            ProductImage.objects.filter(product=product).delete()
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                image_url,
                folder="products",
                public_id=f"product_{product.id}_{product.slug.replace('-', '_')}",
                overwrite=True
            )
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=product,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            updated_count += 1
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        if i % 10 == 0:  # Progress update every 10 products
            print(f"Progress: {i+1}/{products.count()} completed")
    
    print(f"\n=== Complete ===")
    print(f"Successfully updated: {updated_count}/{products.count()} products")

if __name__ == "__main__":
    update_all_products()
