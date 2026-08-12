import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Get beauty category and brands
beauty_category = Category.objects.get(slug='beauty')
brands = list(Brand.objects.all())

# Beauty makeup subcategories to create
makeup_subcategories = [
    {'name': 'Lakme Lipstick', 'slug': 'lakme-lipstick'},
    {'name': 'Maybelline Lipstick', 'slug': 'maybelline-lipstick'},
    {'name': 'Loreal Lipstick', 'slug': 'loreal-lipstick'},
    {'name': 'M.A.C Lipstick', 'slug': 'mac-lipstick'},
    {'name': 'Nykaa Lipstick', 'slug': 'nykaa-lipstick'},
    {'name': 'Forest Essentials Lipstick', 'slug': 'forest-essentials-lipstick'},
    {'name': 'Lip Gloss', 'slug': 'lip-gloss'},
    {'name': 'Lip Liner', 'slug': 'lip-liner'},
    {'name': 'Mascara', 'slug': 'mascara'},
    {'name': 'Eyeliner', 'slug': 'eyeliner'},
    {'name': 'Kajal', 'slug': 'kajal'},
    {'name': 'Eyeshadow', 'slug': 'eyeshadow'},
    {'name': 'Foundation', 'slug': 'foundation'},
    {'name': 'Primer', 'slug': 'primer'},
    {'name': 'Concealer', 'slug': 'concealer'},
    {'name': 'Compact', 'slug': 'compact'},
    {'name': 'Nail Polish', 'slug': 'nail-polish'}
]

