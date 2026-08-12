from django.contrib import admin
from .models import Order, OrderItem, Payment, OrderStatusHistory

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total')

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'comment', 'updated_by', 'timestamp')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'payment_method')
        }),
        ('Shipping Information', {
            'fields': ('shipping_name', 'shipping_phone', 'shipping_address', 
                      'shipping_city', 'shipping_state', 'shipping_pincode', 'shipping_country')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'shipping_charge', 'tax_amount', 
                      'discount_amount', 'total_amount')
        }),
        ('Delivery Information', {
            'fields': ('delivery_boy', 'estimated_delivery', 'actual_delivery', 'tracking_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total')
    list_filter = ('order', 'product')
    search_fields = ('order__order_number', 'product__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_id', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'order__order_number', 'transaction_id')
    readonly_fields = ('payment_id', 'created_at', 'updated_at')

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'updated_by', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('order__order_number', 'updated_by__username')
    readonly_fields = ('timestamp',)
