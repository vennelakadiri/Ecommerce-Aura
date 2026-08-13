from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import User, CustomerProfile, AdminProfile, DeliveryBoyProfile

ALLOWED_DEMO_CREDENTIALS = {
    'customer@aura.com': 'customer123',
    'customer': 'customer123',
    'admin@aura.com': 'admin123',
    'admin': 'admin123',
    'delivery@aura.com': 'delivery123',
    'delivery': 'delivery123',
}


def _get_user_profile(user):
    if user.role == 'customer':
        profile, _ = CustomerProfile.objects.get_or_create(
            user=user,
            defaults={
                'loyalty_points': 0,
                'default_payment_method': 'credit_card',
            },
        )
        return profile
    if user.role == 'delivery_boy':
        profile, _ = DeliveryBoyProfile.objects.get_or_create(
            user=user,
            defaults={
                'vehicle_type': 'bike',
                'vehicle_number': 'N/A',
                'license_number': 'N/A',
            },
        )
        return profile
    if user.role == 'admin':
        profile, _ = AdminProfile.objects.get_or_create(
            user=user,
            defaults={'department': 'Management'},
        )
        return profile
    return None


@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            if username in ALLOWED_DEMO_CREDENTIALS and ALLOWED_DEMO_CREDENTIALS[username] == password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.role == 'admin':
                        if not user.is_staff or not user.is_superuser:
                            user.is_staff = True
                            user.is_superuser = True
                            user.save(update_fields=['is_staff', 'is_superuser'])
                        AdminProfile.objects.get_or_create(
                            user=user,
                            defaults={'department': 'Management'},
                        )

                    login(request, user)
                    
                    # Redirect based on user role
                    if user.role == 'admin':
                        redirect_url = '/accounts/dashboard/'
                    elif user.role == 'delivery_boy':
                        redirect_url = '/delivery/home/'
                    else:
                        redirect_url = '/home/'
                    
                    return JsonResponse({
                        'access': 'mock-token',
                        'redirect_url': redirect_url,
                        'role': user.role
                    })
            
            # If credentials are not one of the allowed 3 demo accounts
            return JsonResponse({'detail': 'Invalid credentials only demo credientals are allowed'}, status=400)
                
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
def signup_view(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            password = data.get('password', '').strip()
            first_name = data.get('first_name', '').strip()
            
            if not email or not password:
                return JsonResponse({'detail': 'Email and Password are required'}, status=400)
            
            if User.objects.filter(Q(email=email) | Q(username=email)).exists():
                return JsonResponse({'detail': 'An account with this email already exists'}, status=400)
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                phone=phone,
                role='customer'
            )
            
            CustomerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'loyalty_points': 0,
                    'default_payment_method': 'credit_card'
                }
            )
            
            # Return redirect to login page after signup
            return JsonResponse({
                'message': 'Account created successfully',
                'redirect_url': '/accounts/login/'
            })
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
def forgot_password_view(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            identity = data.get('identity', '').strip()
            new_password = data.get('new_password', '').strip()
            
            if not identity or not new_password:
                return JsonResponse({'detail': 'Email/Phone and New Password are required'}, status=400)
            
            user = User.objects.filter(Q(email=identity) | Q(username=identity) | Q(phone=identity)).first()
            if not user:
                return JsonResponse({'detail': 'No account found with provided Email/Phone'}, status=404)
            
            user.set_password(new_password)
            user.save()
            
            return JsonResponse({'message': 'Password reset successful!'})
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=500)

def logout_view(request):
    logout(request)
    return redirect('login')

def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    return render(request, 'admin_dashboard.html', {'user': request.user})

@ensure_csrf_cookie
def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'user': request.user,
    }

    profile = _get_user_profile(request.user)
    if profile is not None:
        context['profile'] = profile

    return render(request, 'profile.html', context)

def subscription_management(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    return render(request, 'admin_subscription.html', {'user': request.user})

def dashboard_analytics(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    return render(request, 'admin_analytics.html', {'user': request.user})

def notifications_management(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    return render(request, 'admin_notifications.html', {'user': request.user})

def reports_management(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    return render(request, 'admin_reports.html', {'user': request.user})

def advertisements_management(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('login')
    
    return render(request, 'admin_advertisements.html', {'user': request.user})
