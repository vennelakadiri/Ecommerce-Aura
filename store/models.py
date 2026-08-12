from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    image = CloudinaryField('image', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "SubCategories"
        ordering = ['name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
        ('kids', 'Kids'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_discount_percentage(self):
        if self.discount_price:
            return int((self.price - self.discount_price) / self.price * 100)
        return 0

    def get_final_price(self):
        return self.discount_price if self.discount_price else self.price

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.product.name} - Image"

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10)  # S, M, L, XL, 2XL, etc.
    stock_quantity = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['product', 'size']

    def __str__(self):
        return f"{self.product.name} - Size {self.size}"

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=7, help_text="Hex color code")
    stock_quantity = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['product', 'color_name']

    def __str__(self):
        return f"{self.product.name} - {self.color_name}"

class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_url = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100)  # Store user name instead of foreign key
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=100)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} - {self.product.name} ({self.rating} stars)"
