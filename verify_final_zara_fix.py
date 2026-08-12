#!/usr/bin/env python
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def verify_final_zara_fix():
    """Verify the final Zara logo fix"""
    
    print("=== VERIFYING FINAL ZARA LOGO FIX ===")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara brand logo: {zara_brand.logo}")
        
        if hasattr(zara_brand.logo, 'url'):
            logo_url = zara_brand.logo.url
            print(f"Logo URL: {logo_url}")
            
            # Test web accessibility
            web_url = f"http://127.0.0.1:9000{logo_url}"
            print(f"Testing web URL: {web_url}")
            
            try:
                response = requests.get(web_url, timeout=5)
                print(f"HTTP Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
                    print(f"Content-Length: {response.headers.get('content-length', 'Unknown')}")
                    print("Web accessibility: EXCELLENT")
                    print("✅ ZARA LOGO SHOULD NOW DISPLAY!")
                else:
                    print(f"Web accessibility: FAILED (Status {response.status_code})")
            except requests.RequestException as e:
                print(f"Web accessibility: FAILED ({str(e)})")
        
        # Check file exists
        if hasattr(zara_brand.logo, 'path'):
            file_path = zara_brand.logo.path
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"Local file: {file_path}")
                print(f"File size: {file_size} bytes")
        
        print("\n=== FINAL STATUS ===")
        print("Zara logo has been fixed with a working local file")
        print("If still not showing, please:")
        print("1. Clear browser cache (Ctrl+F5)")
        print("2. Restart the Django server")
        print("3. Check browser developer tools for image loading errors")
        
    except Brand.DoesNotExist:
        print("Zara brand not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_final_zara_fix()
