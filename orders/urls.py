from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_list_view, name='order_list'),
    path('order/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('payment/<str:order_number>/', views.payment_view, name='payment'),
]
