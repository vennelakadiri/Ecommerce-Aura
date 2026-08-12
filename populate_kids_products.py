import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, Category, SubCategory, Brand, ProductImage

# Get kids category and existing brands
kids_category = Category.objects.get(slug='kids')
brands = list(Brand.objects.all())

# Product data for missing subcategories
boys_products = {
    'USPA Boys T-Shirts': [
        {'name': 'USPA Boys Graphic T-Shirt', 'price': 899, 'discount': 699, 'description': 'Comfortable cotton graphic t-shirt with USPA branding. Perfect for casual wear and everyday activities.'},
        {'name': 'USPA Boys Polo T-Shirt', 'price': 1099, 'discount': 899, 'description': 'Classic polo shirt with collar, made from premium cotton fabric. Ideal for semi-formal occasions.'},
        {'name': 'USPA Boys Sports T-Shirt', 'price': 799, 'discount': 599, 'description': 'Moisture-wicking sports t-shirt designed for active kids. Quick-dry fabric keeps them comfortable during play.'},
        {'name': 'USPA Boys Striped T-Shirt', 'price': 949, 'discount': 749, 'description': 'Stylish striped t-shirt with modern design. Soft and breathable fabric for all-day comfort.'},
        {'name': 'USPA Boys Printed T-Shirt', 'price': 849, 'discount': 649, 'description': 'Fun printed t-shirt with colorful graphics. Made from 100% cotton for maximum comfort.'},
    ],
    'HRX Boys T-Shirts': [
        {'name': 'HRX Boys Gym T-Shirt', 'price': 999, 'discount': 799, 'description': 'Performance gym t-shirt by HRX. Designed for workouts and sports activities with sweat-wicking technology.'},
        {'name': 'HRX Boys Athletic T-Shirt', 'price': 899, 'discount': 699, 'description': 'Athletic fit t-shirt perfect for sports. Features HRX logo and modern styling.'},
        {'name': 'HRX Boys Training T-Shirt', 'price': 1099, 'discount': 899, 'description': 'Professional training t-shirt for serious young athletes. Advanced fabric technology.'},
        {'name': 'HRX Boys Casual T-Shirt', 'price': 799, 'discount': 599, 'description': 'Casual everyday t-shirt with HRX branding. Comfortable fit for daily wear.'},
    ],
    'Pantaloons Boys T-Shirts': [
        {'name': 'Pantaloons Boys Cartoon T-Shirt', 'price': 699, 'discount': 499, 'description': 'Fun cartoon-printed t-shirt for kids. Bright colors and playful designs that kids love.'},
        {'name': 'Pantaloons Boys Plain T-Shirt', 'price': 599, 'discount': 399, 'description': 'Simple plain t-shirt in solid colors. Versatile piece that goes with everything.'},
        {'name': 'Pantaloons Boys Summer T-Shirt', 'price': 649, 'discount': 449, 'description': 'Lightweight summer t-shirt perfect for hot weather. Breathable fabric keeps kids cool.'},
        {'name': 'Pantaloons Boys School T-Shirt', 'price': 749, 'discount': 549, 'description': 'Durable school t-shirt designed for daily wear. Easy to wash and maintain.'},
    ],
    'Boys Shirts': [
        {'name': 'Boys Casual Shirt', 'price': 1299, 'discount': 999, 'description': 'Comfortable casual shirt for everyday wear. Button-down style with pocket detail.'},
        {'name': 'Boys Formal Shirt', 'price': 1599, 'discount': 1199, 'description': 'Elegant formal shirt perfect for special occasions. Crisp fabric with classic styling.'},
        {'name': 'Boys Denim Shirt', 'price': 1499, 'discount': 1099, 'description': 'Trendy denim shirt with modern fit. Great for casual outings and weekend wear.'},
        {'name': 'Boys Checkered Shirt', 'price': 1399, 'discount': 999, 'description': 'Stylish checkered shirt with contemporary pattern. Perfect for smart-casual look.'},
        {'name': 'Boys Linen Shirt', 'price': 1699, 'discount': 1299, 'description': 'Premium linen shirt ideal for summer. Lightweight and breathable fabric.'},
    ],
    'Boys Shorts': [
        {'name': 'Boys Cargo Shorts', 'price': 999, 'discount': 799, 'description': 'Functional cargo shorts with multiple pockets. Perfect for outdoor activities and adventures.'},
        {'name': 'Boys Denim Shorts', 'price': 899, 'discount': 699, 'description': 'Classic denim shorts with comfortable fit. Durable fabric that withstands active play.'},
        {'name': 'Boys Sports Shorts', 'price': 799, 'discount': 599, 'description': 'Athletic shorts designed for sports and physical activities. Moisture-wicking fabric.'},
        {'name': 'Boys Cotton Shorts', 'price': 699, 'discount': 499, 'description': 'Soft cotton shorts for everyday comfort. Elastic waistband for easy wear.'},
        {'name': 'Boys Beach Shorts', 'price': 849, 'discount': 649, 'description': 'Quick-dry beach shorts perfect for swimming and water activities. UV protection fabric.'},
    ],
    'Boys Jeans': [
        {'name': 'Boys Skinny Jeans', 'price': 1599, 'discount': 1199, 'description': 'Trendy skinny fit jeans for modern kids. Stretchable fabric for comfort and movement.'},
        {'name': 'Boys Regular Fit Jeans', 'price': 1499, 'discount': 1099, 'description': 'Classic regular fit jeans that never go out of style. Durable denim construction.'},
        {'name': 'Boys Distressed Jeans', 'price': 1699, 'discount': 1299, 'description': 'Fashionable distressed jeans with stylish rips and fades. Perfect for trendy look.'},
        {'name': 'Boys Cargo Jeans', 'price': 1799, 'discount': 1399, 'description': 'Utility cargo jeans with extra pockets. Combines style with functionality.'},
        {'name': 'Boys Slim Fit Jeans', 'price': 1549, 'discount': 1149, 'description': 'Modern slim fit jeans for stylish appearance. Comfortable stretch fabric.'},
    ],
    'Boys Trousers': [
        {'name': 'Boys Formal Trousers', 'price': 1899, 'discount': 1499, 'description': 'Elegant formal trousers for special occasions. Premium fabric with perfect fit.'},
        {'name': 'Boys Chinos', 'price': 1599, 'discount': 1199, 'description': 'Versatile chino trousers perfect for smart-casual wear. Comfortable and stylish.'},
        {'name': 'Boys Dress Pants', 'price': 1799, 'discount': 1399, 'description': 'Sophisticated dress pants for formal events. Classic design with modern comfort.'},
        {'name': 'Boys Casual Trousers', 'price': 1399, 'discount': 999, 'description': 'Comfortable casual trousers for everyday wear. Easy to maintain and style.'},
    ],
    'Clothing Sets': [
        {'name': 'Boys 2-Piece Set', 'price': 1999, 'discount': 1499, 'description': 'Coordinated 2-piece set with t-shirt and shorts. Perfect matching outfit for casual wear.'},
        {'name': 'Boys 3-Piece Set', 'price': 2499, 'discount': 1899, 'description': 'Complete 3-piece set with shirt, shorts, and cap. Stylish coordinated outfit.'},
        {'name': 'Boys Summer Set', 'price': 1799, 'discount': 1299, 'description': 'Lightweight summer set with breathable fabrics. Perfect for hot weather.'},
        {'name': 'Boys Party Wear Set', 'price': 2999, 'discount': 2299, 'description': 'Elegant party wear set for special occasions. Premium fabrics and stylish design.'},
    ],
    'Ethnic Wear': [
        {'name': 'Boys Kurta Set', 'price': 2299, 'discount': 1699, 'description': 'Traditional kurta set with matching pajama. Perfect for festivals and celebrations.'},
        {'name': 'Boys Sherwani', 'price': 3999, 'discount': 2999, 'description': 'Elegant sherwani for weddings and formal events. Intricate embroidery and premium fabric.'},
        {'name': 'Boys Dhoti Kurta', 'price': 2499, 'discount': 1899, 'description': 'Classic dhoti kurta set for traditional occasions. Comfortable and authentic design.'},
        {'name': 'Boys Nehru Jacket Set', 'price': 2799, 'discount': 2099, 'description': 'Sophisticated Nehru jacket with kurta. Perfect for formal cultural events.'},
    ],
    'Track Pants & Pyjamas': [
        {'name': 'Boys Track Pants', 'price': 999, 'discount': 799, 'description': 'Comfortable track pants for sports and lounging. Elastic waistband with drawstring.'},
        {'name': 'Boys Joggers', 'price': 1099, 'discount': 899, 'description': 'Stylish joggers perfect for active kids. Soft fabric with modern fit.'},
        {'name': 'Boys Pyjama Set', 'price': 899, 'discount': 699, 'description': 'Comfortable pyjama set for good night sleep. Soft cotton fabric.'},
        {'name': 'Boys Sports Track Pants', 'price': 1199, 'discount': 899, 'description': 'Professional track pants for sports training. Moisture-wicking technology.'},
    ],
    'Jacket, Sweater & Sweatshirts': [
        {'name': 'Boys Denim Jacket', 'price': 2499, 'discount': 1899, 'description': 'Classic denim jacket with modern styling. Perfect for layering and casual outings.'},
        {'name': 'Boys Hooded Sweatshirt', 'price': 1299, 'discount': 999, 'description': 'Comfortable hooded sweatshirt with kangaroo pocket. Ideal for casual wear.'},
        {'name': 'Boys Winter Jacket', 'price': 3499, 'discount': 2499, 'description': 'Warm winter jacket with insulation. Perfect for cold weather protection.'},
        {'name': 'Boys Sweater', 'price': 1499, 'discount': 1099, 'description': 'Cozy wool sweater for winter. Classic design with modern comfort.'},
        {'name': 'Boys Bomber Jacket', 'price': 2799, 'discount': 1999, 'description': 'Trendy bomber jacket with ribbed cuffs. Stylish and functional.'},
    ],
    'Party Wear': [
        {'name': 'Boys Party Suit', 'price': 4999, 'discount': 3499, 'description': 'Elegant party suit for special occasions. Complete 3-piece suit with premium fabric.'},
        {'name': 'Boys Formal Blazer', 'price': 2999, 'discount': 1999, 'description': 'Sophisticated blazer perfect for formal events. Classic design with modern fit.'},
        {'name': 'Boys Dress Shirt Set', 'price': 1999, 'discount': 1499, 'description': 'Formal dress shirt with matching accessories. Perfect for celebrations.'},
        {'name': 'Boys Party Outfit', 'price': 3499, 'discount': 2499, 'description': 'Complete party outfit with coordinated pieces. Stylish and elegant.'},
    ],
    'Innerwear & Thermals': [
        {'name': 'Boys Briefs Pack', 'price': 599, 'discount': 399, 'description': 'Comfortable briefs pack of 3. Soft cotton fabric for all-day comfort.'},
        {'name': 'Boys Boxers Pack', 'price': 699, 'discount': 499, 'description': 'Loose-fit boxers pack of 3. Breathable fabric for comfort.'},
        {'name': 'Boys Thermals Set', 'price': 999, 'discount': 799, 'description': 'Warm thermal set for winter. Provides insulation and comfort in cold weather.'},
        {'name': 'Boys Vests Pack', 'price': 499, 'discount': 299, 'description': 'Soft vests pack of 3. Essential layering piece for comfort.'},
    ],
    'Nightwear & Loungewear': [
        {'name': 'Boys Night Suit', 'price': 899, 'discount': 699, 'description': 'Comfortable night suit for peaceful sleep. Soft fabric with relaxed fit.'},
        {'name': 'Boys Pajama Set', 'price': 799, 'discount': 599, 'description': 'Classic pajama set for bedtime. Cozy and comfortable.'},
        {'name': 'Boys Lounge Set', 'price': 999, 'discount': 799, 'description': 'Stylish lounge set for relaxing at home. Modern design with comfort.'},
        {'name': 'Boys Sleep Shirt', 'price': 699, 'discount': 499, 'description': 'Comfortable sleep shirt for restful nights. Breathable fabric.'},
    ],
    'Value Packs': [
        {'name': 'Boys T-Shirt Pack', 'price': 1999, 'discount': 1499, 'description': 'Value pack of 5 colorful t-shirts. Essential basics for everyday wear.'},
        {'name': 'Boys Shorts Pack', 'price': 1799, 'discount': 1299, 'description': 'Pack of 3 comfortable shorts. Perfect for summer and casual wear.'},
        {'name': 'Boys Innerwear Pack', 'price': 999, 'discount': 699, 'description': 'Complete innerwear pack with essentials. Great value for money.'},
        {'name': 'Boys Socks Pack', 'price': 599, 'discount': 399, 'description': 'Pack of 6 colorful socks. Soft and comfortable for daily wear.'},
    ]
}

