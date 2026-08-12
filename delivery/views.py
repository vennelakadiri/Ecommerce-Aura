from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from orders.models import Order, OrderStatusHistory
from accounts.models import DeliveryBoyProfile
from django.db.models import Count, Sum, Avg
from datetime import datetime, timedelta

@login_required
def delivery_home_view(request):
    if request.user.role != 'delivery_boy':
        return redirect('login')
    
    try:
        delivery_profile = request.user.delivery_profile
        
        # Get today's orders
        today = datetime.now().date()
        today_orders = Order.objects.filter(
            delivery_boy=request.user,
            created_at__date=today
        ).count()
        
        # Get pending orders assigned to this delivery boy
        pending_orders = Order.objects.filter(
            delivery_boy=request.user,
            status__in=['confirmed', 'processing', 'shipped', 'out_for_delivery']
        ).order_by('created_at')
        
        # Get completed orders
        completed_orders = Order.objects.filter(
            delivery_boy=request.user,
            status='delivered'
        ).count()
        
        # Get recent deliveries
        recent_deliveries = Order.objects.filter(
            delivery_boy=request.user,
            status='delivered'
        ).order_by('-actual_delivery')[:5]
        
        context = {
            'delivery_profile': delivery_profile,
            'today_orders': today_orders,
            'pending_orders': pending_orders[:5],
            'completed_orders': completed_orders,
            'recent_deliveries': recent_deliveries,
            'total_earnings': delivery_profile.earnings,
        }
        return render(request, 'delivery/home.html', context)
    
    except DeliveryBoyProfile.DoesNotExist:
        messages.error(request, 'Delivery profile not found!')
        return redirect('login')

@login_required
def orders_list_view(request):
    if request.user.role != 'delivery_boy':
        return redirect('login')
    
    status_filter = request.GET.get('status', 'all')
    
    orders = Order.objects.filter(delivery_boy=request.user)
    
    if status_filter != 'all':
        orders = orders.filter(status=status_filter)
    
    orders = orders.order_by('-created_at')
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
    }
    return render(request, 'delivery/orders_list.html', context)

@login_required
def order_detail_view(request, order_number):
    if request.user.role != 'delivery_boy':
        return redirect('login')
    
    order = get_object_or_404(Order, order_number=order_number, delivery_boy=request.user)
    status_history = OrderStatusHistory.objects.filter(order=order).order_by('-timestamp')
    
    context = {
        'order': order,
        'status_history': status_history,
    }
    return render(request, 'delivery/order_detail.html', context)

@login_required
def update_order_status(request, order_number):
    if request.user.role != 'delivery_boy':
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
    
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, order_number=order_number, delivery_boy=request.user)
            new_status = request.POST.get('status')
            comment = request.POST.get('comment', '')
            
            # Validate status transition
            valid_transitions = {
                'confirmed': ['processing'],
                'processing': ['shipped'],
                'shipped': ['out_for_delivery'],
                'out_for_delivery': ['delivered'],
            }
            
            if new_status in valid_transitions.get(order.status, []):
                order.status = new_status
                
                if new_status == 'delivered':
                    order.actual_delivery = datetime.now().date()
                    # Update delivery boy stats
                    delivery_profile = request.user.delivery_profile
                    delivery_profile.total_deliveries += 1
                    delivery_profile.earnings += order.total_amount * 0.05  # 5% commission
                    delivery_profile.save()
                
                order.save()
                
                # Add to status history
                OrderStatusHistory.objects.create(
                    order=order,
                    status=new_status,
                    comment=comment,
                    updated_by=request.user
                )
                
                return JsonResponse({'success': True, 'message': f'Status updated to {new_status}'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid status transition'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def earnings_view(request):
    if request.user.role != 'delivery_boy':
        return redirect('login')
    
    try:
        delivery_profile = request.user.delivery_profile
        
        # Get earnings data
        total_earnings = delivery_profile.earnings
        total_deliveries = delivery_profile.total_deliveries
        
        # Get monthly earnings
        current_month = datetime.now().replace(day=1)
        monthly_orders = Order.objects.filter(
            delivery_boy=request.user,
            status='delivered',
            actual_delivery__gte=current_month
        )
        monthly_earnings = sum(order.total_amount * 0.05 for order in monthly_orders)
        
        # Get recent earnings
        recent_earnings = Order.objects.filter(
            delivery_boy=request.user,
            status='delivered'
        ).order_by('-actual_delivery')[:10]
        
        context = {
            'delivery_profile': delivery_profile,
            'total_earnings': total_earnings,
            'total_deliveries': total_deliveries,
            'monthly_earnings': monthly_earnings,
            'recent_earnings': recent_earnings,
        }
        return render(request, 'delivery/earnings.html', context)
    
    except DeliveryBoyProfile.DoesNotExist:
        messages.error(request, 'Delivery profile not found!')
        return redirect('login')

@login_required
def map_view(request, order_number):
    if request.user.role != 'delivery_boy':
        return redirect('login')
    
    order = get_object_or_404(Order, order_number=order_number, delivery_boy=request.user)
    
    context = {
        'order': order,
        'delivery_address': f"{order.shipping_address}, {order.shipping_city}, {order.shipping_state} - {order.shipping_pincode}",
    }
    return render(request, 'delivery/map.html', context)

@login_required
def delivery_profile_view(request):
    if request.user.role != 'delivery_boy':
        return redirect('login')
    
    try:
        delivery_profile = request.user.delivery_profile
        
        # Get delivery statistics
        total_deliveries = delivery_profile.total_deliveries
        total_earnings = delivery_profile.earnings
        rating = delivery_profile.rating
        
        # Get recent deliveries
        recent_deliveries = Order.objects.filter(
            delivery_boy=request.user,
            status='delivered'
        ).order_by('-actual_delivery')[:5]
        
        context = {
            'delivery_profile': delivery_profile,
            'total_deliveries': total_deliveries,
            'total_earnings': total_earnings,
            'rating': rating,
            'recent_deliveries': recent_deliveries,
        }
        return render(request, 'delivery/profile.html', context)
    
    except DeliveryBoyProfile.DoesNotExist:
        messages.error(request, 'Delivery profile not found!')
        return redirect('login')
