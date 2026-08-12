import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')

import django

django.setup()

from accounts.models import User, CustomerProfile, AdminProfile, DeliveryBoyProfile


def create_user(username, email, password, role, first_name):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'role': role,
            'first_name': first_name,
        }
    )

    user.email = email
    user.role = role
    user.first_name = first_name
    user.set_password(password)

    if role == 'admin':
        user.is_staff = True
        user.is_superuser = True
    else:
        user.is_staff = False
        user.is_superuser = False

    user.save()

    return user


customer = create_user(
    'customer@aura.com',
    'customer@aura.com',
    'customer123',
    'customer',
    'Customer'
)

CustomerProfile.objects.get_or_create(
    user=customer,
    defaults={
        'loyalty_points': 0,
        'default_payment_method': 'credit_card',
    }
)


admin = create_user(
    'admin@aura.com',
    'admin@aura.com',
    'admin123',
    'admin',
    'Admin'
)

AdminProfile.objects.get_or_create(
    user=admin,
    defaults={
        'department': 'Management',
        'permissions': {},
    }
)


delivery = create_user(
    'delivery@aura.com',
    'delivery@aura.com',
    'delivery123',
    'delivery_boy',
    'Delivery'
)

DeliveryBoyProfile.objects.get_or_create(
    user=delivery,
    defaults={
        'vehicle_type': 'bike',
        'vehicle_number': 'AURA-001',
        'license_number': 'AURA-LICENSE-001',
        'is_available': True,
    }
)

print('Demo users created successfully.')
