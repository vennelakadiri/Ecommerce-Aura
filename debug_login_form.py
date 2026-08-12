#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

def debug_login_form():
    """Debug the login form for any remaining issues"""
    
    print("=== DEBUGGING LOGIN FORM ===")
    print()
    
    try:
        # Read the current login.html
        with open('templates/login.html', 'r') as f:
            content = f.read()
        
        print("Checking login form structure:")
        
        # Check for common issues
        issues = []
        
        # Check if form has proper action
        if 'action="/accounts/login/"' not in content:
            issues.append("❌ Missing form action")
        else:
            print("✅ Form action present")
        
        # Check if CSRF token is properly placed
        if '{% csrf_token %}' in content:
            print("✅ CSRF token tag present")
        else:
            issues.append("❌ CSRF token tag missing")
        
        # Check if form method is POST
        if 'method="post"' not in content.lower():
            issues.append("❌ Missing method='POST'")
        else:
            print("✅ Form method is POST")
        
        # Check if input fields have proper names
        if 'name="phone"' in content:
            print("✅ Phone input has name attribute")
        else:
            issues.append("❌ Phone input missing name attribute")
        
        if 'name="password"' in content:
            print("✅ Password input has name attribute")
        else:
            issues.append("❌ Password input missing name attribute")
        
        # Check for JavaScript validation
        if 'validateForm()' in content:
            print("✅ JavaScript validation function present")
        else:
            issues.append("❌ JavaScript validation function missing")
        
        # Check for submit button
        if 'type="submit"' in content:
            print("✅ Submit button present")
        else:
            issues.append("❌ Submit button missing")
        
        print(f"\n=== ISSUES FOUND ===")
        if issues:
            for issue in issues:
                print(issue)
        else:
            print("✅ No obvious issues found in form structure")
        
        print("\n=== RECOMMENDATIONS ===")
        print("If 405 error persists:")
        print("1. Restart Django development server")
        print("2. Clear browser cache (Ctrl+F5)")
        print("3. Check browser developer tools (F12)")
        print("4. Try different browser")
        print("5. Verify server is running on correct port")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_login_form()
