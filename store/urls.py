from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
]
