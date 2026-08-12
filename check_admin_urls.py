#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from django.urls import get_resolver
from django.conf import settings

def check_admin_urls():
    """Check for Django admin URLs and login page"""
    
    print("=== CHECKING DJANGO ADMIN URLS ===")
    print()
    
    try:
        resolver = get_resolver()
        
        print("Available URL patterns:")
        for pattern in resolver.url_patterns:
            print(f"  {pattern}")
        
        print("\n=== ADMIN URL CHECK ===")
        if hasattr(settings, 'ADMIN_URL'):
            admin_url = settings.ADMIN_URL
            print(f"ADMIN_URL setting: {admin_url}")
        else:
            admin_url = '/admin/'
            print(f"Default ADMIN_URL: {admin_url}")
        
        print(f"Expected admin URL: http://127.0.0.1:9000{admin_url}")
        
        # Check if admin is included in urls
        print("\n=== URL PATTERN ANALYSIS ===")
        try:
            with open('aura/urls.py', 'r') as f:
                content = f.read()
                if 'admin/' in content:
                    print("✅ Admin URLs are configured in urls.py")
                else:
                    print("❌ Admin URLs NOT found in urls.py")
        except FileNotFoundError:
            print("❌ urls.py file not found")
        
        print("\n=== LOGIN INFORMATION ===")
        print("Django Admin Login:")
        print(f"  URL: http://127.0.0.1:9000{admin_url}")
        print("  Default credentials:")
        print("    - Username: admin (check your settings)")
        print("    - Password: (check your settings or createsuperuser)")
        print("  Note: If you haven't created a superuser, run:")
        print("    python manage.py createsuperuser")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_admin_urls()
