#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

def fix_login_405_error():
    """Fix the HTTP 405 error in login view"""
    
    print("=== FIXING LOGIN 405 ERROR ===")
    print("Issue: JsonResponse is missing closing part")
    print()
    
    # Read the current login view
    try:
        with open('accounts/views.py', 'r') as f:
            content = f.read()
            print("Current login view content:")
            print(content)
        
        print("\n=== ANALYSIS ===")
        # Check if JsonResponse is properly closed
        if "'access': 'mock-token'," in content:
            if "'redirect_url': redirect_url," in content:
                if "'role': user.role" in content:
                    if "})" in content:
                        print("✅ JsonResponse appears to be properly closed")
                    else:
                        print("❌ JsonResponse missing closing brace")
            else:
                print("❌ JsonResponse missing redirect_url or role")
        else:
            print("❌ JsonResponse structure issue found")
        
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    fix_login_405_error()
