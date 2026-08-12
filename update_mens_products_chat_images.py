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

def update_mens_products_with_chat_images():
    """Update all men's category products with their correct image URLs from chat data"""
    
    # Define the exact mappings for men's products from chat data
    mens_product_mappings = {
        'Business Trousers': 'https://www.aesido.com/cdn/shop/files/aesido-men-s-business-trousers-30805791572014.jpg?v=1704584529',
        'Dress Shirt': 'https://shop.bluffworks.com/cdn/shop/products/Mens.9-28_00114.jpg?v=1698077052',
        'Formal Blazer': 'https://imagescdn.louisphilippe.com/img/app/product/3/39687978-14048162.jpg',
        'Formal Suit': 'https://www.reviewtique.com/wp-content/uploads/2024/12/formal-suits-men.webp',
        'Leather Wallet': 'https://i.etsystatic.com/16971055/r/il/4e0cf5/3021061575/il_1588xN.3021061575_7om9.jpg',
        'Silk Tie': 'https://media.neimanmarcus.com/f_auto,q_auto/01/nm_4489966_100551_m',
        'Slim Fit Jeans': 'https://imagescdn.louisphilippe.com/img/app/product/4/40077201-21886843.jpg?auto=format&w=390',
        'Winter Jacket': 'https://i5.walmartimages.com/seo/Ierhent-Kid-Big-Boys-Winter-Coats-Jackets-Kids-Lightweight-Padded-Hooded-Puffer-Autumn-and-Winter-Coat-Grey-13-14-Years_51d40446-2594-46b2-ae2f-20ec2d8d1fa1.0778d786bb6a2567a6e83fbe6c869910.jpeg',
    }
    
    print("=== UPDATING MEN'S CATEGORY PRODUCTS WITH CHAT IMAGES ===")
    print()
    
    # Get all men's category products
    mens_products = Product.objects.filter(category__name='Men')
    total_updated = 0
    total_found = 0
    
    for product in mens_products:
        product_name = product.name
        print(f"Processing: {product_name} (ID: {product.id})")
        
        # Find matching image URL
        image_url = None
        for key, url in mens_product_mappings.items():
            if key.lower() in product_name.lower():
                image_url = url
                total_found += 1
                break
        
        if image_url:
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
        else:
            print(f"  No matching image URL found for this product")
        
        print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Total men's products processed: {mens_products.count()}")
    print(f"Products with matching images: {total_found}")
    print(f"Successfully updated: {total_updated}")
    print(f"Products without matching images: {mens_products.count() - total_found}")
    
    print("\n=== PRODUCTS UPDATED ===")
    for key, url in mens_product_mappings.items():
        products = Product.objects.filter(category__name='Men', name__icontains=key.lower())
        if products.exists():
            product = products.first()
            images = ProductImage.objects.filter(product=product)
            if images.exists():
                print(f"  {key}: {images.first().image.url if hasattr(images.first().image, 'url') else str(images.first().image)}")

if __name__ == "__main__":
    update_mens_products_with_chat_images()
