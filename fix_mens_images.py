#!/usr/bin/env python
import os
import django
import shutil
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

# Create media/products directory if it doesn't exist
media_products_dir = os.path.join('media', 'products')
if not os.path.exists(media_products_dir):
    os.makedirs(media_products_dir, exist_ok=True)

def get_appropriate_image_for_mens_product(product_name, subcategory_name):
    """Assign appropriate image based on men's product subcategory"""
    name_lower = product_name.lower()
    subcategory_lower = subcategory_name.lower() if subcategory_name else ""
    
    # T-Shirts
    if 't-shirt' in name_lower or subcategory_lower == 't-shirts':
        return 'temp_image_100.jpg'  # Plain t-shirt
    
    # Casual Shirts
    elif 'casual shirt' in name_lower or subcategory_lower == 'casual-shirts':
        return 'temp_image_101.jpg'  # Casual shirt
    
    # Formal Shirts
    elif 'formal shirt' in name_lower or subcategory_lower == 'formal-shirts':
        return 'temp_image_102.jpg'  # Formal shirt
    
    # Polo Shirts
    elif 'polo shirt' in name_lower or subcategory_lower == 'polo-shirts':
        return 'temp_image_103.jpg'  # Polo shirt
    
    # Sweatshirts
    elif 'sweatshirt' in name_lower or subcategory_lower == 'sweatshirts':
        return 'temp_image_104.jpg'  # Sweatshirt
    
    # Sweaters
    elif 'sweater' in name_lower or subcategory_lower == 'sweaters':
        return 'temp_image_105.jpg'  # Sweater
    
    # Jackets
    elif 'jacket' in name_lower and 'rain' not in name_lower or subcategory_lower == 'jackets':
        return 'temp_image_106.jpg'  # Regular jacket
    
    # Rain Jackets
    elif 'rain jacket' in name_lower or subcategory_lower == 'rain-jackets':
        return 'temp_image_107.jpg'  # Rain jacket
    
    # Blazers & Coats
    elif 'blazer' in name_lower or 'coat' in name_lower or subcategory_lower == 'blazers':
        return 'temp_image_108.jpg'  # Blazer
    
    # Suits
    elif 'suit' in name_lower or subcategory_lower == 'suits':
        return 'temp_image_109.jpg'  # Suit
    
    # Jeans
    elif 'jean' in name_lower or subcategory_lower == 'jeans':
        return 'temp_image_110.jpg'  # Jeans
    
    # Casual Trousers
    elif 'casual trouser' in name_lower or subcategory_lower == 'casual-trousers':
        return 'temp_image_111.jpg'  # Casual trousers
    
    # Formal Trousers
    elif 'formal trouser' in name_lower or subcategory_lower == 'formal-trousers':
        return 'temp_image_112.jpg'  # Formal trousers
    
    # Chinos
    elif 'chino' in name_lower or subcategory_lower == 'chinos':
        return 'temp_image_113.jpg'  # Chinos
    
    # Shorts
    elif 'short' in name_lower or subcategory_lower == 'shorts':
        return 'temp_image_114.jpg'  # Shorts
    
    # Track Pants & Joggers
    elif 'track pant' in name_lower or 'jogger' in name_lower or subcategory_lower == 'track-pants':
        return 'temp_image_115.jpg'  # Track pants
    
    # Cargo Pants
    elif 'cargo pant' in name_lower or subcategory_lower == 'cargo-pants':
        return 'temp_image_116.jpg'  # Cargo pants
    
    # Casual Shoes
    elif 'casual shoe' in name_lower or subcategory_lower == 'casual-shoes':
        return 'temp_image_117.jpg'  # Casual shoes
    
    # Sports Shoes
    elif 'sports shoe' in name_lower or subcategory_lower == 'sports-shoes':
        return 'temp_image_118.jpg'  # Sports shoes
    
    # Formal Shoes
    elif 'formal shoe' in name_lower or subcategory_lower == 'formal-shoes':
        return 'temp_image_119.jpg'  # Formal shoes
    
    # Sneakers
    elif 'sneaker' in name_lower or subcategory_lower == 'sneakers':
        return 'temp_image_120.jpg'  # Sneakers
    
    # Sandals & Floaters
    elif 'sandal' in name_lower or 'flip-flop' in name_lower or subcategory_lower in ['sandals', 'flip-flops']:
        return 'temp_image_121.jpg'  # Sandals
    
    # Socks
    elif 'sock' in name_lower or subcategory_lower == 'socks':
        return 'temp_image_122.jpg'  # Socks
    
    # Wallets
    elif 'wallet' in name_lower or subcategory_lower == 'wallets-accessories':
        return 'temp_image_123.jpg'  # Wallet
    
    # Belts
    elif 'belt' in name_lower or subcategory_lower == 'belts-accessories':
        return 'temp_image_124.jpg'  # Belt
    
    # Perfumes & Body Mists
    elif 'perfume' in name_lower or subcategory_lower == 'perfumes':
        return 'temp_image_125.jpg'  # Perfume
    
    # Trimmers
    elif 'trimmer' in name_lower or subcategory_lower == 'trimmers':
        return 'temp_image_126.jpg'  # Trimmer
    
    # Deodorants
    elif 'deodorant' in name_lower or subcategory_lower == 'deodorants':
        return 'temp_image_127.jpg'  # Deodorant
    
    # Ties
    elif 'tie' in name_lower or subcategory_lower == 'ties':
        return 'temp_image_128.jpg'  # Tie
    
    # Cufflinks & Pockets
    elif 'cufflink' in name_lower or subcategory_lower == 'cufflinks':
        return 'temp_image_129.jpg'  # Cufflinks
    
    # Caps & Hats
    elif 'cap' in name_lower or 'hat' in name_lower or subcategory_lower == 'caps-hats':
        return 'temp_image_130.jpg'  # Cap
    
    # Mufflers, Scarves & Gloves
    elif 'muffler' in name_lower or 'scarf' in name_lower or 'glove' in name_lower or subcategory_lower == 'mufflers':
        return 'temp_image_131.jpg'  # Winter accessories
    
    # Phone Cases
    elif 'phone case' in name_lower or subcategory_lower == 'phone-cases':
        return 'temp_image_132.jpg'  # Phone case
    
    # Rings & Wristwear
    elif 'ring' in name_lower or 'bracelet' in name_lower or subcategory_lower == 'rings-wristwear':
        return 'temp_image_133.jpg'  # Ring/Bracelet
    
    # Helmets
    elif 'helmet' in name_lower or subcategory_lower == 'helmets':
        return 'temp_image_134.jpg'  # Helmet
    
    # Hair Care (wax, oil)
    elif any(keyword in name_lower for keyword in ['hair wax', 'beard oil', 'hair wax']):
        return 'temp_image_135.jpg'  # Hair care product
    
    # Default
    else:
        return 'temp_image_136.jpg'  # Default men's product

print("=== Fixing Men's Product Images ===")
mens_products = Product.objects.filter(category__name='Men')

for product in mens_products:
    # Get appropriate image filename
    image_filename = get_appropriate_image_for_mens_product(product.name, product.subcategory.name if product.subcategory else "")
    source_path = os.path.join(os.getcwd(), image_filename)
    
    if os.path.exists(source_path):
        # Create unique filename for this product
        product_image_name = f"{product.slug}_{image_filename}"
        dest_path = os.path.join(media_products_dir, product_image_name)
        
        # Copy image to media folder
        shutil.copy2(source_path, dest_path)
        
        # Remove existing images for this product
        ProductImage.objects.filter(product=product).delete()
        
        # Create new product image record
        with open(dest_path, 'rb') as f:
            product_image = ProductImage.objects.create(
                product=product,
                image=File(f, name=product_image_name)
            )
        
        print(f"Product: {product.name}")
        print(f"  Subcategory: {product.subcategory.name if product.subcategory else 'None'}")
        print(f"  Assigned: {image_filename}")
        print("-" * 50)
    else:
        print(f"Image not found: {image_filename}")

print("=== Men's Product Images Fixed ===")
