from django.contrib import admin
from .models import Category, SubCategory, Brand, Product, ProductImage, ProductSize, ProductColor, Banner, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 3

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'discount_price', 'stock_quantity', 'is_active', 'is_featured')
    list_filter = ('category', 'brand', 'gender', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSizeInline, ProductColorInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'sku')
        }),
        ('Classification', {
            'fields': ('category', 'subcategory', 'brand', 'gender')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    ordering = ('order', '-created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user_name', 'rating', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('product__name', 'user_name', 'title')
    readonly_fields = ('created_at',)
