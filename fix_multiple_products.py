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

# Product-specific image mappings
product_image_mappings = {
    # Leather Wallet
    1314: 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=400&fit=crop&bg=white',  # Puma wallet
    378: 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=400&fit=crop&bg=white',   # Coach wallet
    213: 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=400&h=400&fit=crop&bg=white',  # Tommy Hilfiger wallet
    
    # Sports Shoes
    1313: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&bg=white',  # Nike shoes
    
    # Formal Blazer
    1312: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',  # Park Avenue blazer
    
    # Polo T-Shirt
    1311: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',  # USPA polo
    1275: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',  # Jack & Jones polo
    1239: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',  # Jack & Jones polo
    
    # Slim Fit Jeans
    1310: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&bg=white',  # Levi's jeans
    1273: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&bg=white',  # Jack & Jones jeans
    1237: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&bg=white',  # Jack & Jones jeans
    
    # Classic Oxford Shirt
    1309: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',  # Allen Solly shirt
    
    # Silk Tie
    1299: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop&bg=white',  # Van Heusen tie
    1263: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop&bg=white',  # Van Heusen tie
    
    # Business Trousers
    1298: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop&bg=white',  # Van Heusen trousers
    1262: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop&bg=white',  # Van Heusen trousers
    
    # Dress Shirt
    1297: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',  # Van Heusen dress shirt
    1261: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',  # Van Heusen dress shirt
    
    # Formal Suit
    1296: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop&bg=white',  # Van Heusen suit
    1260: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop&bg=white',  # Van Heusen suit
}

def fix_product_images():
    """Fix all specified products with proper images"""
    
    print("=== FIXING MULTIPLE PRODUCT IMAGES ===")
    
    for product_id, image_url in product_image_mappings.items():
        try:
            # Get the product
            product = Product.objects.get(id=product_id)
            print(f"\n[{product_id}] Updating: {product.name} ({product.brand.name})")
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                image_url,
                folder='products',
                public_id=f'product_{product_id}_{product.slug.replace("-", "_")}',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=product).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=product,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            
        except Product.DoesNotExist:
            print(f"  ERROR: Product {product_id} not found")
        except Exception as e:
            print(f"  ERROR: {str(e)}")
    
    print(f"\n=== COMPLETED ===")
    print(f"Processed {len(product_image_mappings)} products")

if __name__ == "__main__":
    fix_product_images()
