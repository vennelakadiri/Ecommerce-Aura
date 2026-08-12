#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Category

# Update or create categories with the correct names and images
categories_data = [
    {
        'name': 'Men',
        'slug': 'men',
        'image_url': 'https://marketplace.canva.com/EAE_cenV7wI/1/0/1131w/canva-white-classic-photocentric-fashion-magazine-cover-jIAqY7fZGiY.jpg'
    },
    {
        'name': 'Women', 
        'slug': 'women',
        'image_url': 'https://www.mswordcoverpages.com/wp-content/uploads/2020/12/Fashion-design-cover-page-3-CRC.png'
    },
    {
        'name': 'Accessories',
        'slug': 'accessories', 
        'image_url': 'https://i.pinimg.com/474x/81/0f/c6/810fc60a1125baea6fc5168185d6f6c6.jpg?nii=t'
    },
    {
        'name': 'New Arrivals',
        'slug': 'new-arrivals',
        'image_url': 'https://d1csarkz8obe9u.cloudfront.net/posterpreviews/fashion-sales-new-arrivals-instagram-story-design-template-debbfc0bb9eb5c5a53786529149de17d_screen.jpg?ts=1706184019'
    }
]

print("Updating categories...")
for cat_data in categories_data:
    category, created = Category.objects.update_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': f'{cat_data["name"]} category',
            'is_active': True
        }
    )
    
    # Update image if URL is provided
    if cat_data['image_url']:
        import requests
        from django.core.files.base import ContentFile
        from io import BytesIO
        
        try:
            response = requests.get(cat_data['image_url'])
            if response.status_code == 200:
                # Get filename from URL
                filename = f"{cat_data['slug']}_category.jpg"
                category.image.save(filename, ContentFile(response.content))
                category.save()
                print(f"✓ Updated {cat_data['name']} category with new image")
            else:
                print(f"✗ Failed to download image for {cat_data['name']}")
        except Exception as e:
            print(f"✗ Error updating {cat_data['name']}: {e}")
    
    print(f"{'Created' if created else 'Updated'}: {category.name} ({category.slug})")

print("\nCurrent categories in database:")
for cat in Category.objects.filter(is_active=True):
    print(f"- {cat.name} ({cat.slug}) - Image: {'Yes' if cat.image else 'No'}")
