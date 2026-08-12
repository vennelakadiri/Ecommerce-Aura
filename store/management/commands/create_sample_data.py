from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Category, SubCategory, Brand, Product, ProductImage, Banner, Review
from accounts.models import CustomerProfile, DeliveryBoyProfile, AdminProfile
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for the Aura ecommerce application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create demo users
        self.create_users()
        
        # Create categories and subcategories
        self.create_categories()
        
        # Create brands
        self.create_brands()
        
        # Create products
        self.create_products()
        
        # Create banners
        self.create_banners()
        
        # Create reviews
        self.create_reviews()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_users(self):
        # Create customer user
        customer_user, created = User.objects.get_or_create(
            username='customer@aura.com',
            defaults={
                'email': 'customer@aura.com',
                'role': 'customer',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '9876543210',
            }
        )
        if created:
            customer_user.set_password('customer123')
            customer_user.save()
            CustomerProfile.objects.create(user=customer_user, loyalty_points=100)

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin@aura.com',
            defaults={
                'email': 'admin@aura.com',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            AdminProfile.objects.create(user=admin_user, department='Management')

        # Create delivery boy user
        delivery_user, created = User.objects.get_or_create(
            username='delivery@aura.com',
            defaults={
                'email': 'delivery@aura.com',
                'role': 'delivery_boy',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'phone': '9876543211',
            }
        )
        if created:
            delivery_user.set_password('delivery123')
            delivery_user.save()
            DeliveryBoyProfile.objects.create(
                user=delivery_user,
                vehicle_type='bike',
                vehicle_number='DL01AB1234',
                license_number='DL123456789',
                is_available=True,
                rating=4.5
            )

    def create_categories(self):
        categories_data = [
            {
                'name': 'Men',
                'description': 'Men\'s clothing and accessories',
                'subcategories': ['Shirts', 'T-Shirts', 'Jeans', 'Trousers', 'Shorts', 'Jackets']
            },
            {
                'name': 'Women',
                'description': 'Women\'s clothing and accessories',
                'subcategories': ['Dresses', 'Tops', 'Jeans', 'Skirts', 'Kurtis', 'Sarees']
            },
            {
                'name': 'Kids',
                'description': 'Kids clothing and accessories',
                'subcategories': ['Boys Clothing', 'Girls Clothing', 'Baby Clothes', 'School Uniforms']
            },
            {
                'name': 'Accessories',
                'description': 'Fashion accessories',
                'subcategories': ['Bags', 'Watches', 'Sunglasses', 'Belts', 'Wallets', 'Jewelry']
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': cat_data['name'].lower(),
                    'description': cat_data['description']
                }
            )
            
            for sub_name in cat_data['subcategories']:
                SubCategory.objects.get_or_create(
                    category=category,
                    name=sub_name,
                    defaults={'slug': f"{sub_name.lower().replace(' ', '-')}-{category.slug}"}
                )

    def create_brands(self):
        brands_data = [
            'Nike', 'Adidas', 'Puma', 'Gucci', 'Prada', 'Balenciaga', 'Versace', 'Dior',
            'Louis Vuitton', 'H&M', 'Zara', 'Gap', 'Tommy Hilfiger', 'Calvin Klein', 'Levi\'s'
        ]

        for brand_name in brands_data:
            Brand.objects.get_or_create(
                name=brand_name,
                defaults={
                    'slug': brand_name.lower().replace(' ', '-').replace('\'', ''),
                    'description': f'{brand_name} - Premium fashion brand'
                }
            )

    def create_products(self):
        categories = list(Category.objects.all())
        brands = list(Brand.objects.all())
        subcategories = list(SubCategory.objects.all())
        
        if not categories or not brands or not subcategories:
            return
        
        # Define products with specific subcategories
        products_data = [
            # Men's T-Shirts
            {
                'name': 'Classic White Shirt',
                'description': 'A timeless white shirt perfect for any occasion. Made from premium cotton with a comfortable fit.',
                'short_description': 'Classic white formal shirt',
                'price': Decimal('49.99'),
                'discount_price': Decimal('39.99'),
                'stock_quantity': 50,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Shirts'
            },
            {
                'name': 'Blue Denim Shirt',
                'description': 'Casual blue denim shirt perfect for weekend outings.',
                'short_description': 'Blue denim casual shirt',
                'price': Decimal('59.99'),
                'discount_price': None,
                'stock_quantity': 40,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Shirts'
            },
            {
                'name': 'Striped Polo Shirt',
                'description': 'Classic polo shirt with stylish stripes in navy and white.',
                'short_description': 'Striped polo shirt',
                'price': Decimal('69.99'),
                'discount_price': Decimal('54.99'),
                'stock_quantity': 35,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Polo Shirts'
            },
            {
                'name': 'Graphic Print T-Shirt',
                'description': 'Modern graphic t-shirt with trendy print design.',
                'short_description': 'Graphic print t-shirt',
                'price': Decimal('34.99'),
                'discount_price': Decimal('24.99'),
                'stock_quantity': 60,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'T-Shirts'
            },
            {
                'name': 'Cotton V-Neck T-Shirt',
                'description': 'Comfortable v-neck t-shirt made from 100% cotton.',
                'short_description': 'Cotton v-neck t-shirt',
                'price': Decimal('29.99'),
                'discount_price': None,
                'stock_quantity': 45,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'T-Shirts'
            },
            {
                'name': 'Henley Long Sleeve Shirt',
                'description': 'Casual henley shirt with button placket.',
                'short_description': 'Henley long sleeve shirt',
                'price': Decimal('44.99'),
                'discount_price': Decimal('34.99'),
                'stock_quantity': 30,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Shirts'
            },
            {
                'name': 'Flannel Check Shirt',
                'description': 'Warm flannel shirt with classic check pattern.',
                'short_description': 'Flannel check shirt',
                'price': Decimal('54.99'),
                'discount_price': None,
                'stock_quantity': 25,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Shirts'
            },
            {
                'name': 'Athletic Performance T-Shirt',
                'description': 'High-performance athletic t-shirt with moisture-wicking fabric.',
                'short_description': 'Athletic performance t-shirt',
                'price': Decimal('44.99'),
                'discount_price': Decimal('34.99'),
                'stock_quantity': 35,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'T-Shirts'
            },
            {
                'name': 'Polo Style T-Shirt',
                'description': 'Classic polo style t-shirt with collar and button placket.',
                'short_description': 'Polo style t-shirt',
                'price': Decimal('39.99'),
                'discount_price': None,
                'stock_quantity': 40,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'T-Shirts'
            },
            {
                'name': 'Long Sleeve T-Shirt',
                'description': 'Comfortable long sleeve t-shirt perfect for cooler weather.',
                'short_description': 'Long sleeve t-shirt',
                'price': Decimal('36.99'),
                'discount_price': None,
                'stock_quantity': 38,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'T-Shirts'
            },
            {
                'name': 'Crew Neck Sweatshirt',
                'description': 'Cozy crew neck sweatshirt for casual comfort.',
                'short_description': 'Crew neck sweatshirt',
                'price': Decimal('54.99'),
                'discount_price': Decimal('44.99'),
                'stock_quantity': 25,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'T-Shirts'
            },
            
            # Men's Jeans
            {
                'name': 'Slim Fit Blue Jeans',
                'description': 'Modern slim fit blue jeans with stretch comfort.',
                'short_description': 'Slim fit blue jeans',
                'price': Decimal('89.99'),
                'discount_price': Decimal('69.99'),
                'stock_quantity': 40,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Regular Fit Black Jeans',
                'description': 'Classic regular fit black jeans for everyday wear.',
                'short_description': 'Regular fit black jeans',
                'price': Decimal('79.99'),
                'discount_price': None,
                'stock_quantity': 35,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Skinny Fit distressed Jeans',
                'description': 'Trendy skinny fit jeans with stylish distressing.',
                'short_description': 'Skinny distressed jeans',
                'price': Decimal('94.99'),
                'discount_price': Decimal('74.99'),
                'stock_quantity': 30,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Bootcut Denim Jeans',
                'description': 'Classic bootcut jeans in medium wash denim.',
                'short_description': 'Bootcut denim jeans',
                'price': Decimal('84.99'),
                'discount_price': None,
                'stock_quantity': 28,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Relaxed Fit Cargo Jeans',
                'description': 'Comfortable relaxed fit jeans with cargo pockets.',
                'short_description': 'Relaxed fit cargo jeans',
                'price': Decimal('99.99'),
                'discount_price': Decimal('79.99'),
                'stock_quantity': 22,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Dark Wash Straight Fit Jeans',
                'description': 'Classic straight fit jeans in dark wash.',
                'short_description': 'Dark wash straight jeans',
                'price': Decimal('109.99'),
                'discount_price': Decimal('87.99'),
                'stock_quantity': 18,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Jeans'
            },
            
            # Men's Wallets
            {
                'name': 'Genuine Leather Bifold Wallet',
                'description': 'Premium leather bifold wallet with multiple card slots.',
                'short_description': 'Leather bifold wallet',
                'price': Decimal('59.99'),
                'discount_price': None,
                'stock_quantity': 50,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Wallets'
            },
            {
                'name': 'Canvas Trifold Wallet',
                'description': 'Durable canvas trifold wallet with coin pocket.',
                'short_description': 'Canvas trifold wallet',
                'price': Decimal('24.99'),
                'discount_price': None,
                'stock_quantity': 40,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Wallets'
            },
            {
                'name': 'RFID Blocking Leather Wallet',
                'description': 'Modern leather wallet with RFID protection.',
                'short_description': 'RFID blocking wallet',
                'price': Decimal('79.99'),
                'discount_price': Decimal('64.99'),
                'stock_quantity': 35,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Wallets'
            },
            {
                'name': 'Minimalist Card Holder Wallet',
                'description': 'Slim minimalist wallet for essential cards only.',
                'short_description': 'Card holder wallet',
                'price': Decimal('34.99'),
                'discount_price': None,
                'stock_quantity': 60,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Wallets'
            },
            {
                'name': 'Travel Passport Wallet',
                'description': 'Secure travel wallet with passport compartment.',
                'short_description': 'Travel passport wallet',
                'price': Decimal('44.99'),
                'discount_price': None,
                'stock_quantity': 25,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Wallets'
            },
            {
                'name': 'Smart Phone Wallet',
                'description': 'Tech-enabled wallet with phone pocket and tracker.',
                'short_description': 'Smart phone wallet',
                'price': Decimal('89.99'),
                'discount_price': Decimal('71.99'),
                'stock_quantity': 20,
                'gender': 'men',
                'category': 'Men',
                'subcategory': 'Wallets'
            },
            
            # Women's Dresses
            {
                'name': 'Floral Summer Dress',
                'description': 'Beautiful floral print dress perfect for summer. Lightweight and comfortable fabric.',
                'short_description': 'Floral print summer dress',
                'price': Decimal('89.99'),
                'discount_price': Decimal('69.99'),
                'stock_quantity': 25,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Dresses'
            },
            {
                'name': 'Little Black Dress',
                'description': 'Elegant little black dress perfect for evening occasions.',
                'short_description': 'Little black dress',
                'price': Decimal('129.99'),
                'discount_price': Decimal('99.99'),
                'stock_quantity': 15,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Dresses'
            },
            {
                'name': 'Midi Wrap Dress',
                'description': 'Sophisticated midi wrap dress with flattering silhouette.',
                'short_description': 'Midi wrap dress',
                'price': Decimal('149.99'),
                'discount_price': Decimal('119.99'),
                'stock_quantity': 12,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Dresses'
            },
            {
                'name': 'Maxi Floral Dress',
                'description': 'Stunning maxi dress with beautiful floral print.',
                'short_description': 'Maxi floral dress',
                'price': Decimal('179.99'),
                'discount_price': Decimal('149.99'),
                'stock_quantity': 8,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Dresses'
            },
            {
                'name': 'Cocktail Party Dress',
                'description': 'Glamorous cocktail dress perfect for special occasions.',
                'short_description': 'Cocktail party dress',
                'price': Decimal('199.99'),
                'discount_price': Decimal('159.99'),
                'stock_quantity': 10,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Dresses'
            },
            {
                'name': 'Casual Sundress',
                'description': 'Comfortable sundress ideal for beach and casual outings.',
                'short_description': 'Casual sundress',
                'price': Decimal('79.99'),
                'discount_price': Decimal('64.99'),
                'stock_quantity': 20,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Dresses'
            },
            
            # Women's Tops
            {
                'name': 'Silk Blouse',
                'description': 'Elegant silk blouse with delicate details.',
                'short_description': 'Silk blouse',
                'price': Decimal('119.99'),
                'discount_price': Decimal('89.99'),
                'stock_quantity': 18,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Tops'
            },
            {
                'name': 'Cotton T-Shirt',
                'description': 'Comfortable cotton t-shirt perfect for everyday wear.',
                'short_description': 'Cotton t-shirt',
                'price': Decimal('39.99'),
                'discount_price': Decimal('29.99'),
                'stock_quantity': 45,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Tops'
            },
            {
                'name': 'Linen Button-Up Shirt',
                'description': 'Breathable linen shirt with button front.',
                'short_description': 'Linen shirt',
                'price': Decimal('69.99'),
                'discount_price': Decimal('54.99'),
                'stock_quantity': 22,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Tops'
            },
            {
                'name': 'Cashmere Sweater',
                'description': 'Luxurious cashmere sweater for cold weather.',
                'short_description': 'Cashmere sweater',
                'price': Decimal('189.99'),
                'discount_price': Decimal('149.99'),
                'stock_quantity': 12,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Tops'
            },
            {
                'name': 'Denim Jacket',
                'description': 'Casual denim jacket with modern fit.',
                'short_description': 'Denim jacket',
                'price': Decimal('149.99'),
                'discount_price': Decimal('119.99'),
                'stock_quantity': 16,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Tops'
            },
            
            # Women's Jeans
            {
                'name': 'High Waisted Skinny Jeans',
                'description': 'Fashionable high waisted skinny jeans in dark blue.',
                'short_description': 'High waisted skinny jeans',
                'price': Decimal('119.99'),
                'discount_price': Decimal('94.99'),
                'stock_quantity': 25,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Bootcut Stretch Jeans',
                'description': 'Comfortable bootcut jeans with stretch fabric.',
                'short_description': 'Bootcut stretch jeans',
                'price': Decimal('99.99'),
                'discount_price': Decimal('79.99'),
                'stock_quantity': 20,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Straight Leg Jeans',
                'description': 'Classic straight fit jeans for everyday comfort.',
                'short_description': 'Straight leg jeans',
                'price': Decimal('89.99'),
                'discount_price': None,
                'stock_quantity': 30,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Flare Jeans',
                'description': 'Trendy flare jeans with vintage-inspired silhouette.',
                'short_description': 'Flare jeans',
                'price': Decimal('109.99'),
                'discount_price': Decimal('87.99'),
                'stock_quantity': 15,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Jeans'
            },
            {
                'name': 'Ripped Boyfriend Jeans',
                'description': 'Casual ripped jeans with relaxed boyfriend fit.',
                'short_description': 'Ripped boyfriend jeans',
                'price': Decimal('94.99'),
                'discount_price': Decimal('74.99'),
                'stock_quantity': 18,
                'gender': 'women',
                'category': 'Women',
                'subcategory': 'Jeans'
            },
            
            # Kids - Boys Clothing
            {
                'name': 'Boys Graphic T-Shirt',
                'description': 'Cool graphic t-shirt with superhero print for boys.',
                'short_description': 'Boys graphic t-shirt',
                'price': Decimal('24.99'),
                'discount_price': Decimal('19.99'),
                'stock_quantity': 40,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Boys Clothing'
            },
            {
                'name': 'Boys Polo Shirt',
                'description': 'Classic polo shirt perfect for school and casual wear.',
                'short_description': 'Boys polo shirt',
                'price': Decimal('34.99'),
                'discount_price': None,
                'stock_quantity': 35,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Boys Clothing'
            },
            {
                'name': 'Boys Denim Jeans',
                'description': 'Durable denim jeans designed for active boys.',
                'short_description': 'Boys denim jeans',
                'price': Decimal('44.99'),
                'discount_price': Decimal('35.99'),
                'stock_quantity': 30,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Boys Clothing'
            },
            {
                'name': 'Boys Shorts Set',
                'description': 'Pack of 3 comfortable shorts for everyday wear.',
                'short_description': 'Boys shorts set',
                'price': Decimal('39.99'),
                'discount_price': Decimal('29.99'),
                'stock_quantity': 25,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Boys Clothing'
            },
            {
                'name': 'Boys Hoodie',
                'description': 'Warm and cozy hoodie perfect for cooler weather.',
                'short_description': 'Boys hoodie',
                'price': Decimal('49.99'),
                'discount_price': Decimal('39.99'),
                'stock_quantity': 20,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Boys Clothing'
            },
            {
                'name': 'Boys Track Suit',
                'description': 'Athletic track suit for sports and practice.',
                'short_description': 'Boys track suit',
                'price': Decimal('64.99'),
                'discount_price': Decimal('54.99'),
                'stock_quantity': 15,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Boys Clothing'
            },
            
            # Kids - Girls Clothing
            {
                'name': 'Girls Floral Dress',
                'description': 'Beautiful floral dress perfect for parties and special occasions.',
                'short_description': 'Girls floral dress',
                'price': Decimal('44.99'),
                'discount_price': Decimal('34.99'),
                'stock_quantity': 30,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Girls Clothing'
            },
            {
                'name': 'Girls Tunic Top',
                'description': 'Elegant tunic top with delicate embroidery details.',
                'short_description': 'Girls tunic top',
                'price': Decimal('34.99'),
                'discount_price': None,
                'stock_quantity': 25,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Girls Clothing'
            },
            {
                'name': 'Girls Leggings Set',
                'description': 'Comfortable leggings set perfect for school and play.',
                'short_description': 'Girls leggings set',
                'price': Decimal('29.99'),
                'discount_price': Decimal('24.99'),
                'stock_quantity': 35,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Girls Clothing'
            },
            {
                'name': 'Girls Skirt with Pockets',
                'description': 'Cute skirt with practical pockets for little treasures.',
                'short_description': 'Girls skirt with pockets',
                'price': Decimal('24.99'),
                'discount_price': None,
                'stock_quantity': 28,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Girls Clothing'
            },
            {
                'name': 'Girls Cardigan',
                'description': 'Cozy cardigan perfect for layering in cooler weather.',
                'short_description': 'Girls cardigan',
                'price': Decimal('39.99'),
                'discount_price': Decimal('31.99'),
                'stock_quantity': 22,
                'gender': 'kids',
                'category': 'Kids',
                'subcategory': 'Girls Clothing'
            },
            
            # Home - Bed Linen
            {
                'name': 'Luxury Cotton Bed Sheet Set',
                'description': 'Premium cotton bed sheets with high thread count for ultimate comfort.',
                'short_description': 'Luxury cotton bed sheets',
                'price': Decimal('89.99'),
                'discount_price': Decimal('71.99'),
                'stock_quantity': 20,
                'gender': 'unisex',
                'category': 'Home',
                'subcategory': 'Bed Linen & Furnishing'
            },
            {
                'name': 'Egyptian Cotton Duvet Cover',
                'description': 'Soft Egyptian cotton duvet cover with elegant pattern.',
                'short_description': 'Egyptian cotton duvet',
                'price': Decimal('64.99'),
                'discount_price': Decimal('54.99'),
                'stock_quantity': 25,
                'gender': 'unisex',
                'category': 'Home',
                'subcategory': 'Bed Linen & Furnishing'
            },
            {
                'name': 'Memory Foam Pillow',
                'description': 'Supportive memory foam pillow for better sleep quality.',
                'short_description': 'Memory foam pillow',
                'price': Decimal('44.99'),
                'discount_price': None,
                'stock_quantity': 30,
                'gender': 'unisex',
                'category': 'Home',
                'subcategory': 'Bed Linen & Furnishing'
            },
            {
                'name': 'Bamboo Mattress Protector',
                'description': 'Eco-friendly bamboo mattress protector with waterproof layer.',
                'short_description': 'Bamboo mattress protector',
                'price': Decimal('79.99'),
                'discount_price': Decimal('64.99'),
                'stock_quantity': 15,
                'gender': 'unisex',
                'category': 'Home',
                'subcategory': 'Bed Linen & Furnishing'
            },
            {
                'name': 'Silk Pillowcase Set',
                'description': 'Luxurious silk pillowcases with elegant finish.',
                'short_description': 'Silk pillowcase set',
                'price': Decimal('54.99'),
                'discount_price': None,
                'stock_quantity': 18,
                'gender': 'unisex',
                'category': 'Home',
                'subcategory': 'Bed Linen & Furnishing'
            },
            {
                'name': 'Weighted Blanket',
                'description': 'Cozy weighted blanket for better sleep and comfort.',
                'short_description': 'Weighted blanket',
                'price': Decimal('119.99'),
                'discount_price': Decimal('94.99'),
                'stock_quantity': 12,
                'gender': 'unisex',
                'category': 'Home',
                'subcategory': 'Bed Linen & Furnishing'
            },
            
            # Beauty - Makeup
            {
                'name': 'Matte Lipstick Set',
                'description': 'Collection of matte finish lipsticks in various shades.',
                'short_description': 'Matte lipstick set',
                'price': Decimal('59.99'),
                'discount_price': Decimal('44.99'),
                'stock_quantity': 25,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Makeup'
            },
            {
                'name': 'Liquid Foundation',
                'description': 'Lightweight liquid foundation with natural finish.',
                'short_description': 'Liquid foundation',
                'price': Decimal('44.99'),
                'discount_price': Decimal('34.99'),
                'stock_quantity': 30,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Makeup'
            },
            {
                'name': 'Mascara Volume',
                'description': 'Dramatic volume mascara for fuller lashes.',
                'short_description': 'Volume mascara',
                'price': Decimal('29.99'),
                'discount_price': None,
                'stock_quantity': 40,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Makeup'
            },
            {
                'name': 'Eyeshadow Palette',
                'description': 'Professional eyeshadow palette with 12 versatile shades.',
                'short_description': 'Eyeshadow palette',
                'price': Decimal('79.99'),
                'discount_price': Decimal('64.99'),
                'stock_quantity': 20,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Makeup'
            },
            {
                'name': 'Concealer Wand',
                'description': 'Precision concealer wand for flawless coverage.',
                'short_description': 'Concealer wand',
                'price': Decimal('24.99'),
                'discount_price': None,
                'stock_quantity': 35,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Makeup'
            },
            {
                'name': 'Setting Spray',
                'description': 'Professional makeup setting spray for long-lasting wear.',
                'short_description': 'Setting spray',
                'price': Decimal('34.99'),
                'discount_price': None,
                'stock_quantity': 25,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Makeup'
            },
            
            # Beauty - Skincare
            {
                'name': 'Vitamin C Serum',
                'description': 'Brightening vitamin C serum for radiant skin.',
                'short_description': 'Vitamin C serum',
                'price': Decimal('64.99'),
                'discount_price': Decimal('49.99'),
                'stock_quantity': 20,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Skincare'
            },
            {
                'name': 'Hyaluronic Acid Moisturizer',
                'description': 'Hydrating hyaluronic acid moisturizer for all skin types.',
                'short_description': 'Hyaluronic acid moisturizer',
                'price': Decimal('79.99'),
                'discount_price': Decimal('64.99'),
                'stock_quantity': 25,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Skincare'
            },
            {
                'name': 'Retinol Night Cream',
                'description': 'Anti-aging retinol night cream for youthful skin.',
                'short_description': 'Retinol night cream',
                'price': Decimal('89.99'),
                'discount_price': Decimal('71.99'),
                'stock_quantity': 15,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Skincare'
            },
            {
                'name': 'SPF 50 Sunscreen',
                'description': 'Broad spectrum SPF 50 sunscreen for daily protection.',
                'short_description': 'SPF 50 sunscreen',
                'price': Decimal('34.99'),
                'discount_price': None,
                'stock_quantity': 40,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Skincare'
            },
            {
                'name': 'Gentle Cleansing Balm',
                'description': 'Soothing cleansing balm for effective makeup removal.',
                'short_description': 'Cleansing balm',
                'price': Decimal('24.99'),
                'discount_price': None,
                'stock_quantity': 30,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Skincare'
            },
            
            # Beauty - Haircare
            {
                'name': 'Argan Oil Treatment',
                'description': 'Nourishing argan oil treatment for healthy, shiny hair.',
                'short_description': 'Argan oil treatment',
                'price': Decimal('29.99'),
                'discount_price': None,
                'stock_quantity': 35,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Haircare'
            },
            {
                'name': 'Repairing Hair Mask',
                'description': 'Intensive repairing hair mask for damaged hair.',
                'short_description': 'Repairing hair mask',
                'price': Decimal('19.99'),
                'discount_price': None,
                'stock_quantity': 45,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Haircare'
            },
            {
                'name': 'Volumizing Shampoo',
                'description': 'Body-building volumizing shampoo for fine hair.',
                'short_description': 'Volumizing shampoo',
                'price': Decimal('24.99'),
                'discount_price': None,
                'stock_quantity': 50,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Haircare'
            },
            {
                'name': 'Leave-In Conditioner',
                'description': 'Lightweight leave-in conditioner for detangling and shine.',
                'short_description': 'Leave-in conditioner',
                'price': Decimal('19.99'),
                'discount_price': None,
                'stock_quantity': 40,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Haircare'
            },
            
            # Beauty - Fragrances
            {
                'name': 'Floral Eau de Parfum',
                'description': 'Elegant floral fragrance with lasting scent.',
                'short_description': 'Floral perfume',
                'price': Decimal('149.99'),
                'discount_price': Decimal('119.99'),
                'stock_quantity': 12,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Fragrances'
            },
            {
                'name': 'Woody Cologne',
                'description': 'Sophisticated woody cologne with warm notes.',
                'short_description': 'Woody cologne',
                'price': Decimal('129.99'),
                'discount_price': Decimal('99.99'),
                'stock_quantity': 18,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Fragrances'
            },
            {
                'name': 'Citrus Body Mist',
                'description': 'Refreshing citrus body mist for daily freshness.',
                'short_description': 'Citrus body mist',
                'price': Decimal('44.99'),
                'discount_price': None,
                'stock_quantity': 25,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Fragrances'
            },
            {
                'name': 'Oriental Perfume Oil',
                'description': 'Exotic oriental perfume oil with rich, complex notes.',
                'short_description': 'Oriental perfume oil',
                'price': Decimal('189.99'),
                'discount_price': Decimal('149.99'),
                'stock_quantity': 8,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Fragrances'
            },
            {
                'name': 'Unisex Deodorant Stick',
                'description': 'Effective unisex deodorant stick for all-day protection.',
                'short_description': 'Unisex deodorant stick',
                'price': Decimal('14.99'),
                'discount_price': None,
                'stock_quantity': 60,
                'gender': 'unisex',
                'category': 'Beauty',
                'subcategory': 'Fragrances'
            }
        ]

        for i, product_data in enumerate(products_data):
            # Find the correct category and subcategory
            category = Category.objects.filter(name=product_data['category']).first()
            subcategory = SubCategory.objects.filter(category=category, name=product_data['subcategory']).first()
            brand = random.choice(brands)
            
            if not category or not subcategory:
                continue
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': f"{product_data['name'].lower().replace(' ', '-')}-{i}",
                    'description': product_data['description'],
                    'short_description': product_data['short_description'],
                    'category': category,
                    'subcategory': subcategory,
                    'brand': brand,
                    'gender': product_data['gender'],
                    'price': product_data['price'],
                    'discount_price': product_data.get('discount_price'),
                    'stock_quantity': product_data['stock_quantity'],
                    'sku': f'PRD{category.id}{subcategory.id}{i+1:04d}',
                    'is_active': True,
                    'is_featured': i < 4  # First 4 products are featured
                }
            )

            if created:
                # Create product images
                for j in range(1, 4):
                    ProductImage.objects.create(
                        product=product,
                        image=f'products/product{i+1}_{j}.jpg',
                        alt_text=f'{product.name} - Image {j}',
                        is_primary=(j == 1)
                    )

    def create_banners(self):
        banners_data = [
            {
                'title': 'Summer Sale',
                'subtitle': 'Up to 50% off on selected items',
                'button_text': 'Shop Now',
                'button_url': '/store/products/?sale=summer',
                'order': 1
            },
            {
                'title': 'New Collection',
                'subtitle': 'Discover our latest fashion trends',
                'button_text': 'Explore',
                'button_url': '/store/products/?new=true',
                'order': 2
            },
            {
                'title': 'Premium Brands',
                'subtitle': 'Exclusive designer collections',
                'button_text': 'View Brands',
                'button_url': '/store/products/?premium=true',
                'order': 3
            },
            {
                'title': 'Flash Sale',
                'subtitle': 'Limited time offers',
                'button_text': 'Grab Deal',
                'button_url': '/store/products/?flash=true',
                'order': 4
            }
        ]

        for banner_data in banners_data:
            Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults={
                    'subtitle': banner_data['subtitle'],
                    'button_text': banner_data['button_text'],
                    'button_url': banner_data['button_url'],
                    'order': banner_data['order']
                }
            )

    def create_reviews(self):
        products = list(Product.objects.all()[:5])  # First 5 products
        customer_user = User.objects.filter(role='customer').first()
        
        if not customer_user:
            return
            
        review_texts = [
            {
                'title': 'Excellent Quality',
                'comment': 'Really impressed with the quality of this product. Highly recommended!'
            },
            {
                'title': 'Good Value',
                'comment': 'Great product for the price. Fits well and looks good.'
            },
            {
                'title': 'Amazing Product',
                'comment': 'Exactly what I was looking for. Perfect fit and great material.'
            },
            {
                'title': 'Satisfied',
                'comment': 'Good quality product. Would definitely buy again.'
            },
            {
                'title': 'Love It!',
                'comment': 'Absolutely love this product. Exceeded my expectations.'
            }
        ]

        for i, product in enumerate(products):
            review_data = review_texts[i % len(review_texts)]
            rating = random.randint(4, 5)
            
            Review.objects.get_or_create(
                product=product,
                user_name=customer_user.username,
                rating=rating,
                title=review_data['title'],
                comment=review_data['comment'],
                is_verified_purchase=True
            )
