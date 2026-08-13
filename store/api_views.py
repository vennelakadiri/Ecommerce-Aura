import os

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]


class DeployStatusAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db = settings.DATABASES['default']
        products_active = Product.objects.filter(is_active=True).count()
        categories = Category.objects.count()
        brands = Brand.objects.count()
        return Response({
            'database_engine': db.get('ENGINE', ''),
            'database_name': str(db.get('NAME', '')),
            'database_url_configured': bool(os.environ.get('DATABASE_URL')),
            'render': bool(os.environ.get('RENDER')),
            'catalog_ready': products_active > 0 and categories > 0 and brands > 0,
            'products_total': Product.objects.count(),
            'products_active': products_active,
            'categories': categories,
            'brands': brands,
        })
