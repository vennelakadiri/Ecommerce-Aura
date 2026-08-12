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

def get_precise_image_url(product_name, category_name, brand_name):
    """Get highly specific image URLs based on exact product name, category, and brand"""
    
    name_lower = product_name.lower()
    category_lower = category_name.lower() if category_name else ''
    brand_lower = brand_name.lower() if brand_name else ''
    
    # MEN CATEGORY - Specific product matching
    if category_lower == 'men':
        if 'watch' in name_lower:
            if 'casio' in brand_lower:
                return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
            elif 'fastrack' in brand_lower:
                return 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1498687720653-55b7e9b01557?w=400&h=300&fit=crop'
        
        elif 'wallet' in name_lower:
            if 'puma' in brand_lower:
                return 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=300&fit=crop'
        
        elif 'sneakers' in name_lower or 'shoes' in name_lower:
            if 'adidas' in brand_lower:
                return 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop'
            elif 'nike' in brand_lower:
                return 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=300&fit=crop'
        
        elif 'shirt' in name_lower or 't-shirt' in name_lower:
            if 'polo' in name_lower:
                return 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop'
        
        elif 'jeans' in name_lower:
            return 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
        
        elif 'belt' in name_lower:
            return 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=300&fit=crop'
        
        else:
            return 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=300&fit=crop'
    
    # WOMEN CATEGORY - Specific product matching
    elif category_lower == 'women':
        if 'sunglasses' in name_lower:
            if 'ray-ban' in brand_lower:
                return 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1516102691325-485c9690ae8c?w=400&h=300&fit=crop'
        
        elif 'clutch' in name_lower or 'handbag' in name_lower:
            if 'coach' in brand_lower:
                return 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'
            elif 'mango' in brand_lower:
                return 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1584917875444-8329d4ff7c9e?w=400&h=300&fit=crop'
        
        elif 'pants' in name_lower or 'yoga' in name_lower:
            if 'nike' in brand_lower:
                return 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=300&fit=crop'
        
        elif 'dress' in name_lower:
            return 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=400&h=300&fit=crop'
        
        elif 'heels' in name_lower or 'shoes' in name_lower:
            return 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop'
        
        elif 'scarf' in name_lower:
            return 'https://images.unsplash.com/photo-1583744983541-9a548a6af254?w=400&h=300&fit=crop'
        
        else:
            return 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=300&fit=crop'
    
    # KIDS CATEGORY - Specific product matching
    elif category_lower == 'kids':
        if 'pajama' in name_lower:
            return 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=400&h=300&fit=crop'
        
        elif 'watch' in name_lower:
            return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
        
        elif 'school' in name_lower or 'uniform' in name_lower:
            return 'https://images.unsplash.com/photo-1588072428504-1a848e2e1af3?w=400&h=300&fit=crop'
        
        elif 'bag' in name_lower:
            return 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'
        
        elif 'toy' in name_lower:
            return 'https://images.unsplash.com/photo-1515488344751-661a8d1e8de1?w=400&h=300&fit=crop'
        
        elif 'shoes' in name_lower:
            return 'https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&h=300&fit=crop'
        
        elif 't-shirt' in name_lower:
            return 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=300&fit=crop'
        
        elif 'jacket' in name_lower:
            return 'https://images.unsplash.com/photo-1544978148-4bd0d0d9dbbb?w=400&h=300&fit=crop'
        
        else:
            return 'https://images.unsplash.com/photo-1514091189623-a2a7585aae13?w=400&h=300&fit=crop'
    
    # ACCESSORIES CATEGORY - Specific product matching
    elif category_lower == 'accessories':
        if 'wallet' in name_lower:
            if 'puma' in brand_lower:
                return 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=300&fit=crop'
        
        elif 'sunglasses' in name_lower:
            if 'fastrack' in brand_lower:
                return 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1516102691325-485c9690ae8c?w=400&h=300&fit=crop'
        
        elif 'belt' in name_lower:
            return 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=300&fit=crop'
        
        elif 'watch' in name_lower:
            return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
        
        else:
            return 'https://images.unsplash.com/photo-1524863479829-916d8e77f114?w=400&h=300&fit=crop'
    
    # HOME CATEGORY - Specific product matching
    elif category_lower == 'home':
        if 'lamp' in name_lower:
            if 'philips' in brand_lower:
                return 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1534040380116-1a14e1532dc8?w=400&h=300&fit=crop'
        
        elif 'vase' in name_lower:
            return 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop'
        
        elif 'kitchen' in name_lower or 'storage' in name_lower:
            if 'ikea' in brand_lower:
                return 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1587413853953-4292b30fd722?w=400&h=300&fit=crop'
        
        elif 'cushion' in name_lower or 'pillow' in name_lower:
            return 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop'
        
        elif 'wall' in name_lower or 'art' in name_lower:
            return 'https://images.unsplash.com/photo-1533158307587-50cd1c35e15?w=400&h=300&fit=crop'
        
        else:
            return 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop'
    
    # BEAUTY CATEGORY - Specific product matching
    elif category_lower == 'beauty':
        if 'lipstick' in name_lower or 'lip' in name_lower:
            if 'lakme' in brand_lower:
                return 'https://images.unsplash.com/photo-1596462502278-27d4415415f2?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1584304290319-9fd6be0c5df2?w=400&h=300&fit=crop'
        
        elif 'nail' in name_lower:
            return 'https://images.unsplash.com/photo-1610990837682-c590686d7015?w=400&h=300&fit=crop'
        
        elif 'makeup' in name_lower or 'palette' in name_lower:
            if 'maybelline' in brand_lower:
                return 'https://images.unsplash.com/photo-1596462502278-27d4415415f2?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop'
        
        elif 'shampoo' in name_lower or 'hair' in name_lower:
            if 'lakme' in brand_lower:
                return 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop'
            else:
                return 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=400&h=300&fit=crop'
        
        elif 'cream' in name_lower or 'moisturizer' in name_lower:
            return 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=400&h=300&fit=crop'
        
        elif 'soap' in name_lower or 'wash' in name_lower:
            return 'https://images.unsplash.com/photo-1584304290319-9fd6be0c5df2?w=400&h=300&fit=crop'
        
        elif 'perfume' in name_lower:
            return 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop'
        
        else:
            return 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=300&fit=crop'
    
    # NEW ARRIVALS CATEGORY
    elif category_lower == 'new-arrivals':
        if 'handbag' in name_lower:
            return 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'
        elif 'sneakers' in name_lower:
            return 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=300&fit=crop'
        elif 'watch' in name_lower:
            return 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop'
    
    # TOP BRANDS CATEGORY
    elif category_lower == 'top-brands':
        if 'moisturizer' in name_lower or 'cream' in name_lower:
            return 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=400&h=300&fit=crop'
        elif 'soap' in name_lower or 'wash' in name_lower:
            return 'https://images.unsplash.com/photo-1584304290319-9fd6be0c5df2?w=400&h=300&fit=crop'
        else:
            return 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop'
    
    # Default fallback
    else:
        return 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop'

def update_all_products_precise():
    """Update all products with highly specific relevant images"""
    
    print("=== PRECISE PRODUCT IMAGE ASSIGNMENT ===")
    products = Product.objects.all()
    updated_count = 0
    error_count = 0
    
    for i, product in enumerate(products):
        print(f"[{i+1}/{products.count()}] {product.name}")
        print(f"  Category: {product.category.name}")
        print(f"  Brand: {product.brand.name}")
        
        try:
            # Get precise image URL
            image_url = get_precise_image_url(
                product.name, 
                product.category.name, 
                product.brand.name
            )
            
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
            error_count += 1
        
        if i % 25 == 0:  # Progress update every 25 products
            print(f"Progress: {i+1}/{products.count()} completed")
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Successfully updated: {updated_count}/{products.count()} products")
    print(f"Errors encountered: {error_count} products")

if __name__ == "__main__":
    update_all_products_precise()
