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

def force_update_specific_images():
    """Force update specific products with their correct image URLs"""
    
    # Define the exact mappings for our target products
    specific_mappings = {
        'Evening Clutch': 'https://down-my.img.susercontent.com/file/sg-11134201-7qvcs-liftn4g5c3fw6c',
        'Yoga Pants': 'https://cdn-img.prettylittlething.com/f/c/d/b/fcdb73b680066d5e235a4d9cdec973e3d18e6797_CNF7400_1_bone_ultimate_sculpt_flare_yoga_pants.jpg?imwidth=600',
        'Fashion Scarf': 'https://i.pinimg.com/originals/3e/96/3c/3e963ce5e09958c28dad83b7713d9b93.png',
        'Stylish Heels': 'https://i.pinimg.com/originals/54/83/e2/5483e23615637716efbb4c6a4468a47a.jpg',
        'Designer Handbag': 'https://image.made-in-china.com/2f0j00WKnbeElFkokI/Luxury-Handbags-Women-Bags-Designer-Shoulder-Bag-High-Quality-Soft-Leather-Purses-and-Handbags-3-Layer-Large-Capacity-Tote-Bag.webp',
        'Floral Summer Dress': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjTfW2Gdaagj-meCJW9YtG3yC8_VSGnBsF9CMB9_9AXuL66WibRvVXXOAD5hlohK47NDXFFCt4XGUejM9cpfsuhBcwyLwG5SKgSojAYkQjRaPitJjEohyuqK8UuHoC9SfUMRTm0CMZb1M2s/s1600/Floral+Summer+Dresses6.jpg',
        'Sport Sandals': 'https://img.ltwebstatic.com/images3_pi/2023/06/16/16868808355d27ec229722af7cc53f5f7f0200ea29_thumbnail_900x.webp',
        'Platform Sandals': 'https://m.media-amazon.com/images/I/81zzreJyFzS._AC_SL1500_.jpg',
    }
    
    print("=== FORCE UPDATING SPECIFIC PRODUCT IMAGES ===")
    print()
    
    for product_name, image_url in specific_mappings.items():
        print(f"Processing: {product_name}")
        
        # Find the product
        products = Product.objects.filter(name__icontains=product_name.lower())
        if not products.exists():
            print(f"  ERROR: Product '{product_name}' not found")
            continue
            
        product = products.first()
        print(f"  Found: {product.name} (ID: {product.id})")
        
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
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        print()
    
    print("=== FORCE UPDATE COMPLETED ===")

if __name__ == "__main__":
    force_update_specific_images()
