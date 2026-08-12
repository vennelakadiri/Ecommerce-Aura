from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product, Category
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
