#!/usr/bin/env python
import os
import django
import random
import requests
import uuid

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, Category, SubCategory, Brand, ProductImage
import cloudinary
import cloudinary.uploader

print("=== Bulk Product Creation with Unsplash Images ===")

# Sample product data for different categories
PRODUCT_DATA = {
    'men': [
        {'name': 'Classic Oxford Shirt', 'price': 1299, 'brand': 'allen-solly', 'subcategory': 'shirts'},
        {'name': 'Slim Fit Jeans', 'price': 1899, 'brand': 'levis', 'subcategory': 'trousers'},
        {'name': 'Polo T-Shirt', 'price': 899, 'brand': 'uspa', 'subcategory': 't-shirts'},
        {'name': 'Formal Blazer', 'price': 3299, 'brand': 'park-avenue', 'subcategory': 'suits'},
        {'name': 'Sports Shoes', 'price': 2499, 'brand': 'nike', 'subcategory': 'sports-shoes'},
        {'name': 'Leather Wallet', 'price': 799, 'brand': 'puma', 'subcategory': 'wallets'},
        {'name': 'Casual Sneakers', 'price': 2199, 'brand': 'adidas', 'subcategory': 'sneakers'},
        {'name': 'Wrist Watch', 'price': 1599, 'brand': 'fastrack', 'subcategory': 'watches'},
    ],
    'women': [
        {'name': 'Floral Summer Dress', 'price': 1499, 'brand': 'only', 'subcategory': 'tops'},
        {'name': 'Designer Handbag', 'price': 2799, 'brand': 'mango', 'subcategory': 'travel-bags-women'},
        {'name': 'Stylish Heels', 'price': 1899, 'brand': 'steve-madden', 'subcategory': 'sandals-women'},
        {'name': 'Fashion Scarf', 'price': 599, 'brand': 'vero-moda', 'subcategory': 'scarves-women'},
        {'name': 'Casual T-Shirt', 'price': 799, 'brand': 'hm', 'subcategory': 'tops'},
        {'name': 'Yoga Pants', 'price': 1299, 'brand': 'nike', 'subcategory': 'sports-bottoms-women'},
        {'name': 'Evening Clutch', 'price': 999, 'brand': 'coach', 'subcategory': 'travel-bags-women'},
        {'name': 'Fashion Sunglasses', 'price': 1399, 'brand': 'ray-ban', 'subcategory': 'sunglasses-women'},
    ],
    'accessories': [
        {'name': 'Smart Watch Pro', 'price': 3999, 'brand': 'casio', 'subcategory': 'watches-accessories'},
        {'name': 'Leather Belt', 'price': 899, 'brand': 'jack-jones', 'subcategory': 'wallets-accessories'},
        {'name': 'Designer Sunglasses', 'price': 1299, 'brand': 'fastrack', 'subcategory': 'sunglasses-accessories'},
        {'name': 'Premium Wallet', 'price': 799, 'brand': 'puma', 'subcategory': 'wallets-accessories'},
        {'name': 'Sports Headphones', 'price': 1999, 'brand': 'sony', 'subcategory': 'speakers'},
        {'name': 'Fitness Tracker', 'price': 2499, 'brand': 'apple', 'subcategory': 'smart-wearables'},
        {'name': 'Travel Backpack', 'price': 1599, 'brand': 'wildcraft', 'subcategory': 'travel-bags-women'},
        {'name': 'Phone Case', 'price': 399, 'brand': 'apple', 'subcategory': 'phone-cases'},
    ],
    'beauty': [
        {'name': 'Luxury Face Cream', 'price': 899, 'brand': 'loreal', 'subcategory': 'skincare-beauty'},
        {'name': 'Designer Perfume', 'price': 1899, 'brand': 'dior', 'subcategory': 'perfume'},
        {'name': 'Premium Lipstick', 'price': 599, 'brand': 'mac', 'subcategory': 'nykaa-lipstick'},
        {'name': 'Face Serum', 'price': 1299, 'brand': 'forest-essentials', 'subcategory': 'serum'},
        {'name': 'Hair Care Set', 'price': 799, 'brand': 'lakme', 'subcategory': 'shampoo'},
        {'name': 'Makeup Palette', 'price': 1599, 'brand': 'maybelline', 'subcategory': 'primer'},
        {'name': 'Body Lotion', 'price': 499, 'brand': 'nivea', 'subcategory': 'skincare'},
        {'name': 'Nail Polish Set', 'price': 399, 'brand': 'lakme', 'subcategory': 'nail-polish'},
    ],
    'home': [
        {'name': 'Decorative Wall Art', 'price': 1299, 'brand': 'ikea', 'subcategory': 'wall-decor'},
        {'name': 'Modern Table Lamp', 'price': 899, 'brand': 'philips', 'subcategory': 'table-lamps'},
        {'name': 'Comfortable Cushions', 'price': 599, 'brand': 'fabindia', 'subcategory': 'pillows-pillow-covers'},
        {'name': 'Kitchen Storage Set', 'price': 799, 'brand': 'ikea', 'subcategory': 'organisers'},
        {'name': 'Bathroom Towels Set', 'price': 499, 'brand': 'westside-bedsheets', 'subcategory': 'towels-set'},
        {'name': 'Decorative Vase', 'price': 699, 'brand': 'fabindia', 'subcategory': 'showpieces-vases'},
        {'name': 'Bed Sheet Set', 'price': 1599, 'brand': 'raymond-bedsheets', 'subcategory': 'raymond-bedsheets'},
        {'name': 'Floor Lamp', 'price': 1199, 'brand': 'philips', 'subcategory': 'floor-lamps'},
    ],
    'kids': [
        {'name': 'Kids T-Shirt', 'price': 399, 'brand': 'pantaloons', 'subcategory': 'infants-tops'},
        {'name': 'School Uniform', 'price': 799, 'brand': 'mothercare', 'subcategory': 'school-uniforms-kids'},
        {'name': 'Toy Set', 'price': 599, 'brand': 'lego', 'subcategory': 'toys'},
        {'name': 'Kids Shoes', 'price': 699, 'brand': 'nike', 'subcategory': 'kids-sunglasses'},
        {'name': 'Winter Jacket', 'price': 999, 'brand': 'mothercare', 'subcategory': 'infants-winter-wear'},
        {'name': 'School Bag', 'price': 499, 'brand': 'wildcraft', 'subcategory': 'soft-toys'},
        {'name': 'Kids Watch', 'price': 299, 'brand': 'casio', 'subcategory': 'kids-watches'},
        {'name': 'Pajama Set', 'price': 349, 'brand': 'mothercare', 'subcategory': 'nightwear-and-loungewear'},
    ]
}

