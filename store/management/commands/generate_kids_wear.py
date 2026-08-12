from django.core.management.base import BaseCommand
from store.models import Category, SubCategory, Brand, Product, ProductSize, ProductColor
from decimal import Decimal
import random
import string

class Command(BaseCommand):
    help = 'Generate kids wear products for specific categories'

    def handle(self, *args, **options):
        self.stdout.write('Generating kids wear products...')
        
        # Get or create required brands
        self.setup_brands()
        
        # Get kids category and subcategories
        kids_category = Category.objects.get(name='Kids')
        
        # Generate products for each category
        self.generate_boys_tshirts(kids_category)
        self.generate_boys_clothing(kids_category)
        self.generate_girls_dresses(kids_category)
        self.generate_girls_clothing(kids_category)
        
        self.stdout.write(self.style.SUCCESS('Kids wear products generated successfully!'))

    def setup_brands(self):
        """Ensure required brands exist"""
        required_brands = ['H&M', 'USPA', 'HRX', 'Pantaloons', 'Zara', 'Mothercare']
        
        for brand_name in required_brands:
            # Handle potential duplicates by using filter() and first()
            existing_brand = Brand.objects.filter(name=brand_name).first()
            if not existing_brand:
                Brand.objects.create(
                    name=brand_name,
                    slug=brand_name.lower().replace(' ', '-').replace('&', 'm')
                )

    def generate_slug(self, name):
        """Generate slug from name"""
        return name.lower().replace(' ', '-').replace('&', 'and').replace(',', '').replace('(', '').replace(')', '')

    def generate_sku(self):
        """Generate unique SKU"""
        return 'KIDS-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def generate_boys_tshirts(self, kids_category):
        """Generate products for boys T-shirts categories"""
        brands = ['H&M', 'USPA', 'HRX', 'Pantaloons']
        
        products_data = {
            'H&M Boys T-Shirts': [
                {
                    'name': 'H&M Boys Graphic Print T-Shirt',
                    'description': 'Comfortable cotton T-shirt with cool graphic print. Perfect for everyday wear and school.',
                    'short_description': 'Soft cotton graphic tee for boys',
                    'price': 599,
                    'discount_price': 399,
                    'stock': 50
                },
                {
                    'name': 'H&M Boys Striped Polo T-Shirt',
                    'description': 'Classic polo shirt with modern stripe design. Made from breathable cotton blend.',
                    'short_description': 'Stylish striped polo for boys',
                    'price': 799,
                    'discount_price': 559,
                    'stock': 40
                },
                {
                    'name': 'H&M Boys Solid Color T-Shirt',
                    'description': 'Essential solid color T-shirt available in multiple colors. Must-have for every boy\'s wardrobe.',
                    'short_description': 'Basic solid color tee for boys',
                    'price': 449,
                    'discount_price': 299,
                    'stock': 60
                }
            ],
            'USPA Boys T-Shirts': [
                {
                    'name': 'USPA Boys Logo T-Shirt',
                    'description': 'Sporty T-shirt featuring USPA logo. Perfect for active kids who love sports.',
                    'short_description': 'Athletic logo tee for boys',
                    'price': 899,
                    'discount_price': 629,
                    'stock': 35
                },
                {
                    'name': 'USPA Boys Performance T-Shirt',
                    'description': 'Moisture-wicking performance T-shirt ideal for sports and outdoor activities.',
                    'short_description': 'Sports performance tee for active boys',
                    'price': 1099,
                    'discount_price': 769,
                    'stock': 30
                }
            ],
            'HRX Boys T-Shirts': [
                {
                    'name': 'HRX Boys Training T-Shirt',
                    'description': 'Training T-shirt with HRX branding. Designed for comfort during physical activities.',
                    'short_description': 'Training tee for active boys',
                    'price': 999,
                    'discount_price': 699,
                    'stock': 45
                },
                {
                    'name': 'HRX Boys Athletic T-Shirt',
                    'description': 'Professional athletic wear T-shirt with quick-dry fabric technology.',
                    'short_description': 'Quick-dry athletic tee for boys',
                    'price': 1199,
                    'discount_price': 839,
                    'stock': 25
                }
            ],
            'Pantaloons Boys T-Shirts': [
                {
                    'name': 'Pantaloons Boys Casual T-Shirt',
                    'description': 'Comfortable casual T-shirt perfect for weekend outings and playtime.',
                    'short_description': 'Casual everyday tee for boys',
                    'price': 699,
                    'discount_price': 489,
                    'stock': 55
                },
                {
                    'name': 'Pantaloons Boys Printed T-Shirt',
                    'description': 'Fun printed T-shirt with vibrant colors and kid-friendly designs.',
                    'short_description': 'Colorful printed tee for boys',
                    'price': 749,
                    'discount_price': 524,
                    'stock': 40
                }
            ]
        }

        for subcategory_name, products in products_data.items():
            subcategory, _ = SubCategory.objects.get_or_create(
                name=subcategory_name,
                category=kids_category,
                defaults={'slug': self.generate_slug(subcategory_name)}
            )
            
            brand_name = subcategory_name.split(' ')[0]
            brand = Brand.objects.filter(name=brand_name).first()
            
            for product_data in products:
                self.create_product(product_data, subcategory, brand, 'kids')

    def generate_boys_clothing(self, kids_category):
        """Generate products for other boys clothing categories"""
        boys_clothing_subcats = [
            'Boys Shirts', 'Boys Shorts', 'Boys Jeans', 'Boys Trousers',
            'Clothing Sets', 'Ethnic Wear', 'Track Pants & Pyjamas',
            'Jacket, Sweater & Sweatshirts', 'Party Wear', 'Innerwear & Thermals',
            'Nightwear & Loungewear', 'Value Packs'
        ]
        
        for subcat_name in boys_clothing_subcats:
            subcategory, _ = SubCategory.objects.get_or_create(
                name=subcat_name,
                category=kids_category,
                defaults={'slug': self.generate_slug(subcat_name)}
            )
            
            # Generate 2-3 products per subcategory
            num_products = random.randint(2, 3)
            brands = ['H&M', 'USPA', 'HRX', 'Pantaloons']
            
            for i in range(num_products):
                brand = Brand.objects.filter(name=random.choice(brands)).first()
                self.generate_boys_clothing_product(subcat_name, subcategory, brand)

    def generate_girls_dresses(self, kids_category):
        """Generate products for girls dresses categories"""
        brands = ['Zara', 'USPA', 'Mothercare']
        
        products_data = {
            'Zara Girls Dresses': [
                {
                    'name': 'Zara Girls Floral Dress',
                    'description': 'Beautiful floral print dress with comfortable fit. Perfect for parties and special occasions.',
                    'short_description': 'Elegant floral dress for girls',
                    'price': 1299,
                    'discount_price': 909,
                    'stock': 30
                },
                {
                    'name': 'Zara Girls Summer Dress',
                    'description': 'Light and breezy summer dress made from soft cotton fabric.',
                    'short_description': 'Comfortable summer dress for girls',
                    'price': 1099,
                    'discount_price': 769,
                    'stock': 35
                }
            ],
            'USPA Girls Dresses': [
                {
                    'name': 'USPA Girls Sporty Dress',
                    'description': 'Sporty dress with USPA branding. Comfortable for active girls.',
                    'short_description': 'Athletic dress for active girls',
                    'price': 999,
                    'discount_price': 699,
                    'stock': 25
                }
            ],
            'Mothercare Girls Dresses': [
                {
                    'name': 'Mothercare Girls Party Dress',
                    'description': 'Elegant party dress with beautiful details. Perfect for special occasions.',
                    'short_description': 'Formal party dress for girls',
                    'price': 1499,
                    'discount_price': 1049,
                    'stock': 20
                },
                {
                    'name': 'Mothercare Girls Casual Dress',
                    'description': 'Comfortable casual dress for everyday wear and playtime.',
                    'short_description': 'Everyday casual dress for girls',
                    'price': 899,
                    'discount_price': 629,
                    'stock': 40
                }
            ]
        }

        for subcategory_name, products in products_data.items():
            subcategory, _ = SubCategory.objects.get_or_create(
                name=subcategory_name,
                category=kids_category,
                defaults={'slug': self.generate_slug(subcategory_name)}
            )
            
            brand_name = subcategory_name.split(' ')[0]
            brand = Brand.objects.filter(name=brand_name).first()
            
            for product_data in products:
                self.create_product(product_data, subcategory, brand, 'kids')

    def generate_girls_clothing(self, kids_category):
        """Generate products for other girls clothing categories"""
        girls_clothing_subcats = [
            'Girls Tops', 'Girls Tshirts', 'Clothing Sets', 'Lehenga choli',
            'Kurta Sets', 'Party wear', 'Dungarees & Jumpsuits',
            'Skirts & shorts', 'Tights & Leggings', 'Jeans, Trousers & Capris',
            'Jacket, Sweater & Sweatshirts', 'Innerwear & Thermals',
            'Nightwear & Loungewear', 'Value Packs'
        ]
        
        for subcat_name in girls_clothing_subcats:
            subcategory, _ = SubCategory.objects.get_or_create(
                name=subcat_name,
                category=kids_category,
                defaults={'slug': self.generate_slug(subcat_name)}
            )
            
            # Generate 2-3 products per subcategory
            num_products = random.randint(2, 3)
            brands = ['Zara', 'USPA', 'Mothercare']
            
            for i in range(num_products):
                brand = Brand.objects.filter(name=random.choice(brands)).first()
                self.generate_girls_clothing_product(subcat_name, subcategory, brand)

    def generate_boys_clothing_product(self, subcat_name, subcategory, brand):
        """Generate a single boys clothing product"""
        product_templates = {
            'Boys Shirts': [
                {'name': '{} Boys Casual Shirt', 'price_range': (799, 1299)},
                {'name': '{} Boys Formal Shirt', 'price_range': (999, 1599)}
            ],
            'Boys Shorts': [
                {'name': '{} Boys Denim Shorts', 'price_range': (699, 1099)},
                {'name': '{} Boys Cotton Shorts', 'price_range': (499, 799)}
            ],
            'Boys Jeans': [
                {'name': '{} Boys Slim Fit Jeans', 'price_range': (1199, 1899)},
                {'name': '{} Boys Regular Fit Jeans', 'price_range': (1099, 1699)}
            ],
            'Boys Trousers': [
                {'name': '{} Boys Formal Trousers', 'price_range': (899, 1399)},
                {'name': '{} Boys Casual Trousers', 'price_range': (799, 1199)}
            ],
            'Clothing Sets': [
                {'name': '{} Boys 2-Piece Set', 'price_range': (1299, 1999)},
                {'name': '{} Boys 3-Piece Set', 'price_range': (1599, 2499)}
            ],
            'Ethnic Wear': [
                {'name': '{} Boys Kurta Pyjama Set', 'price_range': (999, 1599)},
                {'name': '{} Boys Ethnic Outfit', 'price_range': (1299, 2099)}
            ],
            'Track Pants & Pyjamas': [
                {'name': '{} Boys Track Pants', 'price_range': (699, 1099)},
                {'name': '{} Boys Pyjama Set', 'price_range': (599, 999)}
            ],
            'Jacket, Sweater & Sweatshirts': [
                {'name': '{} Boys Hooded Sweatshirt', 'price_range': (999, 1599)},
                {'name': '{} Boys Denim Jacket', 'price_range': (1299, 1999)}
            ],
            'Party Wear': [
                {'name': '{} Boys Party Outfit', 'price_range': (1499, 2499)},
                {'name': '{} Boys Formal Suit', 'price_range': (1999, 2999)}
            ],
            'Innerwear & Thermals': [
                {'name': '{} Boys Innerwear Set', 'price_range': (399, 699)},
                {'name': '{} Boys Thermal Wear', 'price_range': (599, 999)}
            ],
            'Nightwear & Loungewear': [
                {'name': '{} Boys Pyjama Set', 'price_range': (499, 899)},
                {'name': '{} Boys Night Suit', 'price_range': (599, 999)}
            ],
            'Value Packs': [
                {'name': '{} Boys 3-Pack T-Shirts', 'price_range': (999, 1599)},
                {'name': '{} Boys 2-Pack Bottoms', 'price_range': (799, 1299)}
            ]
        }
        
        template = random.choice(product_templates.get(subcat_name, [{'name': '{} Boys Clothing', 'price_range': (599, 1299)}]))
        price_range = template['price_range']
        price = random.randint(price_range[0], price_range[1])
        discount_price = int(price * random.uniform(0.6, 0.85))
        
        product_data = {
            'name': template['name'].format(brand.name),
            'description': f'High-quality {subcat_name.lower()} from {brand.name}. Designed for comfort and style.',
            'short_description': f'Stylish {subcat_name.lower()} for boys',
            'price': price,
            'discount_price': discount_price,
            'stock': random.randint(20, 60)
        }
        
        self.create_product(product_data, subcategory, brand, 'kids')

    def generate_girls_clothing_product(self, subcat_name, subcategory, brand):
        """Generate a single girls clothing product"""
        product_templates = {
            'Girls Tops': [
                {'name': '{} Girls Casual Top', 'price_range': (599, 999)},
                {'name': '{} Girls Fancy Top', 'price_range': (799, 1299)}
            ],
            'Girls Tshirts': [
                {'name': '{} Girls Graphic T-Shirt', 'price_range': (499, 899)},
                {'name': '{} Girls Solid T-Shirt', 'price_range': (399, 699)}
            ],
            'Clothing Sets': [
                {'name': '{} Girls 2-Piece Set', 'price_range': (1199, 1899)},
                {'name': '{} Girls 3-Piece Set', 'price_range': (1499, 2399)}
            ],
            'Lehenga choli': [
                {'name': '{} Girls Lehenga Choli', 'price_range': (1599, 2999)},
                {'name': '{} Girls Traditional Lehenga', 'price_range': (1999, 3499)}
            ],
            'Kurta Sets': [
                {'name': '{} Girls Kurta Set', 'price_range': (999, 1599)},
                {'name': '{} Girls Ethnic Kurta', 'price_range': (1299, 1999)}
            ],
            'Party wear': [
                {'name': '{} Girls Party Dress', 'price_range': (1299, 2199)},
                {'name': '{} Girls Formal Outfit', 'price_range': (1599, 2699)}
            ],
            'Dungarees & Jumpsuits': [
                {'name': '{} Girls Dungaree', 'price_range': (899, 1499)},
                {'name': '{} Girls Jumpsuit', 'price_range': (999, 1699)}
            ],
            'Skirts & shorts': [
                {'name': '{} Girls Skirt', 'price_range': (599, 999)},
                {'name': '{} Girls Shorts', 'price_range': (499, 899)}
            ],
            'Tights & Leggings': [
                {'name': '{} Girls Leggings', 'price_range': (399, 699)},
                {'name': '{} Girls Tights', 'price_range': (299, 599)}
            ],
            'Jeans, Trousers & Capris': [
                {'name': '{} Girls Jeans', 'price_range': (999, 1599)},
                {'name': '{} Girls Capris', 'price_range': (699, 1099)}
            ],
            'Jacket, Sweater & Sweatshirts': [
                {'name': '{} Girls Sweatshirt', 'price_range': (899, 1499)},
                {'name': '{} Girls Cardigan', 'price_range': (999, 1599)}
            ],
            'Innerwear & Thermals': [
                {'name': '{} Girls Innerwear Set', 'price_range': (299, 599)},
                {'name': '{} Girls Thermal Wear', 'price_range': (499, 899)}
            ],
            'Nightwear & Loungewear': [
                {'name': '{} Girls Night Suit', 'price_range': (599, 999)},
                {'name': '{} Girls Loungewear Set', 'price_range': (699, 1099)}
            ],
            'Value Packs': [
                {'name': '{} Girls 3-Pack Tops', 'price_range': (899, 1399)},
                {'name': '{} Girls 2-Pack Bottoms', 'price_range': (699, 1099)}
            ]
        }
        
        template = random.choice(product_templates.get(subcat_name, [{'name': '{} Girls Clothing', 'price_range': (499, 1199)}]))
        price_range = template['price_range']
        price = random.randint(price_range[0], price_range[1])
        discount_price = int(price * random.uniform(0.6, 0.85))
        
        product_data = {
            'name': template['name'].format(brand.name),
            'description': f'Beautiful {subcat_name.lower()} from {brand.name}. Designed for comfort and style.',
            'short_description': f'Elegant {subcat_name.lower()} for girls',
            'price': price,
            'discount_price': discount_price,
            'stock': random.randint(20, 60)
        }
        
        self.create_product(product_data, subcategory, brand, 'kids')

    def create_product(self, product_data, subcategory, brand, gender):
        """Create a single product with sizes and colors"""
        # Check if product already exists
        existing_product = Product.objects.filter(name=product_data['name']).first()
        if existing_product:
            self.stdout.write(f'Product "{product_data["name"]}" already exists, skipping...')
            return
        
        product = Product.objects.create(
            name=product_data['name'],
            slug=self.generate_slug(product_data['name']),
            description=product_data['description'],
            short_description=product_data['short_description'],
            category=subcategory.category,
            subcategory=subcategory,
            brand=brand,
            gender=gender,
            price=Decimal(product_data['price']),
            discount_price=Decimal(product_data['discount_price']),
            stock_quantity=product_data['stock'],
            sku=self.generate_sku(),
            is_active=True,
            is_featured=random.choice([True, False])
        )
        
        # Add sizes
        sizes = ['2-3Y', '3-4Y', '4-5Y', '5-6Y', '6-7Y', '7-8Y', '8-9Y', '9-10Y', '10-11Y', '11-12Y']
        selected_sizes = random.sample(sizes, random.randint(4, 7))
        
        for size in selected_sizes:
            ProductSize.objects.create(
                product=product,
                size=size,
                stock_quantity=random.randint(5, 20)
            )
        
        # Add colors
        colors = [
            ('Red', '#FF0000'),
            ('Blue', '#0000FF'),
            ('Green', '#008000'),
            ('Yellow', '#FFFF00'),
            ('Pink', '#FFC0CB'),
            ('Purple', '#800080'),
            ('Orange', '#FFA500'),
            ('Black', '#000000'),
            ('White', '#FFFFFF'),
            ('Grey', '#808080'),
            ('Navy', '#000080'),
            ('Maroon', '#800000')
        ]
        
        selected_colors = random.sample(colors, random.randint(2, 5))
        
        for color_name, color_code in selected_colors:
            ProductColor.objects.create(
                product=product,
                color_name=color_name,
                color_code=color_code,
                stock_quantity=random.randint(5, 25)
            )
        
        self.stdout.write(f'Created product: {product.name}')
