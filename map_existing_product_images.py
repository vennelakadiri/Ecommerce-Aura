import os
import django
import re
from difflib import SequenceMatcher

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

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

def map_existing_images_to_products():
    """
    Map existing product images in media/products/ to products based on name matching.
    """
    # Get all product images from media folder
    products_dir = 'media/products'
    if not os.path.exists(products_dir):
        print(f"Products directory not found: {products_dir}")
        return
    
    image_files = [f for f in os.listdir(products_dir) if f.endswith('.jpg')]
    print(f"Found {len(image_files)} images in {products_dir}")
    
    # Remove duplicates (keep only one version of each image)
    unique_images = {}
    for img in image_files:
        # Extract base name (remove temp_image_XXX suffixes)
        base_name = re.sub(r'_temp_image_\w+\.jpg$', '', img)
        base_name = re.sub(r'_\w{8}\.jpg$', '', base_name)  # Remove hash suffixes
        if base_name not in unique_images:
            unique_images[base_name] = img
        else:
            # Keep the shorter filename (usually the original)
            if len(img) < len(unique_images[base_name]):
                unique_images[base_name] = img
    
    image_files = list(unique_images.values())
    print(f"After deduplication: {len(image_files)} unique images")
    
    # Get all products
    products = Product.objects.all()
    total_products = products.count()
    print(f"Found {total_products} products in database")
    print("=" * 60)
    
    matched_count = 0
    unmatched_count = 0
    
    for index, product in enumerate(products, 1):
        print(f"\n[{index}/{total_products}] Processing: {product.name}")
        
        # Find matching image
        matching_image = find_matching_image(product.name, image_files)
        
        if matching_image:
            # Construct media URL
            image_url = f"/media/products/{matching_image}"
            
            # Get existing images
            existing_images = product.images.all()
            
            if existing_images.exists():
                # Update existing images
                for img in existing_images:
                    img.image = image_url
                    img.alt_text = f"{product.name} - {product.category.name}"
                    img.save()
                print(f"  ✓ Updated with: {matching_image}")
            else:
                # Create new image
                ProductImage.objects.create(
                    product=product,
                    image=image_url,
                    is_primary=True,
                    alt_text=f"{product.name} - {product.category.name}"
                )
                print(f"  ✓ Created with: {matching_image}")
            
            matched_count += 1
        else:
            print(f"  ✗ No matching image found")
            unmatched_count += 1
        
        # Progress indicator
        if index % 100 == 0:
            print(f"\n--- Progress: {index}/{total_products} ---")
            print(f"Matched: {matched_count}, Unmatched: {unmatched_count}")
    
    print("\n" + "=" * 60)
    print("MAPPING COMPLETE")
    print("=" * 60)
    print(f"Total products: {total_products}")
    print(f"Matched: {matched_count}")
    print(f"Unmatched: {unmatched_count}")
    print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("MAP EXISTING PRODUCT IMAGES")
    print("=" * 60)
    print("This script will map existing product images from")
    print("media/products/ to products based on name matching.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        map_existing_images_to_products()
    else:
        print("Operation cancelled.")
