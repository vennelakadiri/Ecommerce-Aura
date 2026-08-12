#!/usr/bin/env python
import os
import sys
import django
import requests
from io import BytesIO

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Banner, Category, Brand
from django.core.files.uploadedfile import SimpleUploadedFile

def download_image(url, filename):
    """Download image from URL and return as SimpleUploadedFile"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Create SimpleUploadedFile
        uploaded_file = SimpleUploadedFile(
            name=filename,
            content=response.content,
            content_type='image/jpeg'
        )
        return uploaded_file
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def add_banner_images():
    """Add images to all banners"""
    print("Adding banner images...")
    
    banner_urls = [
        "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=2070",
        "https://img.freepik.com/premium-photo/banner-with-gold-jewelry-sale-is-displayed-gold-background_943617-40682.jpg",
        "https://mir-s3-cdn-cf.behance.net/project_modules/fs/d60b22179788335.6535ea2d5dc11.jpg",
        "https://images.unsplash.com/photo-1469334031218-e382a71b716b?q=80&w=2070"
    ]
    
    banners = Banner.objects.all()
    for i, banner in enumerate(banners):
        if i < len(banner_urls):
            image_file = download_image(banner_urls[i], f"banner_{banner.id}.jpg")
            if image_file:
                banner.image = image_file
                banner.save()
                print(f"Added image to Banner {banner.id}: {banner.title}")
            else:
                print(f"Failed to add image to Banner {banner.id}")

def add_category_images():
    """Add images to all categories"""
    print("\nAdding category images...")
    
    category_urls = {
        "Men": "https://marketplace.canva.com/EAE_cenV7wI/1/0/1131w/canva-white-classic-photocentric-fashion-magazine-cover-jIAqY7fZGiY.jpg",
        "Women": "https://www.mswordcoverpages.com/wp-content/uploads/2020/12/Fashion-design-cover-page-3-CRC.png",
        "Kids": "https://i.pinimg.com/474x/81/0f/c6/810fc60a1125baea6fc5168185d6f6c6.jpg?nii=t",
        "Accessories": "https://d1csarkz8obe9u.cloudfront.net/posterpreviews/fashion-sales-new-arrivals-instagram-story-design-template-debbfc0bb9eb5c5a53786529149de17d_screen.jpg?ts=1706184019",
        "Beauty": "https://png.pngtree.com/background/20230519/original/pngtree-store-with-hanging-clothing-in-a-high-end-environment-picture-image_2654941.jpg",
        "Home": "https://www.vanheusen.com.au/media/wysiwyg/VH/2021/710x780_VH_Suits.jpg",
        "TOP BRANDS": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg"
    }
    
    categories = Category.objects.all()
    for category in categories:
        if category.name in category_urls:
            image_file = download_image(category_urls[category.name], f"category_{category.slug}.jpg")
            if image_file:
                category.image = image_file
                category.save()
                print(f"Added image to Category {category.id}: {category.name}")
            else:
                print(f"Failed to add image to Category {category.name}")

def add_brand_logos():
    """Add logos to brands (first 10 brands as example)"""
    print("\nAdding brand logos...")
    
    brand_logos = {
        "Adidas": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Nike": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Puma": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Reebok": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Levi's": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Allen Solly": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Apple": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Axe": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Balenciaga": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg",
        "Zara": "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg"
    }
    
    brands = Brand.objects.all()[:10]  # First 10 brands
    for brand in brands:
        if brand.name in brand_logos:
            logo_file = download_image(brand_logos[brand.name], f"brand_{brand.slug}.jpg")
            if logo_file:
                brand.logo = logo_file
                brand.save()
                print(f"Added logo to Brand {brand.id}: {brand.name}")
            else:
                print(f"Failed to add logo to Brand {brand.name}")

def main():
    print("Starting to add cover page images...")
    print("=" * 50)
    
    try:
        add_banner_images()
        add_category_images()
        add_brand_logos()
        
        print("\n" + "=" * 50)
        print("Cover page images added successfully!")
        print("Please restart your Django server to see the changes.")
        
    except Exception as e:
        print(f"Error during image addition: {e}")

if __name__ == "__main__":
    main()
