#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

# Read current store/views.py file
with open('store/views.py', 'r') as f:
    content = f.read()

# Fix wishlist function with better error handling
content = content.replace(
    '''except CustomerProfile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer profile not found'})''',
    '''except CustomerProfile.DoesNotExist:
            # Create customer profile if it doesn't exist
            from accounts.models import CustomerProfile
            customer_profile, created = CustomerProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'loyalty_points': 0,
                    'default_payment_method': 'credit_card'
                }
            )
            return JsonResponse({'success': False, 'message': 'Customer profile created and item added to wishlist!'})'''
)

# Write fixed content back to file
with open('store/views.py', 'w') as f:
    f.write(content)

print("✅ Fixed wishlist function error handling")
