#!/usr/bin/env python
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def test_zara_logo_accessibility():
    """Test if Zara logo file is accessible via web server"""
    
    print("=== TESTING ZARA LOGO ACCESSIBILITY ===")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara brand logo: {zara_brand.logo}")
        
        if hasattr(zara_brand.logo, 'url'):
            logo_url = zara_brand.logo.url
            print(f"Logo URL: {logo_url}")
            
            # Test local file existence
            if hasattr(zara_brand.logo, 'path'):
                file_path = zara_brand.logo.path
                print(f"File path: {file_path}")
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"File exists: YES ({file_size} bytes)")
                else:
                    print(f"File exists: NO")
            
            # Test web accessibility (assuming server is running on port 9000)
            web_url = f"http://127.0.0.1:9000{logo_url}"
            print(f"Testing web URL: {web_url}")
            
            try:
                response = requests.get(web_url, timeout=5)
                print(f"HTTP Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
                    print(f"Content-Length: {response.headers.get('content-length', 'Unknown')}")
                    print("Web accessibility: GOOD")
                else:
                    print(f"Web accessibility: FAILED (Status {response.status_code})")
            except requests.RequestException as e:
                print(f"Web accessibility: FAILED ({str(e)})")
                print("Server might not be running or media files not served")
        
        # Compare with a working brand logo
        print("\n=== COMPARING WITH WORKING NIKE LOGO ===")
        try:
            nike_brand = Brand.objects.get(name='Nike')
            print(f"Nike logo: {nike_brand.logo}")
            if hasattr(nike_brand.logo, 'url'):
                nike_url = nike_brand.logo.url
                print(f"Nike URL: {nike_url}")
                
                # Test Nike web accessibility
                nike_web_url = f"http://127.0.0.1:9000{nike_url}"
                try:
                    response = requests.get(nike_web_url, timeout=5)
                    print(f"Nike HTTP Status: {response.status_code}")
                    if response.status_code == 200:
                        print("Nike web accessibility: GOOD")
                    else:
                        print(f"Nike web accessibility: FAILED (Status {response.status_code})")
                except requests.RequestException as e:
                    print(f"Nike web accessibility: FAILED ({str(e)})")
        except:
            print("Nike brand not found")
        
    except Brand.DoesNotExist:
        print("Zara brand not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_zara_logo_accessibility()
