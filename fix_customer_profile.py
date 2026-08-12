#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import CustomerProfile

print("=== Creating Customer Profiles for Existing Users ===")

# Get all users without customer profiles using the correct User model
try:
    users_without_profile = User.objects.filter(role='customer').exclude(customerprofile__isnull=False)
except AttributeError:
    print("Using accounts.User model instead of auth.User")
    users_without_profile = User.objects.filter(role='customer').exclude(customerprofile__isnull=False)

for user in users_without_profile:
    # Create customer profile for existing users
    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=user,
        defaults={
            'loyalty_points': 0,
            'default_payment_method': 'credit_card'
        }
    )
    
    if created:
        print(f"Created profile for: {user.username}")
    else:
        print(f"Profile already exists for: {user.username}")

print("=== Customer Profiles Created ===")
