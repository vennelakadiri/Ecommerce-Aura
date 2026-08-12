#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import ProductImage

def remove_all_product_images():
    """
    Remove all product images from the database while keeping:
    - Banner images (home page scrolling)
    - Category images (cover pages)
    - Brand images (cover pages)
    """
    try:
        # Count images before deletion
        image_count = ProductImage.objects.count()
        print(f"Found {image_count} product images in the database")
        
        if image_count == 0:
            print("No product images found to remove.")
            return
        
        # Get all product images
        product_images = ProductImage.objects.all()
        
        # Delete each image file from filesystem and database
        deleted_count = 0
        for img in product_images:
            try:
                # Delete the actual image file from filesystem
                if img.image and os.path.exists(img.image.path):
                    os.remove(img.image.path)
                    print(f"Deleted file: {img.image.path}")
                
                # Delete the database record
                img.delete()
                deleted_count += 1
                
            except Exception as e:
                print(f"Error deleting image {img.id}: {e}")
        
        print(f"\nSuccessfully removed {deleted_count} product images from database")
        print("Banner images, Category images, and Brand images remain intact")
        
    except Exception as e:
        print(f"Error during image removal: {e}")

if __name__ == "__main__":
    print("Starting product image removal process...")
    remove_all_product_images()
    print("Process completed.")
