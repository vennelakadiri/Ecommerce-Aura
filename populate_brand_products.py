#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, Brand, Category, SubCategory, ProductImage
import random

# Product data for each brand
brand_products = {
    'tanishq': [
        {'name': 'Gold Diamond Necklace', 'price': 89999, 'category': 'women', 'subcategory': 'fine-jewellery'},
        {'name': 'Ruby Earrings Set', 'price': 45999, 'category': 'women', 'subcategory': 'earrings-women'},
        {'name': 'Platinum Wedding Ring', 'price': 67999, 'category': 'women', 'subcategory': 'rings-women'},
        {'name': 'Emerald Bracelet', 'price': 54999, 'category': 'women', 'subcategory': 'bracelets-women'}
    ],
    'biba': [
        {'name': 'Embroidered Kurti', 'price': 1299, 'category': 'women', 'subcategory': 'kurtis-women'},
        {'name': 'Designer Salwar Suit', 'price': 2499, 'category': 'women', 'subcategory': 'kurtis-women'},
        {'name': 'Printed Palazzo Set', 'price': 1899, 'category': 'women', 'subcategory': 'skirts-women'},
        {'name': 'Anarkali Dress', 'price': 3299, 'category': 'women', 'subcategory': 'dresses'}
    ],
    'jack-jones': [
        {'name': 'Denim Jacket', 'price': 3499, 'category': 'men', 'subcategory': 'jackets'},
        {'name': 'Slim Fit Jeans', 'price': 2799, 'category': 'men', 'subcategory': 'jeans'},
        {'name': 'Casual Shirt', 'price': 1999, 'category': 'men', 'subcategory': 'casual-shirts'},
        {'name': 'Polo T-Shirt', 'price': 1299, 'category': 'men', 'subcategory': 'polo-shirts'}
    ],
    'tommy': [
        {'name': 'Classic Polo Shirt', 'price': 2499, 'category': 'men', 'subcategory': 'polo-shirts'},
        {'name': 'Cotton T-Shirt', 'price': 1599, 'category': 'men', 'subcategory': 't-shirts'},
        {'name': 'Chino Shorts', 'price': 2299, 'category': 'men', 'subcategory': 'shorts'},
        {'name': 'Linen Shirt', 'price': 2999, 'category': 'men', 'subcategory': 'casual-shirts'}
    ],
    'only': [
        {'name': 'Floral Summer Dress', 'price': 2799, 'category': 'women', 'subcategory': 'dresses'},
        {'name': 'High Waist Jeans', 'price': 3299, 'category': 'women', 'subcategory': 'jeans-women'},
        {'name': 'Striped Top', 'price': 1499, 'category': 'women', 'subcategory': 'tops'},
        {'name': 'Midi Skirt', 'price': 1899, 'category': 'women', 'subcategory': 'skirts-women'}
    ],
    'vero-moda': [
        {'name': 'Blazer', 'price': 4499, 'category': 'women', 'subcategory': 'blazers-women'},
        {'name': 'Silk Blouse', 'price': 2499, 'category': 'women', 'subcategory': 'tops'},
        {'name': 'Pencil Skirt', 'price': 2199, 'category': 'women', 'subcategory': 'skirts-women'},
        {'name': 'Evening Dress', 'price': 5999, 'category': 'women', 'subcategory': 'dresses'}
    ],
    'steve-madden': [
        {'name': 'High Heels', 'price': 4999, 'category': 'women', 'subcategory': 'heels'},
        {'name': 'Ankle Boots', 'price': 6499, 'category': 'women', 'subcategory': 'boots-women'},
        {'name': 'Flats', 'price': 2999, 'category': 'women', 'subcategory': 'flats'},
        {'name': 'Platform Sandals', 'price': 3999, 'category': 'women', 'subcategory': 'sandals-women'}
    ],
    'skechers': [
        {'name': 'Running Shoes', 'price': 5499, 'category': 'men', 'subcategory': 'sports-shoes'},
        {'name': 'Walking Sneakers', 'price': 4299, 'category': 'women', 'subcategory': 'sneakers-women'},
        {'name': 'Training Shoes', 'price': 4799, 'category': 'men', 'subcategory': 'casual-shoes'},
        {'name': 'Sport Sandals', 'price': 3299, 'category': 'women', 'subcategory': 'sandals-women'}
    ],
    'van-heusen': [
        {'name': 'Formal Suit', 'price': 8999, 'category': 'men', 'subcategory': 'suits'},
        {'name': 'Dress Shirt', 'price': 2499, 'category': 'men', 'subcategory': 'formal-shirts'},
        {'name': 'Business Trousers', 'price': 3299, 'category': 'men', 'subcategory': 'formal-trousers'},
        {'name': 'Silk Tie', 'price': 1299, 'category': 'men', 'subcategory': 'ties'}
    ]
}

# Sample image URLs
sample_images = [
    'https://picsum.photos/seed/product1/400/500.jpg',
    'https://picsum.photos/seed/product2/400/500.jpg',
    'https://picsum.photos/seed/product3/400/500.jpg',
    'https://picsum.photos/seed/product4/400/500.jpg'
]

print("Creating products for brands...")

for brand_slug, products in brand_products.items():
    try:
        brand = Brand.objects.get(slug=brand_slug, is_active=True)
        print(f"\nAdding products for {brand.name}...")
        
        for i, product_data in enumerate(products):
            try:
                category = Category.objects.get(slug=product_data['category'])
                subcategory = SubCategory.objects.get(slug=product_data['subcategory'], category=category)
                
                # Create unique SKU and slug
                import uuid
                unique_id = str(uuid.uuid4())[:8].upper()
                sku = f"{brand_slug.upper()}-{unique_id}"
                slug = f"{brand_slug}-{product_data['name'].lower().replace(' ', '-').replace('&', 'and')}-{unique_id}"
                
                # Create product
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=slug,
                    description=f"High quality {product_data['name']} by {brand.name}. Perfect for any occasion.",
                    short_description=f"Stylish {product_data['name']} from {brand.name} collection.",
                    price=product_data['price'],
                    category=category,
                    subcategory=subcategory,
                    brand=brand,
                    gender='men' if product_data['category'] == 'men' else 'women',
                    is_active=True,
                    stock_quantity=random.randint(10, 50),
                    sku=sku
                )
                
                # Add product image
                ProductImage.objects.create(
                    product=product,
                    image=sample_images[i % len(sample_images)],
                    alt_text=product.name
                )
                
                print(f"  - Created: {product.name} (${product_data['price']})")
                
            except Exception as e:
                print(f"  - Error creating {product_data['name']}: {e}")
                
    except Brand.DoesNotExist:
        print(f"Brand {brand_slug} not found")

print("\nProduct creation completed!")
