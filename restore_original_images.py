#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Banner, Category, Brand
from django.core.files import File

def restore_banner_images():
    """Restore original banner images from media folder"""
    print("Restoring banner images...")
    
    banner_files = {
        1: "banner_1.jpg",
        2: "banner_2.jpg", 
        3: "banner_3.jpg",
        4: "banner_4.jpg"
    }
    
    for banner_id, filename in banner_files.items():
        try:
            banner = Banner.objects.get(id=banner_id)
            file_path = f"media/banners/{filename}"
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    banner.image.save(filename, File(f), save=True)
                print(f"Restored Banner {banner_id}: {banner.title} -> {filename}")
            else:
                print(f"File not found: {file_path}")
        except Banner.DoesNotExist:
            print(f"Banner {banner_id} not found")
        except Exception as e:
            print(f"Error restoring banner {banner_id}: {e}")

def restore_category_images():
    """Restore original category images from media folder"""
    print("\nRestoring category images...")
    
    category_files = {
        "men": "category_men.jpg",
        "women": "category_women.jpg", 
        "kids": "category_kids.jpg",
        "accessories": "category_accessories.jpg",
        "home": "category_home.jpg",
        "top-brands": "category_top-brands.jpg"
    }
    
    for category_slug, filename in category_files.items():
        try:
            category = Category.objects.get(slug=category_slug)
            file_path = f"media/categories/{filename}"
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    category.image.save(filename, File(f), save=True)
                print(f"Restored Category {category.name} -> {filename}")
            else:
                print(f"File not found: {file_path}")
        except Category.DoesNotExist:
            print(f"Category {category_slug} not found")
        except Exception as e:
            print(f"Error restoring category {category_slug}: {e}")

def restore_brand_logos():
    """Restore original brand logos from media folder"""
    print("\nRestoring brand logos...")
    
    brand_files = {
        "adidas": "brand_adidas.jpg",
        "allen-solly": "brand_allen-solly.jpg",
        "apple": "brand_apple.jpg", 
        "axe": "brand_axe.jpg",
        "balenciaga": "brand_balenciaga.jpg"
    }
    
    for brand_slug, filename in brand_files.items():
        try:
            brand = Brand.objects.get(slug=brand_slug)
            file_path = f"media/brands/{filename}"
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    brand.logo.save(filename, File(f), save=True)
                print(f"Restored Brand {brand.name} -> {filename}")
            else:
                print(f"File not found: {file_path}")
        except Brand.DoesNotExist:
            print(f"Brand {brand_slug} not found")
        except Exception as e:
            print(f"Error restoring brand {brand_slug}: {e}")

def main():
    print("Restoring original cover page images...")
    print("=" * 50)
    
    try:
        restore_banner_images()
        restore_category_images()
        restore_brand_logos()
        
        print("\n" + "=" * 50)
        print("Original cover page images restored successfully!")
        print("Please restart your Django server to see the changes.")
        
    except Exception as e:
        print(f"Error during image restoration: {e}")

if __name__ == "__main__":
    main()
