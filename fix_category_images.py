#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Category

print('=== Fixing Category Images ===')

# Define appropriate images for each category
category_images = {
    'beauty': 'https://images.unsplash.com/photo-1596462502278-27d4415415f2?w=800&h=600&fit=crop',
    'accessories': 'https://images.unsplash.com/photo-1524863479829-916d8e77f114?w=800&h=600&fit=crop',
    'home': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop',
    'kids': 'https://images.unsplash.com/photo-1514091189623-a2a7585aae13?w=800&h=600&fit=crop',
    'men': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&h=600&fit=crop',
    'women': 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=800&h=600&fit=crop',
    'new-arrivals': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&h=600&fit=crop',
    'top-brands': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&h=600&fit=crop'
}

categories = Category.objects.all()

for category in categories:
    print(f'Processing: {category.name} (Slug: {category.slug})')
    
    if category.slug in category_images:
        try:
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                category_images[category.slug],
                folder="categories",
                public_id=f"category_{category.slug}",
                overwrite=True
            )
            
            # Update category with new Cloudinary image
            category.image = result['public_id']
            category.save()
            
            print(f'  ✓ Updated with: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ✗ Error: {str(e)}')
    else:
        print(f'  - No image mapping found for {category.slug}')
    
    print('---')

print('=== Category Images Fix Complete ===')