girls_products = {
    'Gap Girls Dresses': [
        {'name': 'Gap Girls Floral Dress', 'price': 1899, 'discount': 1399, 'description': 'Beautiful floral dress with modern design. Perfect for parties and special occasions.'},
        {'name': 'Gap Girls Summer Dress', 'price': 1699, 'discount': 1199, 'description': 'Lightweight summer dress with bright colors. Comfortable fabric for hot weather.'},
        {'name': 'Gap Girls Party Dress', 'price': 2499, 'discount': 1899, 'description': 'Elegant party dress with stylish details. Perfect for celebrations and events.'},
        {'name': 'Gap Girls Casual Dress', 'price': 1499, 'discount': 999, 'description': 'Comfortable casual dress for everyday wear. Easy to wash and maintain.'},
        {'name': 'Gap Girls Printed Dress', 'price': 1799, 'discount': 1299, 'description': 'Fun printed dress with colorful patterns. Stylish and comfortable.'},
    ],
    'H&M Girls Dresses': [
        {'name': 'H&M Girls Maxi Dress', 'price': 1999, 'discount': 1499, 'description': 'Elegant maxi dress with modern design. Perfect for formal occasions.'},
        {'name': 'H&M Girls Short Dress', 'price': 1599, 'discount': 1099, 'description': 'Trendy short dress with contemporary style. Great for casual outings.'},
        {'name': 'H&M Girls A-Line Dress', 'price': 1799, 'discount': 1299, 'description': 'Classic A-line dress with timeless appeal. Flattering fit for all body types.'},
        {'name': 'H&M Girls Wrap Dress', 'price': 1899, 'discount': 1399, 'description': 'Stylish wrap dress with adjustable fit. Versatile for various occasions.'},
    ],
    'Zara Girls Dresses': [
        {'name': 'Zara Girls Designer Dress', 'price': 2999, 'discount': 1999, 'description': 'High-fashion designer dress from Zara. Premium fabric and elegant design.'},
        {'name': 'Zara Girls Cocktail Dress', 'price': 3499, 'discount': 2499, 'description': 'Sophisticated cocktail dress for special events. Modern and stylish.'},
        {'name': 'Zara Girls Day Dress', 'price': 2199, 'discount': 1599, 'description': 'Chic day dress perfect for outings. Comfortable and fashionable.'},
        {'name': 'Zara Girls Evening Dress', 'price': 3999, 'discount': 2999, 'description': 'Elegant evening dress for formal occasions. Luxurious fabric and design.'},
    ],
    'USPA Girls Dresses': [
        {'name': 'USPA Girls Tennis Dress', 'price': 2299, 'discount': 1699, 'description': 'Sporty tennis dress with athletic design. Perfect for sports and active wear.'},
        {'name': 'USPA Girls Polo Dress', 'price': 1999, 'discount': 1499, 'description': 'Classic polo dress with collar. Sporty yet elegant design.'},
        {'name': 'USPA Girls Sports Dress', 'price': 1899, 'discount': 1399, 'description': 'Performance sports dress for active girls. Moisture-wicking fabric.'},
        {'name': 'USPA Girls Casual Dress', 'price': 1799, 'discount': 1299, 'description': 'Comfortable casual dress for everyday wear. Stylish and practical.'},
    ],
    'Mothercare Girls Dresses': [
        {'name': 'Mothercare Girls Baby Dress', 'price': 1299, 'discount': 999, 'description': 'Soft baby dress with gentle fabric. Designed for comfort and safety.'},
        {'name': 'Mothercare Girls Toddler Dress', 'price': 1499, 'discount': 1099, 'description': 'Cute toddler dress with playful design. Easy to wear and wash.'},
        {'name': 'Mothercare Girls Party Dress', 'price': 1999, 'discount': 1499, 'description': 'Elegant party dress for little girls. Beautiful design with comfort.'},
        {'name': 'Mothercare Girls Summer Dress', 'price': 1399, 'discount': 999, 'description': 'Lightweight summer dress for toddlers. Breathable fabric for comfort.'},
    ],
    'Girls Tops': [
        {'name': 'Girls Casual Top', 'price': 999, 'discount': 699, 'description': 'Comfortable casual top for everyday wear. Versatile piece for various occasions.'},
        {'name': 'Girls Fancy Top', 'price': 1299, 'discount': 999, 'description': 'Stylish fancy top with modern design. Perfect for outings and parties.'},
        {'name': 'Girls Cotton Top', 'price': 899, 'discount': 699, 'description': 'Soft cotton top for comfort. Breathable fabric for all-day wear.'},
        {'name': 'Girls Designer Top', 'price': 1599, 'discount': 1199, 'description': 'Fashionable designer top with trendy details. Perfect for fashion-forward girls.'},
        {'name': 'Girls Sleeveless Top', 'price': 799, 'discount': 599, 'description': 'Comfortable sleeveless top for summer. Lightweight and breathable.'},
    ],
    'Girls Tshirts': [
        {'name': 'Girls Graphic T-Shirt', 'price': 899, 'discount': 699, 'description': 'Fun graphic t-shirt with colorful prints. Made from soft cotton fabric.'},
        {'name': 'Girls Printed T-Shirt', 'price': 799, 'discount': 599, 'description': 'Stylish printed t-shirt with modern patterns. Perfect for casual wear.'},
        {'name': 'Girls Plain T-Shirt', 'price': 699, 'discount': 499, 'description': 'Simple plain t-shirt in solid colors. Essential basic for every wardrobe.'},
        {'name': 'Girls Cartoon T-Shirt', 'price': 849, 'discount': 649, 'description': 'Fun cartoon-printed t-shirt kids love. Bright colors and playful designs.'},
        {'name': 'Girls Sports T-Shirt', 'price': 999, 'discount': 799, 'description': 'Athletic t-shirt for active girls. Moisture-wicking fabric for sports.'},
    ],
    'Girls Tights & Leggings': [
        {'name': 'Girls Cotton Leggings', 'price': 799, 'discount': 599, 'description': 'Comfortable cotton leggings for everyday wear. Stretchable and soft fabric.'},
        {'name': 'Girls Printed Leggings', 'price': 899, 'discount': 699, 'description': 'Stylish printed leggings with fun patterns. Perfect for casual and school wear.'},
        {'name': 'Girls Sports Tights', 'price': 999, 'discount': 799, 'description': 'Athletic tights for sports and activities. Moisture-wicking and stretchable.'},
        {'name': 'Girls Plain Tights', 'price': 699, 'discount': 499, 'description': 'Basic plain tights in solid colors. Essential wardrobe staple.'},
    ],
    'Girls Jeans, Trousers & Capris': [
        {'name': 'Girls Skinny Jeans', 'price': 1899, 'discount': 1399, 'description': 'Trendy skinny fit jeans for stylish girls. Stretchable denim for comfort.'},
        {'name': 'Girls Bootcut Jeans', 'price': 1999, 'discount': 1499, 'description': 'Classic bootcut jeans with flattering fit. Durable denim construction.'},
        {'name': 'Girls Capris', 'price': 1299, 'discount': 999, 'description': 'Comfortable capris perfect for summer. Casual and stylish design.'},
        {'name': 'Girls Trousers', 'price': 1599, 'discount': 1199, 'description': 'Versatile trousers for various occasions. Comfortable and practical.'},
        {'name': 'Girls jeggings', 'price': 1399, 'discount': 999, 'description': 'Comfortable jeggings with denim look. Stretchable fabric for ease of movement.'},
    ],
    'Girls Skirts & shorts': [
        {'name': 'Girls Denim Skirt', 'price': 1299, 'discount': 999, 'description': 'Trendy denim skirt with modern design. Perfect for casual outings.'},
        {'name': 'Girls Pleated Skirt', 'price': 1499, 'discount': 1099, 'description': 'Classic pleated skirt for school and formal wear. Elegant and comfortable.'},
        {'name': 'Girls Cotton Shorts', 'price': 899, 'discount': 699, 'description': 'Comfortable cotton shorts for summer. Breathable fabric for comfort.'},
        {'name': 'Girls Sports Shorts', 'price': 999, 'discount': 799, 'description': 'Athletic shorts for sports and activities. Moisture-wicking fabric.'},
        {'name': 'Girls Tennis Skirt', 'price': 1199, 'discount': 899, 'description': 'Sporty tennis skirt with built-in shorts. Perfect for tennis and sports.'},
    ],
    'Girls Dungarees & Jumpsuits': [
        {'name': 'Girls Denim Dungarees', 'price': 1799, 'discount': 1299, 'description': 'Classic denim dungarees with adjustable straps. Casual and comfortable.'},
        {'name': 'Girls Cotton Jumpsuit', 'price': 1599, 'discount': 1199, 'description': 'Comfortable cotton jumpsuit for all-day wear. Easy to style and wear.'},
        {'name': 'Girls Printed Dungarees', 'price': 1899, 'discount': 1399, 'description': 'Stylish printed dungarees with modern patterns. Fun and fashionable.'},
        {'name': 'Girls Casual Jumpsuit', 'price': 1699, 'discount': 1299, 'description': 'Versatile casual jumpsuit perfect for outings. Comfortable and stylish.'},
    ],
    'Girls Jacket, Sweater & Sweatshirts': [
        {'name': 'Girls Denim Jacket', 'price': 2299, 'discount': 1699, 'description': 'Classic denim jacket with feminine design. Perfect for layering.'},
        {'name': 'Girls Hooded Sweatshirt', 'price': 1199, 'discount': 899, 'description': 'Cozy hooded sweatshirt with feminine details. Comfortable and stylish.'},
        {'name': 'Girls Cardigan', 'price': 1399, 'discount': 999, 'description': 'Elegant cardigan perfect for layering. Soft and warm fabric.'},
        {'name': 'Girls Winter Jacket', 'price': 3199, 'discount': 2299, 'description': 'Warm winter jacket with insulation. Protects from cold weather.'},
        {'name': 'Girls Sweater', 'price': 1299, 'discount': 999, 'description': 'Cozy sweater for winter. Stylish design with comfort.'},
    ],
    'Girls Innerwear & Thermals': [
        {'name': 'Girls Camisole Pack', 'price': 599, 'discount': 399, 'description': 'Comfortable camisole pack of 3. Soft fabric for everyday wear.'},
        {'name': 'Girls Briefs Pack', 'price': 499, 'discount': 299, 'description': 'Soft briefs pack of 3. Comfortable and breathable fabric.'},
        {'name': 'Girls Thermals Set', 'price': 899, 'discount': 699, 'description': 'Warm thermal set for winter. Provides insulation and comfort.'},
        {'name': 'Girls Bra Pack', 'price': 799, 'discount': 599, 'description': 'Comfortable bra pack for growing girls. Soft and supportive fabric.'},
    ],
    'Girls Nightwear & Loungewear': [
        {'name': 'Girls Night Suit', 'price': 999, 'discount': 799, 'description': 'Comfortable night suit for peaceful sleep. Soft fabric with pretty design.'},
        {'name': 'Girls Pajama Set', 'price': 899, 'discount': 699, 'description': 'Cute pajama set for bedtime. Cozy and comfortable.'},
        {'name': 'Girls Night Gown', 'price': 799, 'discount': 599, 'description': 'Elegant night gown for comfortable sleep. Soft and breathable fabric.'},
        {'name': 'Girls Lounge Set', 'price': 1099, 'discount': 899, 'description': 'Stylish lounge set for relaxing at home. Modern design with comfort.'},
    ],
    'Girls Value Packs': [
        {'name': 'Girls T-Shirt Pack', 'price': 1799, 'discount': 1299, 'description': 'Value pack of 5 colorful t-shirts. Essential basics for everyday wear.'},
        {'name': 'Girls Leggings Pack', 'price': 1999, 'discount': 1499, 'description': 'Pack of 3 comfortable leggings. Perfect for school and casual wear.'},
        {'name': 'Girls Innerwear Pack', 'price': 899, 'discount': 699, 'description': 'Complete innerwear pack with essentials. Great value for money.'},
        {'name': 'Girls Socks Pack', 'price': 499, 'discount': 299, 'description': 'Pack of 6 colorful socks. Soft and comfortable for daily wear.'},
    ]
}

