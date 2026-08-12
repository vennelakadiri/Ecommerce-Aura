from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

import json
from .models import Product, Category, SubCategory, Brand, Banner, ProductImage, Review
from accounts.models import CustomerProfile, CartItem

@ensure_csrf_cookie
def home_view(request):
    banners = Banner.objects.filter(is_active=True)[:4]
    # Get categories in specific order
    category_order = ['men', 'women', 'accessories', 'new-arrivals']
    featured_categories = []
    for slug in category_order:
        try:
            category = Category.objects.get(slug=slug, is_active=True)
            featured_categories.append(category)
        except Category.DoesNotExist:
            pass
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    
    # Get specific brands in order
    brand_order = ['levis', 'puma', 'hm', 'zara', 'nike', 'tanishq', 'biba', 'jack-jones', 'uspa', 'tommy', 'only', 'allen-solly', 'vero-moda', 'steve-madden', 'skechers', 'van-heusen']
    brands = []
    for slug in brand_order:
        try:
            brand = Brand.objects.get(slug=slug, is_active=True)
            brands.append(brand)
        except Brand.DoesNotExist:
            pass
    brand_groups = [brands[i:i+4] for i in range(0, len(brands), 4)]
    
    categories = Category.objects.filter(is_active=True).prefetch_related('subcategories')
    
    context = {
        'banners': banners,
        'featured_categories': featured_categories,
        'products': products,
        'brand_groups': brand_groups,
        'categories': categories,
    }
    return render(request, 'home.html', context)

@ensure_csrf_cookie
def products_view(request):
    category_slug = request.GET.get('category', '').strip()
    subcategory_slug = request.GET.get('subcategory', '').strip()
    brand_slug = request.GET.get('brand', '').strip()
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'newest').strip()
    
    qs = Product.objects.filter(is_active=True).select_related('brand', 'category').prefetch_related('images')
    
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if subcategory_slug:
        qs = qs.filter(subcategory__slug=subcategory_slug)
    if brand_slug:
        qs = qs.filter(brand__slug=brand_slug)
    
    if search_query:
        qs = qs.filter(name__istartswith=search_query).distinct()
    
    if sort_by == 'price_low':
        qs = qs.order_by('price')
    elif sort_by == 'price_high':
        qs = qs.order_by('-price')
    elif sort_by == 'name':
        qs = qs.order_by('name')
    else:
        qs = qs.order_by('-created_at')
    
    products = list(qs)
    
    context = {
        'products': products,
        'products_count': len(products),
        'categories': Category.objects.filter(is_active=True),
        'brands': Brand.objects.filter(is_active=True),
        'search_query': search_query,
        'selected_category': category_slug,
        'selected_subcategory': subcategory_slug,
        'selected_brand': brand_slug,
        'sort_by': sort_by,
    }
    return render(request, 'products.html', context)

@ensure_csrf_cookie
def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    reviews = product.reviews.all().order_by('-created_at')
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    context = {
        'product': product,
        'images': images,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': reviews.count(),
    }
    return render(request, 'product_detail.html', context)

@ensure_csrf_cookie
@login_required
def wishlist_view(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'loyalty_points': 0,
            'default_payment_method': 'credit_card'
        }
    )
    wishlist_products = customer_profile.wishlist.filter(is_active=True)
    
    orphaned_ids = list(customer_profile.wishlist.filter(is_active=False).values_list('id', flat=True))
    if orphaned_ids:
        customer_profile.wishlist.remove(*orphaned_ids)
    
    context = {
        'wishlist_products': wishlist_products,
    }
    return render(request, 'wishlist.html', context)

@ensure_csrf_cookie
@login_required
def cart_view(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'loyalty_points': 0,
            'default_payment_method': 'credit_card'
        }
    )
    cart_items = CartItem.objects.filter(customer_profile=customer_profile)
    
    total_price = 0
    for item in cart_items:
        total_price += item.product.get_final_price() * item.quantity
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def toggle_wishlist(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please login to use wishlist'})
        
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        customer_profile, created = CustomerProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'loyalty_points': 0,
                'default_payment_method': 'credit_card'
            }
        )
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            if product in customer_profile.wishlist.all():
                customer_profile.wishlist.remove(product)
                return JsonResponse({'success': True, 'is_in_wishlist': False, 'message': 'Removed from wishlist'})
            else:
                customer_profile.wishlist.add(product)
                return JsonResponse({'success': True, 'is_in_wishlist': True, 'message': 'Added to wishlist'})
                
        except Product.DoesNotExist:
            try:
                product_any = Product.objects.filter(id=product_id).first()
                if product_any:
                    customer_profile.wishlist.remove(product_any)
            except Exception:
                pass
            return JsonResponse({'success': True, 'is_in_wishlist': False, 'message': 'Removed from wishlist'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            customer_profile, created = CustomerProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'loyalty_points': 0,
                    'default_payment_method': 'credit_card'
                }
            )
            cart_item = CartItem.objects.get(id=item_id, customer_profile=customer_profile)
            new_quantity = int(request.POST.get('quantity', 1))
            
            if 1 <= new_quantity <= 10:
                cart_item.quantity = new_quantity
                cart_item.save()
                return JsonResponse({'success': True, 'message': 'Quantity updated'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid quantity'})
                
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            customer_profile, created = CustomerProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'loyalty_points': 0,
                    'default_payment_method': 'credit_card'
                }
            )
            cart_item = CartItem.objects.get(id=item_id, customer_profile=customer_profile)
            cart_item.delete()
            return JsonResponse({'success': True, 'message': 'Item removed'})
            
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            if request.user.is_authenticated:
                # Get or create customer profile
                customer_profile, created = CustomerProfile.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'loyalty_points': 0,
                        'default_payment_method': 'credit_card'
                    }
                )
                
                cart_item, created = CartItem.objects.get_or_create(
                    customer_profile=customer_profile,
                    product=product,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                
                return JsonResponse({'success': True, 'message': 'Product added to cart!'})
            else:
                return JsonResponse({'success': False, 'message': 'Please login to add items to cart'})
                
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            if request.user.is_authenticated:
                customer_profile, created = CustomerProfile.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'loyalty_points': 0,
                        'default_payment_method': 'credit_card'
                    }
                )
                
                if product in customer_profile.wishlist.all():
                    customer_profile.wishlist.remove(product)
                    return JsonResponse({'success': True, 'is_in_wishlist': False, 'message': 'Product removed from wishlist!'})
                else:
                    customer_profile.wishlist.add(product)
                    return JsonResponse({'success': True, 'is_in_wishlist': True, 'message': 'Product added to wishlist!'})
            else:
                return JsonResponse({'success': False, 'message': 'Please login to add items to wishlist!'})
                
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