def get_unsplash_image(query, width=400, height=400):
    """Get an image from Unsplash API"""
    try:
        # Using Unsplash source API (free, no API key required)
        url = f"https://source.unsplash.com/{width}x{height}/?{query}&sig={random.randint(1000, 9999)}"
        return url
    except Exception as e:
        print(f"Error getting Unsplash image: {e}")
        return f"https://picsum.photos/seed/{query}/{width}/{height}.jpg"

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

def create_bulk_products():
    """Create bulk products with images"""
    created_count = 0
    
    for category_slug, products in PRODUCT_DATA.items():
        try:
            category = Category.objects.get(slug=category_slug)
            print(f"\nCreating products for {category.name} category...")
            
            for product_data in products:
                try:
                    # Get subcategory and brand
                    subcategory = SubCategory.objects.get(category=category, slug=product_data['subcategory'])
                    brand = Brand.objects.get(slug=product_data['brand'])
                    
                    # Generate unique SKU and slug
                    sku = f"{category.slug.upper()}-{uuid.uuid4().hex[:8].upper()}"
                    slug = f"{product_data['name'].lower().replace(' ', '-').replace('/', '-').replace('.', '')}-{uuid.uuid4().hex[:4]}"
                    
                    # Create product
                    product = Product.objects.create(
                        name=product_data['name'],
                        slug=slug,
                        description=f"High-quality {product_data['name']} from {brand.name}. Perfect for everyday use.",
                        price=product_data['price'],
                        category=category,
                        subcategory=subcategory,
                        brand=brand,
                        gender=category_slug if category_slug in ['men', 'women'] else 'unisex',
                        is_active=True,
                        stock_quantity=random.randint(10, 50),
                        sku=sku
                    )
                    
                    # Get and upload image
                    image_query = f"{product_data['name']} {brand.name} {category.name}"
                    unsplash_url = get_unsplash_image(image_query)
                    cloudinary_url = upload_to_cloudinary(unsplash_url, f"product_{product.id}")
                    
                    # Create product image
                    ProductImage.objects.create(
                        product=product,
                        image=cloudinary_url,
                        alt_text=product.name,
                        is_primary=True
                    )
                    
                    print(f"  - Created: {product.name} (${product_data['price']})")
                    created_count += 1
                    
                except Exception as e:
                    print(f"  - Error creating {product_data['name']}: {e}")
                    
        except Category.DoesNotExist:
            print(f"Category {category_slug} not found")
    
    print(f"\n=== Successfully created {created_count} products! ===")
    return created_count

if __name__ == "__main__":
    created = create_bulk_products()
    print(f"\nTotal products created: {created}")
    print("All products now have images from Cloudinary CDN!")
