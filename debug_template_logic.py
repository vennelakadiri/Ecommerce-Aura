#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def debug_template_logic():
    """Debug template logic for brand logo display"""
    
    print("=== DEBUGGING TEMPLATE LOGIC ===")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara brand logo field: {zara_brand.logo}")
        print(f"Logo field type: {type(zara_brand.logo)}")
        
        # Test different ways to access the logo
        print("\n=== TESTING DIFFERENT ACCESS METHODS ===")
        
        # Method 1: Direct field access
        print(f"1. Direct access: {zara_brand.logo}")
        
        # Method 2: URL method
        if hasattr(zara_brand.logo, 'url'):
            logo_url = zara_brand.logo.url
            print(f"2. URL method: {logo_url}")
        else:
            print("2. URL method: NOT AVAILABLE")
        
        # Method 3: String conversion
        logo_str = str(zara_brand.logo)
        print(f"3. String conversion: {logo_str}")
        
        # Method 4: Check if it's a URL string
        if logo_str.startswith('http'):
            print("4. Type: External URL")
        elif logo_str.startswith('/media/'):
            print("4. Type: Local media URL")
        else:
            print("4. Type: Other format")
        
        # Test template simulation
        print("\n=== TEMPLATE SIMULATION ===")
        template_logo_url = None
        
        if zara_brand.logo:
            if hasattr(zara_brand.logo, 'url'):
                template_logo_url = zara_brand.logo.url
                print(f"Template will use brand.logo.url: {template_logo_url}")
            else:
                template_logo_url = str(zara_brand.logo)
                print(f"Template will use str(brand.logo): {template_logo_url}")
        else:
            template_logo_url = "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg"
            print(f"Template will use fallback: {template_logo_url}")
        
        # Generate the exact HTML template would produce
        html_output = f'<img src="{template_logo_url}" alt="Zara">'
        print(f"HTML output: {html_output}")
        
        # Test with a working brand for comparison
        print("\n=== COMPARING WITH NIKE ===")
        try:
            nike_brand = Brand.objects.get(name='Nike')
            if nike_brand.logo:
                if hasattr(nike_brand.logo, 'url'):
                    nike_url = nike_brand.logo.url
                    print(f"Nike logo URL: {nike_url}")
                    nike_html = f'<img src="{nike_url}" alt="Nike">'
                    print(f"Nike HTML: {nike_html}")
        except:
            pass
        
    except Brand.DoesNotExist:
        print("Zara brand not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_template_logic()
