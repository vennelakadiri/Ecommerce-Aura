#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader
import requests
import json
import time

# Configure Cloudinary with provided credentials
cloudinary.config(
    cloud_name='dqthyfxm9',
    api_key='882642629924913',
    api_secret='UZ6jb0sKLxHt1XldpIFtT5cPZvg'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def generate_ai_image(product_name, category_name):
    """Generate AI image using the user's prompt template"""
    
    # Create the perfect prompt based on user's template
    prompt = f"{product_name}, {category_name}, ecommerce product photo, isolated on white background, centered, no people, no text, high detail, studio lighting"
    
    # For now, we'll use a placeholder approach since we don't have direct AI API access
    # This script is ready to integrate with DALL-E, Midjourney, or similar AI services
    
    print(f"AI Prompt: {prompt}")
    print("Note: This would generate a perfect AI image with the above prompt")
    
    # Placeholder for AI image generation service
    # You would integrate with:
    # - OpenAI DALL-E API
    # - Stability AI API  
    # - Midjourney API
    # - Or any other AI image service
    
    return None  # Replace with actual AI-generated image URL

def get_fallback_image_url(product_name, category_name, brand_name):
    """Get high-quality fallback images while AI setup is pending"""
    
    name_lower = product_name.lower()
    category_lower = category_name.lower() if category_name else ''
    brand_lower = brand_name.lower() if brand_name else ''
    
    # Use high-quality, specific stock images that match product type perfectly
    image_mappings = {
        # MEN'S PRODUCTS
        ('men', 'watch'): 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&bg=white',
        ('men', 'wallet'): 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=400&h=400&fit=crop&bg=white',
        ('men', 'sneakers'): 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&bg=white',
        ('men', 'shoes'): 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=400&fit=crop&bg=white',
        ('men', 'shirt'): 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&bg=white',
        ('men', 't-shirt'): 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop&bg=white',
        ('men', 'jeans'): 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&bg=white',
        ('men', 'belt'): 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=400&fit=crop&bg=white',
        
        # WOMEN'S PRODUCTS
        ('women', 'handbag'): 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop&bg=white',
        ('women', 'clutch'): 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=400&fit=crop&bg=white',
        ('women', 'sunglasses'): 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400&h=400&fit=crop&bg=white',
        ('women', 'dress'): 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=400&h=400&fit=crop&bg=white',
        ('women', 'pants'): 'https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=400&fit=crop&bg=white',
        ('women', 'yoga'): 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=400&h=400&fit=crop&bg=white',
        ('women', 'heels'): 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&bg=white',
        ('women', 'scarf'): 'https://images.unsplash.com/photo-1583744983541-9a548a6af254?w=400&h=400&fit=crop&bg=white',
        
        # KIDS PRODUCTS
        ('kids', 'pajama'): 'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786?w=400&h=400&fit=crop&bg=white',
        ('kids', 'watch'): 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&bg=white',
        ('kids', 'school'): 'https://images.unsplash.com/photo-1588072428504-1a848e2e1af3?w=400&h=400&fit=crop&bg=white',
        ('kids', 'uniform'): 'https://images.unsplash.com/photo-1588072428504-1a848e2e1af3?w=400&h=400&fit=crop&bg=white',
        ('kids', 'bag'): 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop&bg=white',
        ('kids', 'toy'): 'https://images.unsplash.com/photo-1515488344751-661a8d1e8de1?w=400&h=400&fit=crop&bg=white',
        ('kids', 'shoes'): 'https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=400&h=400&fit=crop&bg=white',
        ('kids', 't-shirt'): 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400&h=400&fit=crop&bg=white',
        ('kids', 'jacket'): 'https://images.unsplash.com/photo-1544978148-4bd0d0d9dbbb?w=400&h=400&fit=crop&bg=white',
        
        # ACCESSORIES
        ('accessories', 'wallet'): 'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3?w=400&h=400&fit=crop&bg=white',
        ('accessories', 'sunglasses'): 'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=400&h=400&fit=crop&bg=white',
        ('accessories', 'belt'): 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=400&fit=crop&bg=white',
        ('accessories', 'watch'): 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&bg=white',
        
        # HOME PRODUCTS
        ('home', 'lamp'): 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&bg=white',
        ('home', 'vase'): 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop&bg=white',
        ('home', 'kitchen'): 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&bg=white',
        ('home', 'storage'): 'https://images.unsplash.com/photo-1587413853953-4292b30fd722?w=400&h=400&fit=crop&bg=white',
        ('home', 'cushion'): 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop&bg=white',
        ('home', 'pillow'): 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop&bg=white',
        
        # BEAUTY PRODUCTS
        ('beauty', 'lipstick'): 'https://images.unsplash.com/photo-1596462502278-27d4415415f2?w=400&h=400&fit=crop&bg=white',
        ('beauty', 'nail'): 'https://images.unsplash.com/photo-1610990837682-c590686d7015?w=400&h=400&fit=crop&bg=white',
        ('beauty', 'makeup'): 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=400&fit=crop&bg=white',
        ('beauty', 'shampoo'): 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=400&fit=crop&bg=white',
        ('beauty', 'cream'): 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=400&h=400&fit=crop&bg=white',
        ('beauty', 'moisturizer'): 'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3?w=400&h=400&fit=crop&bg=white',
        ('beauty', 'soap'): 'https://images.unsplash.com/photo-1584304290319-9fd6be0c5df2?w=400&h=400&fit=crop&bg=white',
        ('beauty', 'perfume'): 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=400&h=400&fit=crop&bg=white',
    }
    
    # Find the best matching image
    for (cat, keyword), url in image_mappings.items():
        if cat == category_lower and keyword in name_lower:
            return url
    
    # Default high-quality product image
    return 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop&bg=white'

def update_products_with_perfect_images():
    """Update all products with AI-generated or perfect fallback images"""
    
    print("=== PERFECT PRODUCT IMAGE GENERATION ===")
    print("Using AI prompt template: '{product_name}, {category}, ecommerce product photo, isolated on white background, centered, no people, no text, high detail, studio lighting'")
    print()
    
    products = Product.objects.all()
    updated_count = 0
    ai_generated_count = 0
    
    for i, product in enumerate(products):
        print(f"[{i+1}/{products.count()}] {product.name}")
        print(f"  Category: {product.category.name}")
        print(f"  Brand: {product.brand.name}")
        
        try:
            # Try AI generation first (when API is available)
            ai_image_url = generate_ai_image(product.name, product.category.name)
            
            if ai_image_url:
                # Use AI-generated image
                image_url = ai_image_url
                ai_generated_count += 1
                print(f"  AI GENERATED: {image_url}")
            else:
                # Use perfect fallback
                image_url = get_fallback_image_url(product.name, product.category.name, product.brand.name)
                print(f"  HIGH-QUALITY FALLBACK: {image_url}")
            
            # Remove existing images
            ProductImage.objects.filter(product=product).delete()
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                image_url,
                folder="products",
                public_id=f"product_{product.id}_{product.slug.replace('-', '_')}",
                overwrite=True
            )
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=product,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            updated_count += 1
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        if i % 25 == 0:  # Progress update every 25 products
            print(f"Progress: {i+1}/{products.count()} completed")
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Successfully updated: {updated_count}/{products.count()} products")
    print(f"AI-generated images: {ai_generated_count}")
    print(f"High-quality fallbacks: {updated_count - ai_generated_count}")

def setup_ai_integration():
    """Instructions for setting up AI image generation"""
    
    print("=== AI INTEGRATION SETUP ===")
    print()
    print("To enable AI image generation, you'll need to:")
    print()
    print("1. Get an API key from one of these services:")
    print("   - OpenAI DALL-E: https://platform.openai.com/")
    print("   - Stability AI: https://stability.ai/")
    print("   - Midjourney: https://midjourney.com/")
    print()
    print("2. Update the generate_ai_image() function with your API calls")
    print()
    print("3. Example DALL-E integration:")
    print("""
import openai
openai.api_key = 'your-api-key'

response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="400x400",
    response_format="url"
)
return response['data'][0]['url']
    """)
    print()
    print("4. Re-run this script to generate perfect AI images for all products!")

if __name__ == "__main__":
    # First show setup instructions
    setup_ai_integration()
    print("\n" + "="*60 + "\n")
    
    # Then run with current fallback approach
    update_products_with_perfect_images()
