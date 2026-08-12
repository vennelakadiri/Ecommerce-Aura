import os
import django
import re
from difflib import SequenceMatcher

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage, Category

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_matching_image(product_name, image_files):
    """Find the best matching image for a product"""
    product_name_clean = product_name.lower().replace(' ', '-').replace("'", "")
    
    # First try exact match
    for img_file in image_files:
        img_name = img_file.lower().replace('_', '-').replace('.jpg', '')
        if product_name_clean in img_name or img_name in product_name_clean:
            return img_file
    
    # Then try similarity match
    best_match = None
    best_score = 0.5  # Minimum threshold
    
    for img_file in image_files:
        img_name = img_file.lower().replace('_', '-').replace('.jpg', '')
        score = similarity(product_name_clean, img_name)
        if score > best_score:
            best_score = score
            best_match = img_file
    
    return best_match

def get_unsplash_image(product_name):
    """Get relevant Unsplash image based on product keywords"""
    product_lower = product_name.lower()
    
    # Specific Unsplash images for Men's products
    if 'watch' in product_lower:
        return "https://images.unsplash.com/photo-1523275335684-3147f3842f27?w=400&h=400&fit=crop"
    elif 'sneakers' in product_lower or 'shoes' in product_lower:
        return "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"
    elif 'wallet' in product_lower:
        return "https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop"
    elif 'blazer' in product_lower or 'jacket' in product_lower:
        return "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop"
    elif 'shirt' in product_lower:
        if 'formal' in product_lower or 'oxford' in product_lower:
            return "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=400&fit=crop"
        elif 'polo' in product_lower:
            return "https://images.unsplash.com/photo-1625910513413-5fc45e99f3c7?w=400&h=400&fit=crop"
        elif 't-shirt' in product_lower or 'tshirt' in product_lower:
            return "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop"
        else:
            return "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=400&h=400&fit=crop"
    elif 'jeans' in product_lower:
        return "https://images.unsplash.com/photo-1542272617-08f086302d36?w=400&h=400&fit=crop"
    elif 'trousers' in product_lower or 'chinos' in product_lower:
        return "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400&h=400&fit=crop"
    elif 'suit' in product_lower:
        return "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&h=400&fit=crop"
    elif 'tie' in product_lower:
        return "https://images.unsplash.com/photo-1589756823695-278bc923f962?w=400&h=400&fit=crop"
    elif 'belt' in product_lower:
        return "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop"
    elif 'shorts' in product_lower:
        return "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop"
    elif 'sweater' in product_lower:
        return "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop"
    elif 'hoodie' in product_lower:
        return "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop"
    elif 'kurta' in product_lower:
        return "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400&h=400&fit=crop"
    elif 'dhoti' in product_lower:
        return "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400&h=400&fit=crop"
    else:
        return "https://images.unsplash.com/photo-1617137968427-85924c800a22?w=400&h=400&fit=crop"

def update_men_products():
    """
    Update Men category products with relevant images.
    First tries to match with existing media images, then falls back to Unsplash.
    """
    # Get Men category
    men_category = Category.objects.filter(name='Men').first()
    if not men_category:
        print("Men category not found!")
        return
    
    # Get all Men products
    products = Product.objects.filter(category=men_category)
    total_products = products.count()
    print(f"Found {total_products} Men category products")
    
    # Get existing product images from media folder
    products_dir = 'media/products'
    image_files = []
    if os.path.exists(products_dir):
        image_files = [f for f in os.listdir(products_dir) if f.endswith('.jpg')]
        # Remove duplicates
        unique_images = {}
        for img in image_files:
            base_name = re.sub(r'_temp_image_\w+\.jpg$', '', img)
            base_name = re.sub(r'_\w{8}\.jpg$', '', base_name)
            if base_name not in unique_images:
                unique_images[base_name] = img
        image_files = list(unique_images.values())
        print(f"Found {len(image_files)} unique images in media folder")
    
    print("=" * 60)
    
    matched_media = 0
    used_unsplash = 0
    
    for index, product in enumerate(products, 1):
        print(f"\n[{index}/{total_products}] Processing: {product.name}")
        
        # First try to find matching image in media folder
        matching_image = find_matching_image(product.name, image_files)
        
        if matching_image:
            image_url = f"/media/products/{matching_image}"
            print(f"  ✓ Using media image: {matching_image}")
            matched_media += 1
        else:
            # Fall back to Unsplash
            image_url = get_unsplash_image(product.name)
            print(f"  ✓ Using Unsplash image")
            used_unsplash += 1
        
        # Update product images
        existing_images = product.images.all()
        
        if existing_images.exists():
            for img in existing_images:
                img.image = image_url
                img.alt_text = f"{product.name} - Men's Fashion"
                img.save()
        else:
            ProductImage.objects.create(
                product=product,
                image=image_url,
                is_primary=True,
                alt_text=f"{product.name} - Men's Fashion"
            )
        
        # Progress indicator
        if index % 50 == 0:
            print(f"\n--- Progress: {index}/{total_products} ---")
            print(f"Media images: {matched_media}, Unsplash: {used_unsplash}")
    
    print("\n" + "=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)
    print(f"Total products: {total_products}")
    print(f"Matched with media images: {matched_media}")
    print(f"Used Unsplash images: {used_unsplash}")
    print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("UPDATE MEN CATEGORY PRODUCTS")
    print("=" * 60)
    print("This script will update Men category products with")
    print("relevant images from media folder and Unsplash.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_men_products()
    else:
        print("Operation cancelled.")
