from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile, CartItem, DeliveryBoyProfile, AdminProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'phone', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone', 'address', 'profile_image')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone', 'address')}),
    )

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'loyalty_points', 'default_payment_method')
    list_filter = ('loyalty_points', 'default_payment_method')
    search_fields = ('user__username', 'user__email')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer_profile', 'product', 'quantity', 'added_at')
    list_filter = ('added_at', 'quantity')
    search_fields = ('customer_profile__user__username', 'product__name')

@admin.register(DeliveryBoyProfile)
class DeliveryBoyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle_type', 'vehicle_number', 'is_available', 'rating', 'total_deliveries', 'earnings')
    list_filter = ('vehicle_type', 'is_available', 'rating')
    search_fields = ('user__username', 'vehicle_number')

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    list_filter = ('department',)
    search_fields = ('user__username', 'department')
