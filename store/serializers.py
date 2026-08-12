from rest_framework import serializers
from .models import Product, Category, SubCategory, Brand, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'subcategories']
    
    def get_subcategories(self, obj):
        subcategories = obj.subcategories.filter(is_active=True)
        return SubCategorySerializer(subcategories, many=True).data

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'description']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'description']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'category', 'brand', 'gender', 'price', 'discount_price',
            'final_price', 'discount_percentage', 'stock_quantity', 'sku',
            'is_active', 'is_featured', 'created_at', 'images'
        ]
    
    def get_final_price(self, obj):
        return obj.get_final_price()
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()
