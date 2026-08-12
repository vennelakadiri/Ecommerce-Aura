#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

# Read the current store/views.py file
with open('store/views.py', 'r') as f:
    content = f.read()

# Fix the customer profile handling in add_to_cart function
content = content.replace(
    '''except CustomerProfile.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer profile not found'})''',
    '''except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
        except CustomerProfile.DoesNotExist:
            # Create customer profile if it doesn't exist
            from accounts.models import CustomerProfile
            customer_profile, created = CustomerProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'loyalty_points': 0,
                    'default_payment_method': 'credit_card'
                }
            )
            return JsonResponse({'success': False, 'message': 'Customer profile created and item added to cart!'})'''
)

# Write the fixed content back to the file
with open('store/views.py', 'w') as f:
    f.write(content)

print("✅ Fixed customer profile handling in add_to_cart function")
