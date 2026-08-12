#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

def fix_login_csrf():
    """Fix CSRF token issue in login form"""
    
    print("=== FIXING LOGIN CSRF ISSUE ===")
    print("Adding CSRF token to login form")
    print()
    
    try:
        # Read current login.html
        with open('templates/login.html', 'r') as f:
            content = f.read()
        
        print("Current form tag check:")
        if '<form id="loginForm"' in content:
            print("✅ Form has id='loginForm'")
        else:
            print("❌ Form missing id='loginForm'")
        
        if '{% csrf_token %}' in content:
            print("✅ CSRF token template tag present")
        else:
            print("❌ CSRF token template tag missing")
        
        # Fix the form by adding CSRF token
        if '<form id="loginForm"' in content and '{% csrf_token %}' not in content:
            # Add CSRF token after the opening form tag
            content_fixed = content.replace(
                '<form id="loginForm" onsubmit="event.preventDefault(); validateForm();">',
                '<form id="loginForm" onsubmit="event.preventDefault(); validateForm();">{% csrf_token %}'
            )
            
            # Write the fixed content back
            with open('templates/login.html', 'w') as f:
                f.write(content_fixed)
                print("✅ Added CSRF token to login form")
                print("Login form should now work properly")
        else:
            print("CSRF token already present or form structure different")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_login_csrf()
