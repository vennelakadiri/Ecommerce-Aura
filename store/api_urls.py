from django.urls import path
from . import api_views

urlpatterns = [
    path('products/', api_views.ProductListAPIView.as_view(), name='api_products'),
    path('products/<slug:slug>/', api_views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('categories/', api_views.CategoryListAPIView.as_view(), name='api_categories'),
    path('deploy-status/', api_views.DeployStatusAPIView.as_view(), name='api_deploy_status'),
]
