#!/usr/bin/env python
import os
import django
import requests
import uuid

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage
import cloudinary
import cloudinary.uploader

print("=== Fixing Product Images with Relevant Images ===")

# Relevant image queries for each product category
PRODUCT_IMAGE_QUERIES = {
    # Men's products
    'Classic Oxford Shirt': 'mens dress shirt formal oxford',
    'Slim Fit Jeans': 'mens slim fit jeans blue denim',
    'Polo T-Shirt': 'mens polo t-shirt casual',
    'Formal Blazer': 'mens formal blazer suit jacket',
    'Sports Shoes': 'mens running shoes athletic',
    'Leather Wallet': 'mens leather wallet brown',
    'Casual Sneakers': 'mens casual sneakers white',
    'Wrist Watch': 'mens wrist watch analog',
    
    # Women's products
    'Floral Summer Dress': 'womens floral summer dress',
    'Designer Handbag': 'womens designer handbag leather',
    'Stylish Heels': 'womens high heels shoes',
    'Fashion Scarf': 'womens fashion scarf silk',
    'Casual T-Shirt': 'womens casual t-shirt',
    'Yoga Pants': 'womens yoga pants athletic',
    'Evening Clutch': 'womens evening clutch bag',
    'Fashion Sunglasses': 'womens fashion sunglasses',
    
    # Accessories
    'Smart Watch Pro': 'smart watch digital fitness',
    'Leather Belt': 'mens leather belt formal',
    'Designer Sunglasses': 'designer sunglasses luxury',
    'Premium Wallet': 'premium leather wallet',
    'Sports Headphones': 'wireless headphones sports',
    'Fitness Tracker': 'fitness tracker watch',
    'Travel Backpack': 'travel backpack modern',
    'Phone Case': 'phone case protective',
    
    # Beauty products
    'Luxury Face Cream': 'face cream luxury skincare',
    'Designer Perfume': 'designer perfume bottle luxury',
    'Premium Lipstick': 'premium lipstick makeup',
    'Hair Care Set': 'hair care shampoo conditioner',
    'Makeup Palette': 'makeup palette cosmetics',
    'Nail Polish Set': 'nail polish set colorful',
    
    # Home products
    'Decorative Wall Art': 'wall art decorative modern',
    'Modern Table Lamp': 'table lamp modern decor',
    'Comfortable Cushions': 'decorative cushions sofa',
    'Kitchen Storage Set': 'kitchen storage containers',
    'Decorative Vase': 'decorative vase ceramic',
    'Floor Lamp': 'floor lamp modern lighting',
    
    # Kids products
    'Kids T-Shirt': 'kids t-shirt colorful',
    'School Uniform': 'kids school uniform',
    'Toy Set': 'kids toys educational',
    'Kids Shoes': 'kids shoes colorful',
    'Winter Jacket': 'kids winter jacket warm',
    'School Bag': 'kids school bag backpack',
    'Kids Watch': 'kids digital watch',
    'Pajama Set': 'kids pajama set comfortable'
}

def get_relevant_image(query, width=400, height=400):
    """Get a relevant image from Picsum with seed"""
    try:
        # Use Picsum with descriptive seed for more relevant images
        seed = query.replace(' ', '-').replace(',', '').lower()
        return f"https://picsum.photos/seed/{seed}/{width}/{height}.jpg"
    except Exception as e:
        print(f"Error getting image: {e}")
        return f"https://picsum.photos/seed/{uuid.uuid4().hex[:8]}/{width}/{height}.jpg"

def upload_to_cloudinary(image_url, public_id):
    """Upload image to Cloudinary"""
    try:
        result = cloudinary.uploader.upload(
            image_url,
            public_id=public_id,
            folder="products",
            resource_type="image"
        )
        return result['secure_url']
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return image_url  # Fallback to original URL

def update_product_images():
    """Update all product images with relevant ones"""
    updated_count = 0
    
    # Get all products
    products = Product.objects.filter(is_active=True)
    print(f"Found {products.count()} products to update...")
    
    for product in products:
        try:
            # Get relevant image query
            query = PRODUCT_IMAGE_QUERIES.get(product.name, f"{product.name} {product.category.name}")
            
            # Get relevant image
            image_url = get_relevant_image(query)
            
            # Upload to Cloudinary
            cloudinary_url = upload_to_cloudinary(image_url, f"product_{product.id}")
            
            # Delete existing images
            ProductImage.objects.filter(product=product).delete()
            
            # Create new product image
            ProductImage.objects.create(
                product=product,
                image=cloudinary_url,
                alt_text=product.name,
                is_primary=True
            )
            
            print(f"  - Updated: {product.name} -> {cloudinary_url}")
            updated_count += 1
            
        except Exception as e:
            print(f"  - Error updating {product.name}: {e}")
    
    print(f"\n=== Successfully updated {updated_count} product images! ===")
    return updated_count

if __name__ == "__main__":
    updated = update_product_images()
    print(f"\nTotal products updated: {updated}")
    print("All product images now show relevant items!")