def create_products():
    # Create boys products
    for subcategory_name, products in boys_products.items():
        subcategory = SubCategory.objects.filter(category=kids_category, name=subcategory_name).first()
        if subcategory:
            for product_data in products:
                # Check if product already exists
                if not Product.objects.filter(name=product_data['name'], subcategory=subcategory).exists():
                    product = Product.objects.create(
                        name=product_data['name'],
                        slug=f"{product_data['name'].lower().replace(' ', '-').replace(',', '-')}-{random.randint(1000, 9999)}",
                        description=product_data['description'],
                        short_description=product_data['description'][:100] + "...",
                        category=kids_category,
                        subcategory=subcategory,
                        brand=random.choice(brands),
                        gender='kids',
                        price=product_data['price'],
                        discount_price=product_data['discount'],
                        is_active=True,
                        is_featured=random.choice([True, False]),
                        stock_quantity=random.randint(20, 100),
                        sku=f"KIDS-{random.randint(10000, 99999)}"
                    )
                    print(f"Created: {product.name} in {subcategory_name}")
                else:
                    print(f"Already exists: {product_data['name']} in {subcategory_name}")
    
    # Create girls products
    for subcategory_name, products in girls_products.items():
        subcategory = SubCategory.objects.filter(category=kids_category, name=subcategory_name).first()
        if subcategory:
            for product_data in products:
                # Check if product already exists
                if not Product.objects.filter(name=product_data['name'], subcategory=subcategory).exists():
                    product = Product.objects.create(
                        name=product_data['name'],
                        slug=f"{product_data['name'].lower().replace(' ', '-').replace(',', '-')}-{random.randint(1000, 9999)}",
                        description=product_data['description'],
                        short_description=product_data['description'][:100] + "...",
                        category=kids_category,
                        subcategory=subcategory,
                        brand=random.choice(brands),
                        gender='kids',
                        price=product_data['price'],
                        discount_price=product_data['discount'],
                        is_active=True,
                        is_featured=random.choice([True, False]),
                        stock_quantity=random.randint(20, 100),
                        sku=f"KIDS-{random.randint(10000, 99999)}"
                    )
                    print(f"Created: {product.name} in {subcategory_name}")
                else:
                    print(f"Already exists: {product_data['name']} in {subcategory_name}")

if __name__ == "__main__":
    create_products()
    print("Kids products population completed!")