# Product data for each subcategory
makeup_products = {
    'lakme-lipstick': [
        {'name': 'Lakme Absolute Matte Lipstick', 'price': 499, 'discount': 399, 'description': 'Intense matte finish lipstick with 16-hour wear. Rich color payoff.'},
        {'name': 'Lakme 9 to5 Lipstick', 'price': 399, 'discount': 299, 'description': 'Professional matte lipstick for all-day wear. Office perfect shades.'},
        {'name': 'Lakme Enrich Lipstick', 'price': 349, 'discount': 249, 'description': 'Moisturizing lipstick with vitamin E. Nourishing formula.'},
        {'name': 'Lakme Bold Color Lipstick', 'price': 449, 'discount': 349, 'description': 'Vibrant bold color lipstick. High impact shades for statement looks.'}
    ],
    'maybelline-lipstick': [
        {'name': 'Maybelline Color Sensational Lipstick', 'price': 449, 'discount': 349, 'description': 'Creamy lipstick with pure pigments. Smooth and comfortable wear.'},
        {'name': 'Maybelline Superstay Matte Ink Lipstick', 'price': 599, 'discount': 449, 'description': '16-hour matte liquid lipstick. Intense color that stays put.'},
        {'name': 'Maybelline Baby Lips Lipstick', 'price': 299, 'discount': 199, 'description': 'Nourishing lip balm with sheer color. Moisturizing formula.'},
        {'name': 'Maybelline Vivid Matte Lipstick', 'price': 399, 'discount': 299, 'description': 'Bright matte lipstick shades. Long-lasting vivid colors.'}
    ],
    'loreal-lipstick': [
        {'name': 'Loreal Color Riche Matte Lipstick', 'price': 599, 'discount': 449, 'description': 'Luxurious matte lipstick with intense color. Enriched with jojoba oil.'},
        {'name': 'Loreal Paris Signature Lipstick', 'price': 499, 'discount': 399, 'description': 'Classic lipstick with signature shades. Timeless elegance.'},
        {'name': 'Loreal Infallible Lipstick', 'price': 699, 'discount': 549, 'description': '24-hour wear lipstick. Unfadeable color and comfort.'},
        {'name': 'Loreal Color Riche Extraordinaire Lipstick', 'price': 799, 'discount': 649, 'description': 'Luxe liquid lipstick with gold shimmer. Premium formula.'}
    ],
    'mac-lipstick': [
        {'name': 'M.A.C Matte Lipstick', 'price': 899, 'discount': 699, 'description': 'Iconic MAC matte lipstick. Professional quality finish.'},
        {'name': 'M.A.C Satin Lipstick', 'price': 899, 'discount': 699, 'description': 'Semi-matte lipstick with medium coverage. Comfortable wear.'},
        {'name': 'M.A.C Cremesheen Lipstick', 'price': 899, 'discount': 699, 'description': 'Creamy lipstick with pearl finish. Luminous color.'},
        {'name': 'M.A.C Retro Matte Lipstick', 'price': 999, 'discount': 799, 'description': 'Modern matte lipstick. Bold and long-lasting color.'}
    ],
    'nykaa-lipstick': [
        {'name': 'Nykaa Matte Lipstick', 'price': 349, 'discount': 249, 'description': 'Affordable matte lipstick. Trendy shades for everyday wear.'},
        {'name': 'Nykaa Velvet Matte Lipstick', 'price': 399, 'discount': 299, 'description': 'Velvet matte finish lipstick. Smooth and luxurious.'},
        {'name': 'Nykaa Creamy Lipstick', 'price': 299, 'discount': 199, 'description': 'Creamy moisturizing lipstick. Comfortable all-day wear.'},
        {'name': 'Nykaa Bold Lipstick', 'price': 349, 'discount': 249, 'description': 'Statement bold lipstick shades. High impact colors.'}
    ],
    'forest-essentials-lipstick': [
        {'name': 'Forest Essentials Ayurvedic Lipstick', 'price': 599, 'discount': 449, 'description': 'Ayurvedic lipstick with herbal extracts. Natural and nourishing.'},
        {'name': 'Forest Essentials Organic Lipstick', 'price': 699, 'discount': 549, 'description': 'Organic lipstick with natural ingredients. Pure and gentle.'},
        {'name': 'Forest Essentials Velvet Lipstick', 'price': 649, 'discount': 499, 'description': 'Luxurious velvet finish lipstick. Rich and smooth.'},
        {'name': 'Forest Essentials Moisturizing Lipstick', 'price': 549, 'discount': 399, 'description': 'Deeply moisturizing lipstick with natural oils. Hydrating formula.'}
    ],
    'lip-gloss': [
        {'name': 'Shiny Lip Gloss', 'price': 349, 'discount': 249, 'description': 'High-shine lip gloss with vitamin E. Plumping effect.'},
        {'name': 'Tinted Lip Gloss', 'price': 399, 'discount': 299, 'description': 'Colored lip gloss with subtle color. Natural enhancement.'},
        {'name': 'Plumping Lip Gloss', 'price': 449, 'discount': 349, 'description': 'Volume-enhancing lip gloss. Fuller-looking lips.'},
        {'name': 'Long-Lasting Lip Gloss', 'price': 399, 'discount': 299, 'description': 'Extended wear lip gloss. Non-sticky formula.'}
    ],
    'lip-liner': [
        {'name': 'Precision Lip Liner', 'price': 299, 'discount': 199, 'description': 'Sharp precision lip liner. Perfect definition.'},
        {'name': 'Retractable Lip Liner', 'price': 349, 'discount': 249, 'description': 'Convenient retractable lip liner. No sharpening needed.'},
        {'name': 'Waterproof Lip Liner', 'price': 399, 'discount': 299, 'description': 'Long-lasting waterproof lip liner. Smudge-proof.'},
        {'name': 'Velvet Lip Liner', 'price': 349, 'discount': 249, 'description': 'Smooth velvet finish lip liner. Easy application.'}
    ],
    'mascara': [
        {'name': 'Volume Mascara', 'price': 499, 'discount': 399, 'description': 'Dramatic volume mascara. Thickens and lengthens lashes.'},
        {'name': 'Waterproof Mascara', 'price': 549, 'discount': 449, 'description': 'Smudge-proof waterproof mascara. All-day wear.'},
        {'name': 'Lengthening Mascara', 'price': 449, 'discount': 349, 'description': 'Lash-extending mascara formula. Natural-looking length.'},
        {'name': 'Curled Mascara', 'price': 499, 'discount': 399, 'description': 'Lash-curling mascara with brush. Lifts and separates.'}
    ],
    'eyeliner': [
        {'name': 'Liquid Eyeliner Pen', 'price': 399, 'discount': 299, 'description': 'Precision liquid eyeliner pen. Sharp winged lines.'},
        {'name': 'Gel Eyeliner', 'price': 449, 'discount': 349, 'description': 'Smooth gel eyeliner pot. Smudge-proof formula.'},
        {'name': 'Waterproof Eyeliner', 'price': 499, 'discount': 399, 'description': 'Long-lasting waterproof eyeliner. Sweat-proof.'},
        {'name': 'Kohl Eyeliner Pencil', 'price': 349, 'discount': 249, 'description': 'Soft kohl eyeliner pencil. Easy to blend.'}
    ],
    'kajal': [
        {'name': 'Traditional Kajal', 'price': 299, 'discount': 199, 'description': 'Classic traditional kajal. Intense black color.'},
        {'name': 'Waterproof Kajal', 'price': 399, 'discount': 299, 'description': 'Smudge-proof kajal. Long-lasting wear.'},
        {'name': 'Herbal Kajal', 'price': 349, 'discount': 249, 'description': 'Ayurvedic herbal kajal. Natural ingredients.'},
        {'name': 'Smudge Kajal', 'price': 349, 'discount': 249, 'description': 'Smudgy kajal pencil. Smoky eye effect.'}
    ],
    'eyeshadow': [
        {'name': 'Nude Eyeshadow Palette', 'price': 899, 'discount': 699, 'description': 'Versatile nude eyeshadow palette. Everyday essential shades.'},
        {'name': 'Smoky Eyeshadow Palette', 'price': 999, 'discount': 799, 'description': 'Dramatic smoky eyeshadow palette. Evening look essentials.'},
        {'name': 'Shimmer Eyeshadow Palette', 'price': 899, 'discount': 699, 'description': 'Glittering shimmer eyeshadow palette. Party-ready shades.'},
        {'name': 'Matte Eyeshadow Palette', 'price': 799, 'discount': 599, 'description': 'Professional matte eyeshadow palette. Sophisticated colors.'}
    ],
    'foundation': [
        {'name': 'Matte Foundation', 'price': 699, 'discount': 549, 'description': 'Oil-control matte foundation. Long-lasting coverage.'},
        {'name': 'Dewy Foundation', 'price': 749, 'discount': 599, 'description': 'Luminous dewy foundation. Radiant finish.'},
        {'name': 'Full Coverage Foundation', 'price': 899, 'discount': 699, 'description': 'High-coverage foundation. Flawless complexion.'},
        {'name': 'Lightweight Foundation', 'price': 649, 'discount': 499, 'description': 'Breathable lightweight foundation. Natural finish.'}
    ],
    'primer': [
        {'name': 'Face Primer', 'price': 599, 'discount': 449, 'description': 'Smoothing face primer. Pore-minimizing effect.'},
        {'name': 'Hydrating Primer', 'price': 649, 'discount': 499, 'description': 'Moisturizing primer with hyaluronic acid. Plumps skin.'},
        {'name': 'Silicone Primer', 'price': 699, 'discount': 549, 'description': 'Silky silicone primer. Creates smooth canvas.'},
        {'name': 'Illuminating Primer', 'price': 649, 'discount': 499, 'description': 'Radiant illuminating primer. Dewy glow effect.'}
    ],
    'concealer': [
        {'name': 'Full Coverage Concealer', 'price': 499, 'discount': 399, 'description': 'High-coverage concealer. Hides imperfections.'},
        {'name': 'Under Eye Concealer', 'price': 449, 'discount': 349, 'description': 'Brightening under-eye concealer. Reduces dark circles.'},
        {'name': 'Liquid Concealer', 'price': 399, 'discount': 299, 'description': 'Smooth liquid concealer. Easy to blend.'},
        {'name': 'Concealer Palette', 'price': 599, 'discount': 449, 'description': 'Multi-shade concealer palette. Customizable coverage.'}
    ],
    'compact': [
        {'name': 'Matte Compact Powder', 'price': 399, 'discount': 299, 'description': 'Oil-control matte compact. Shine-free finish.'},
        {'name': 'Translucent Compact Powder', 'price': 349, 'discount': 249, 'description': 'Invisible translucent powder. Natural finish.'},
        {'name': 'Pressed Powder Compact', 'price': 449, 'discount': 349, 'description': 'Portable pressed powder compact. Touch-up essential.'},
        {'name': 'Mineral Compact Powder', 'price': 499, 'discount': 399, 'description': 'Natural mineral compact powder. Skin-friendly formula.'}
    ],
    'nail-polish': [
        {'name': 'Classic Red Nail Polish', 'price': 199, 'discount': 149, 'description': 'Timeless classic red nail polish. Iconic shade.'},
        {'name': 'Nude Nail Polish', 'price': 179, 'discount': 129, 'description': 'Elegant nude nail polish. Natural-looking shades.'},
        {'name': 'Glitter Nail Polish', 'price': 229, 'discount': 179, 'description': 'Sparkling glitter nail polish. Party-ready shine.'},
        {'name': 'Matte Nail Polish', 'price': 199, 'discount': 149, 'description': 'Modern matte finish nail polish. Chic and sophisticated.'}
    ]
}

print("Creating Beauty makeup subcategories and products...")

# Create subcategories and products
for subcat_data in makeup_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=beauty_category,
        defaults={
            'name': subcat_name,
            'is_active': True
        }
    )
    
    if created:
        print(f"Created subcategory: {subcat_name}")
    else:
        print(f"Subcategory already exists: {subcat_name}")
    
    # Create products for this subcategory
    if subcat_slug in makeup_products:
        products_data = makeup_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('.', '').replace('&', 'and')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=beauty_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='female',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"BEAUTY-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nBeauty makeup population completed!")
