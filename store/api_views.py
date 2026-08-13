import os

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer

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


class DeployStatusAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db = settings.DATABASES['default']
        return Response({
            'database_engine': db.get('ENGINE', ''),
            'database_name': str(db.get('NAME', '')),
            'database_url_configured': bool(os.environ.get('DATABASE_URL')),
            'render': bool(os.environ.get('RENDER')),
            'products_total': Product.objects.count(),
            'products_active': Product.objects.filter(is_active=True).count(),
            'categories': Category.objects.count(),
            'brands': Brand.objects.count(),
        })
