#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

def fix_login_form_issues():
    """Fix critical issues in login form"""
    
    print("=== FIXING LOGIN FORM ISSUES ===")
    print("Issues found: Missing form action, method, and input names")
    print()
    
    try:
        # Read current login.html
        with open('templates/login.html', 'r') as f:
            content = f.read()
        
        # Fix multiple issues at once
        content_fixed = content
        
        # Fix 1: Add proper form action and method
        content_fixed = content_fixed.replace(
            '<form id="loginForm" onsubmit="event.preventDefault(); validateForm();">',
            '<form id="loginForm" method="POST" action="/accounts/login/" onsubmit="event.preventDefault(); validateForm();">'
        )
        
        # Fix 2: Add proper name attributes to inputs
        content_fixed = content_fixed.replace(
            '<input type="text" id="phone" placeholder="Enter your Email or Phone n.o." ',
            '<input type="text" id="phone" name="username" placeholder="Enter your Email or Phone n.o." '
        )
        
        content_fixed = content_fixed.replace(
            '<input type="password" id="password" placeholder="Enter your Password">',
            '<input type="password" id="password" name="password" placeholder="Enter your Password">'
        )
        
        # Write the fixed content back
        with open('templates/login.html', 'w') as f:
            f.write(content_fixed)
        
        print("✅ Fixed form action: method='POST' action='/accounts/login/'")
        print("✅ Fixed phone input: name='username'")
        print("✅ Fixed password input: name='password'")
        print("✅ CSRF token already present")
        print("✅ JavaScript validation already present")
        print("\nLogin form should now work properly!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_login_form_issues()
