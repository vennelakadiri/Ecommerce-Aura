#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

# Map product categories to appropriate image ranges
def get_image_for_product(product, product_index):
    """Assign appropriate image based on product category and type"""
    category_name = product.category.name.lower() if product.category else ''
    product_name = product.name.lower()
    brand_name = product.brand.name.lower() if product.brand else ''
    
    # Men's clothing and accessories
    if category_name == 'men' or any(keyword in product_name for keyword in ['shirt', 't-shirt', 'jeans', 'pants', 'watch', 'wallet', 'sneakers', 'shoes', 'belt']):
        return f'temp_image_{100 + (product_index % 50)}.jpg'
    
    # Women's clothing and accessories  
    elif category_name == 'women' or any(keyword in product_name for keyword in ['dress', 'handbag', 'clutch', 'sunglasses', 'yoga', 'pants', 'fashion']):
        return f'temp_image_{150 + (product_index % 50)}.jpg'
    
    # Kids products
    elif category_name == 'kids' or any(keyword in product_name for keyword in ['kids', 'children', 'toy', 'school', 'pajama', 'uniform']):
        return f'temp_image_{200 + (product_index % 50)}.jpg'
    
    # Home and decor
    elif category_name == 'home' or any(keyword in product_name for keyword in ['lamp', 'vase', 'kitchen', 'storage', 'decor', 'floor', 'bedding']):
        return f'temp_image_{250 + (product_index % 50)}.jpg'
    
    # Beauty and personal care
    elif category_name == 'beauty' or any(keyword in product_name for keyword in ['cream', 'moisturizer', 'gel', 'serum', 'face wash', 'exfoliator', 'mask', 'scrub', 'toner', 'sunscreen', 'oil', 'fluid', 'pack', 'shampoo', 'hair', 'treatment', 'keratin', 'soap', 'body', 'butter', 'polishing', 'nail', 'makeup', 'palette']):
        return f'temp_image_{300 + (product_index % 50)}.jpg'
    
    # Accessories
    elif category_name == 'accessories' or any(keyword in product_name for keyword in ['wallet', 'sunglasses', 'belt', 'watch']):
        return f'temp_image_{350 + (product_index % 50)}.jpg'
    
    # Default - use remaining images
    else:
        return f'temp_image_{400 + (product_index % 50)}.jpg'

print("=== Fixing Product Images ===")
products = Product.objects.all()

for i, product in enumerate(products):
    # Get appropriate image filename
    image_filename = get_image_for_product(product, i)
    source_path = os.path.join(os.getcwd(), image_filename)
    
    if os.path.exists(source_path):
        # Remove existing images for this product
        ProductImage.objects.filter(product=product).delete()
        
        # Upload to Cloudinary
        try:
            result = cloudinary.uploader.upload(
                source_path,
                folder="products",
                public_id=f"{product.slug}_{image_filename.replace('.jpg', '')}",
                overwrite=True
            )
            
            # Create new product image record with Cloudinary URL
            product_image = ProductImage.objects.create(
                product=product,
                image=result['public_id']
            )
            
            print(f"Product: {product.name}")
            print(f"  Assigned: {image_filename}")
            print(f"  Category: {product.category.name if product.category else 'None'}")
            print(f"  Cloudinary URL: {result['secure_url']}")
            print("-" * 50)
        except Exception as e:
            print(f"Error uploading {product.name}: {str(e)}")
    else:
        print(f"Image not found: {image_filename}")

print("=== Product Images Fixed ===")
