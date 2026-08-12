#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product
from accounts.models import CustomerProfile, User
from django.test import Client
from django.urls import reverse

print("=== Wishlist Debug ===")

# Check if products exist
print("\n1. Checking products...")
products = Product.objects.filter(is_active=True)[:5]
for product in products:
    print(f"  - {product.name} (ID: {product.id})")

if not products:
    print("  No active products found!")
    exit()

# Check if users exist
print("\n2. Checking users...")
users = User.objects.all()
for user in users:
    print(f"  - {user.username} (ID: {user.id})")

if not users:
    print("  No users found!")
    exit()

# Create test user if needed
test_user = None
try:
    test_user = User.objects.get(username='testuser')
except User.DoesNotExist:
    test_user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print(f"  Created test user: {test_user.username}")

# Ensure customer profile exists
try:
    profile = CustomerProfile.objects.get(user=test_user)
    print(f"  Customer profile exists for {test_user.username}")
except CustomerProfile.DoesNotExist:
    profile = CustomerProfile.objects.create(user=test_user)
    print(f"  Created customer profile for {test_user.username}")

# Test wishlist functionality
print("\n3. Testing wishlist functionality...")
product = products[0]
print(f"  Testing with product: {product.name} (ID: {product.id})")

# Check if product is in wishlist
if product in profile.wishlist.all():
    print(f"  Product {product.name} is already in wishlist")
else:
    print(f"  Product {product.name} is NOT in wishlist")

# Test adding to wishlist
try:
    profile.wishlist.add(product)
    profile.save()
    print(f"  Successfully added {product.name} to wishlist")
except Exception as e:
    print(f"  Error adding to wishlist: {e}")

# Test removing from wishlist
try:
    profile.wishlist.remove(product)
    profile.save()
    print(f"  Successfully removed {product.name} from wishlist")
except Exception as e:
    print(f"  Error removing from wishlist: {e}")

# Test the view directly
print("\n4. Testing the toggle_wishlist view...")
client = Client()

# Login the test user
client.login(username='testuser', password='testpass123')
print(f"  Logged in as testuser")

# Test the view
try:
    response = client.post('/store/toggle-wishlist/', {'product_id': product.id})
    print(f"  Response status: {response.status_code}")
    print(f"  Response content: {response.content.decode()}")
except Exception as e:
    print(f"  Error testing view: {e}")

print("\n=== Debug Complete ===")
