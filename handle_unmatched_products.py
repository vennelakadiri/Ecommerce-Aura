import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def get_relevant_image_url(product_name, category_name):
    """
    Get a relevant image URL for unmatched products using more specific queries.
    """
    from urllib.parse import quote
    
    product_lower = product_name.lower()
    category_lower = category_name.lower()
    
    # More specific image mapping based on product keywords
    if 'shirt' in product_lower:
        if 'formal' in product_lower:
            return f"https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=400&fit=crop"
        elif 'casual' in product_lower:
            return f"https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop"
        elif 'polo' in product_lower:
            return f"https://images.unsplash.com/photo-1625910513413-5fc45e99f3c7?w=400&h=400&fit=crop"
        elif 't-shirt' in product_lower or 'tshirt' in product_lower:
            return f"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop"
        else:
            return f"https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=400&h=400&fit=crop"
    
    elif 'pants' in product_lower or 'jeans' in product_lower or 'trousers' in product_lower:
        if 'jeans' in product_lower:
            return f"https://images.unsplash.com/photo-1542272617-08f086302d36?w=400&h=400&fit=crop"
        elif 'chinos' in product_lower:
            return f"https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400&h=400&fit=crop"
        elif 'cargo' in product_lower:
            return f"https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400&h=400&fit=crop"
        elif 'track' in product_lower:
            return f"https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=400&h=400&fit=crop"
        else:
            return f"https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&h=400&fit=crop"
    
    elif 'dress' in product_lower:
        if 'floral' in product_lower:
            return f"https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=400&fit=crop"
        elif 'cocktail' in product_lower or 'party' in product_lower:
            return f"https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop"
        elif 'summer' in product_lower:
            return f"https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=400&h=400&fit=crop"
        else:
            return f"https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=400&fit=crop"
    
    elif 'jacket' in product_lower or 'coat' in product_lower or 'blazer' in product_lower:
        if 'denim' in product_lower:
            return f"https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop"
        elif 'winter' in product_lower:
            return f"https://images.unsplash.com/photo-1544966500-38a8c6c8a6f8?w=400&h=400&fit=crop"
        else:
            return f"https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop"
    
    elif 'shoes' in product_lower or 'footwear' in product_lower or 'sneakers' in product_lower:
        if 'sports' in product_lower or 'running' in product_lower:
            return f"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"
        elif 'formal' in product_lower:
            return f"https://images.unsplash.com/photo-1614252369475-531eba835eb1?w=400&h=400&fit=crop"
        else:
            return f"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"
    
    elif 'watch' in product_lower:
        return f"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop"
    
    elif 'bag' in product_lower or 'handbag' in product_lower or 'purse' in product_lower:
        return f"https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop"
    
    elif 'sunglasses' in product_lower:
        return f"https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop"
    
    elif 'wallet' in product_lower:
        return f"https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop"
    
    elif 'scarf' in product_lower:
        return f"https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=400&h=400&fit=crop"
    
    elif 'hat' in product_lower or 'cap' in product_lower:
        return f"https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop"
    
    elif 'sweater' in product_lower:
        return f"https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400&h=400&fit=crop"
    
    elif 'hoodie' in product_lower or 'sweatshirt' in product_lower:
        return f"https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop"
    
    elif 'skirt' in product_lower:
        return f"https://images.unsplash.com/photo-1583496661160-fb5886a0uj5a?w=400&h=400&fit=crop"
    
    elif 'kurta' in product_lower or 'sherwani' in product_lower or 'ethnic' in product_lower:
        return f"https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400&h=400&fit=crop"
    
    elif 'shorts' in product_lower:
        return f"https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop"
    
    # Category-based fallback
    category_images = {
        'Men': f"https://images.unsplash.com/photo-1617137968427-85924c800a22?w=400&h=400&fit=crop",
        'Women': f"https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?w=400&h=400&fit=crop",
        'Kids': f"https://images.unsplash.com/photo-1503939578260-a5e492191f5c?w=400&h=400&fit=crop",
        'Home': f"https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=400&fit=crop",
        'Beauty': f"https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop",
        'Accessories': f"https://images.unsplash.com/photo-1523170335258-5ed11844a49?w=400&h=400&fit=crop",
    }
    
    return category_images.get(category_name, category_images.get('Men'))

def handle_unmatched_products():
    """
    Handle unmatched products with relevant image URLs.
    """
    products = Product.objects.all()
    unmatched_products = []
    
    # Find products without proper image mappings
    for product in products:
        images = product.images.all()
        if not images.exists() or '/media/products/' not in images.first().image:
            unmatched_products.append(product)
    
    total_unmatched = len(unmatched_products)
    print(f"Found {total_unmatched} unmatched products")
    print("=" * 60)
    
    updated_count = 0
    
    for index, product in enumerate(unmatched_products, 1):
        print(f"\n[{index}/{total_unmatched}] Processing: {product.name}")
        print(f"  Category: {product.category.name}")
        
        try:
            # Get relevant image URL
            image_url = get_relevant_image_url(product.name, product.category.name)
            
            # Get existing images
            existing_images = product.images.all()
            
            if existing_images.exists():
                # Update existing images
                for img in existing_images:
                    img.image = image_url
                    img.alt_text = f"{product.name} - {product.category.name}"
                    img.save()
                print(f"  ✓ Updated {existing_images.count()} existing image(s)")
            else:
                # Create new image
                ProductImage.objects.create(
                    product=product,
                    image=image_url,
                    is_primary=True,
                    alt_text=f"{product.name} - {product.category.name}"
                )
                print(f"  ✓ Created new image")
            
            updated_count += 1
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
        
        # Progress indicator
        if index % 50 == 0:
            print(f"\n--- Progress: {index}/{total_unmatched} ---")
            print(f"Updated: {updated_count}")
    
    print("\n" + "=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)
    print(f"Total unmatched: {total_unmatched}")
    print(f"Updated: {updated_count}")
    print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("HANDLE UNMATCHED PRODUCTS")
    print("=" * 60)
    print("This script will update unmatched products with")
    print("relevant image URLs based on product keywords.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        handle_unmatched_products()
    else:
        print("Operation cancelled.")
