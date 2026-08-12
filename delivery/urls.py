from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.delivery_home_view, name='delivery_home'),
    path('orders/', views.orders_list_view, name='delivery_orders'),
    path('order/<str:order_number>/', views.order_detail_view, name='delivery_order_detail'),
    path('update-status/<str:order_number>/', views.update_order_status, name='update_order_status'),
    path('earnings/', views.earnings_view, name='delivery_earnings'),
    path('map/<str:order_number>/', views.map_view, name='delivery_map'),
    path('profile/', views.delivery_profile_view, name='delivery_profile'),
]
