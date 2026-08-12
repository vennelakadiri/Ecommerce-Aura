#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

import cloudinary
import cloudinary.uploader
import cloudinary.api

print("=== Testing Cloudinary Upload ===")

# Test Cloudinary configuration
try:
    print(f"Cloud Name: {cloudinary.config().cloud_name}")
    print(f"API Key: {cloudinary.config().api_key}")
    print("Cloudinary configuration loaded successfully!")
except Exception as e:
    print(f"Error loading Cloudinary config: {e}")

# Test uploading a sample image
try:
    print("\nTesting image upload...")
    # Upload a sample image from URL
    result = cloudinary.uploader.upload(
        "https://picsum.photos/seed/test-cloudinary-upload/400/400.jpg",
        public_id="test_product_image_django",
        folder="products",
        resource_type="image"
    )
    print(f"Upload successful!")
    print(f"Public ID: {result['public_id']}")
    print(f"URL: {result['url']}")
    print(f"Secure URL: {result['secure_url']}")
    print(f"Format: {result['format']}")
    print(f"Size: {result['bytes']} bytes")
    
    # Test image transformation
    transformed_url = cloudinary.utils.cloudinary_url(
        result['public_id'],
        width=200,
        height=200,
        crop='fill',
        format='jpg'
    )[0]
    print(f"Transformed URL: {transformed_url}")
    
    print("\n=== Cloudinary integration is working! ===")
    print("You can now upload images through Django admin!")
    
except Exception as e:
    print(f"Error uploading image: {e}")
    print("Check your API secret and network connection")
