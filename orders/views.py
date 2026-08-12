from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from .models import Order, OrderItem, Payment
from store.models import Product
from accounts.models import CartItem, CustomerProfile
import uuid

@login_required
def checkout_view(request):
    try:
        customer_profile = request.user.customer_profile
        cart_items = CartItem.objects.filter(customer_profile=customer_profile)
        
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
        
        subtotal = sum(item.product.get_final_price() * item.quantity for item in cart_items)
        shipping_charge = Decimal('50.00') if subtotal < 500 else Decimal('0.00')
        tax_amount = subtotal * Decimal('0.18')  # 18% GST
        total_amount = subtotal + shipping_charge + tax_amount
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_charge': shipping_charge,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
        }
        return render(request, 'checkout.html', context)
    
    except CustomerProfile.DoesNotExist:
        messages.error(request, 'Customer profile not found!')
        return redirect('home')

@login_required
def place_order(request):
    if request.method == 'POST':
        try:
            customer_profile = request.user.customer_profile
            cart_items = CartItem.objects.filter(customer_profile=customer_profile)
            
            if not cart_items.exists():
                return JsonResponse({'success': False, 'message': 'Cart is empty'})
            
            # Calculate totals
            subtotal = sum(item.product.get_final_price() * item.quantity for item in cart_items)
            shipping_charge = Decimal('50.00') if subtotal < 500 else Decimal('0.00')
            tax_amount = subtotal * Decimal('0.18')
            total_amount = subtotal + shipping_charge + tax_amount
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                shipping_name=f"{request.POST.get('first_name', '')} {request.POST.get('last_name', '')}".strip(),
                shipping_phone=request.POST.get('phone'),
                shipping_address=request.POST.get('address'),
                shipping_city=request.POST.get('city'),
                shipping_state=request.POST.get('state'),
                shipping_pincode=request.POST.get('postal_code'),
                subtotal=subtotal,
                shipping_charge=shipping_charge,
                tax_amount=tax_amount,
                total_amount=total_amount,
                payment_method=request.POST.get('payment_method'),
                status='pending'
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.get_final_price(),
                    total=cart_item.product.get_final_price() * cart_item.quantity
                )
            
            # Clear cart
            cart_items.delete()
            
            # Create payment record
            Payment.objects.create(
                order=order,
                payment_id=f"PAY{uuid.uuid4().hex[:12].upper()}",
                amount=total_amount,
                status='pending',
                payment_method=request.POST.get('payment_method')
            )
            
            return JsonResponse({'success': True, 'order_number': order.order_number})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'order_list.html', context)

@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'order_detail.html', context)

@login_required
def payment_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'payment.html', context)
