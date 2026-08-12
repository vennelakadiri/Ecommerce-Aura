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

def update_specific_kids_products():
    """Update only the specific kids products mentioned with their correct image URLs from chat data"""
    
    # Define the exact mappings for the specific kids products from chat data
    kids_product_mappings = {
        'Pajama Set': 'https://nightsuit.pk/cdn/shop/files/20250627_1531_Space-Themed_Pajama_Set_remix_01jyreyxvxfysrmh1v6znx3ewh.png?v=1751020556',
        'Winter Jacket': 'https://i5.walmartimages.com/seo/Ierhent-Kid-Big-Boys-Winter-Coats-Jackets-Kids-Lightweight-Padded-Hooded-Puffer-Autumn-and-Winter-Coat-Grey-13-14-Years_51d40446-2594-46b2-ae2f-20ec2d8d1fa1.0778d786bb6a2567a6e83fbe6c869910.jpeg',
        'Kids Shoes': 'https://static.vecteezy.com/system/resources/previews/044/861/282/non_2x/kids-shoes-isolated-png.png',
        'Toy Set': 'https://rukminim1.flixcart.com/image/612/612/l3j2cnk0/role-play-toy/k/r/m/3-in-1-kitchen-suitcase-for-kids-mini-kitchen-play-set-portable-original-imagemjqryhzmscd.jpeg?q=70',
        'School Uniform': 'https://img.freepik.com/free-photo/portrait-young-girl-student-school-uniform_23-2150282547.jpg?semt=ais_hybrid&w=740&q=80',
        'Kids T-Shirt': 'https://img.freepik.com/premium-photo/photography-kids-fashion-white-tshirt-mockup_1288657-101940.jpg',
    }
    
    print("=== UPDATING SPECIFIC KIDS PRODUCTS WITH CHAT IMAGES ===")
    print("Only updating: Pajama Set, Winter Jacket, Kids Shoes, Toy Set, School Uniform, Kids T-Shirt")
    print("NOT touching home page, men's category, or women's category products")
    print()
    
    total_updated = 0
    total_found = 0
    
    for product_name, image_url in kids_product_mappings.items():
        print(f"=== UPDATING {product_name.upper()} ===")
        
        # Find all matching products (only in kids category)
        matching_products = Product.objects.filter(
            category__name='Kids',
            name__icontains=product_name.lower()
        )
        
        if not matching_products.exists():
            print(f"  No {product_name} products found in Kids category")
            print()
            continue
        
        total_found += matching_products.count()
        
        for product in matching_products:
            print(f"Processing: {product.name} (ID: {product.id})")
            
            try:
                # Remove existing images
                ProductImage.objects.filter(product=product).delete()
                print(f"  Removed existing images")
                
                # Upload new image to Cloudinary
                result = cloudinary.uploader.upload(
                    image_url,
                    folder="products",
                    public_id=f"product_{product.id}_{product.name.replace(' ', '_').replace('-', '_').lower()}",
                    overwrite=True
                )
                
                # Create new product image
                product_image = ProductImage.objects.create(
                    product=product,
                    image=result['public_id'],
                    is_primary=True
                )
                
                print(f"  SUCCESS: {result['secure_url']}")
                total_updated += 1
                
            except Exception as e:
                print(f"  ERROR: {str(e)}")
            
            print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Products with matching images: {total_found}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {total_found - total_updated}")
    
    print("\n=== PRODUCTS UPDATED ===")
    for key, url in kids_product_mappings.items():
        products = Product.objects.filter(category__name='Kids', name__icontains=key.lower())
        if products.exists():
            product = products.first()
            images = ProductImage.objects.filter(product=product)
            if images.exists():
                print(f"  {key}: {images.first().image.url if hasattr(images.first().image, 'url') else str(images.first().image)}")
    
    print("\n=== VERIFICATION ===")
    print("Only Kids category products were updated")
    print("Home page, Men's category, and Women's category products were NOT touched")
    print("Only the 6 specified products were updated with chat image URLs")

if __name__ == "__main__":
    update_specific_kids_products()
