import os
import django
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category, Brand

# Get kids category and brands
kids_category = Category.objects.get(slug='kids')
brands = list(Brand.objects.all())

# Toys and games subcategories to create
toys_subcategories = [
    {'name': 'Learning & Development', 'slug': 'learning-toys'},
    {'name': 'Activity Toys', 'slug': 'activity-toys'},
    {'name': 'Soft Toys', 'slug': 'soft-toys'},
    {'name': 'Action Figure / Play set', 'slug': 'action-figure-play-set'}
]

# Product data for each subcategory
toys_products = {
    'learning-toys': [
        {'name': 'Kids ABC Learning Tablet', 'price': 1299, 'discount': 999, 'description': 'Interactive ABC learning tablet for kids. Features educational games and alphabet learning.'},
        {'name': 'Kids Math Puzzle Set', 'price': 899, 'discount': 699, 'description': 'Colorful math puzzle set for children. Helps develop counting and problem-solving skills.'},
        {'name': 'Kids Science Experiment Kit', 'price': 1599, 'discount': 1199, 'description': 'Fun science experiment kit for kids. Safe and educational experiments for young scientists.'},
        {'name': 'Kids Language Learning Flashcards', 'price': 699, 'discount': 499, 'description': 'Bilingual flashcards for language learning. Helps build vocabulary in multiple languages.'}
    ],
    'activity-toys': [
        {'name': 'Kids Building Blocks Set', 'price': 999, 'discount': 799, 'description': 'Colorful building blocks set for creative play. Develops motor skills and creativity.'},
        {'name': 'Kids Art & Craft Kit', 'price': 1199, 'discount': 899, 'description': 'Complete art and craft kit with supplies. Includes paints, brushes, and craft materials.'},
        {'name': 'Kids Musical Instrument Set', 'price': 1499, 'discount': 1099, 'description': 'Mini musical instrument set for kids. Includes keyboard, drum, and maracas for musical exploration.'},
        {'name': 'Kids Play Dough Activity Set', 'price': 799, 'discount': 599, 'description': 'Non-toxic play dough set with molds and tools. Safe and fun creative play material.'}
    ],
    'soft-toys': [
        {'name': 'Kids Teddy Bear Collection', 'price': 899, 'discount': 699, 'description': 'Soft and cuddly teddy bear collection. Different sizes and colors for comfort and companionship.'},
        {'name': 'Kids Plush Animal Set', 'price': 1199, 'discount': 899, 'description': 'Set of 4 plush animals including lion, elephant, giraffe, and monkey. Soft and huggable.'},
        {'name': 'Kids Character Soft Toys', 'price': 999, 'discount': 799, 'description': 'Popular character soft toys collection. Features favorite cartoon characters in plush form.'},
        {'name': 'Kids Interactive Soft Toy', 'price': 1399, 'discount': 999, 'description': 'Interactive soft toy with sounds and movements. Responds to touch and play.'}
    ],
    'action-figure-play-set': [
        {'name': 'Kids Superhero Action Figures', 'price': 1499, 'discount': 1099, 'description': 'Set of 4 superhero action figures with accessories. Perfect for imaginative play.'},
        {'name': 'Kids Castle Play Set', 'price': 1899, 'discount': 1399, 'description': 'Detailed castle play set with figures and accessories. Medieval theme for adventure play.'},
        {'name': 'Kids Space Explorer Play Set', 'price': 1699, 'discount': 1199, 'description': 'Space-themed play set with astronaut figures and rocket ship. Encourages STEM learning.'},
        {'name': 'Kids Dinosaur Play Set', 'price': 1299, 'discount': 999, 'description': 'Realistic dinosaur play set with multiple species. Educational and fun for young paleontologists.'}
    ]
}

print("Creating kids toys and games subcategories and products...")

# Create subcategories and products
for subcat_data in toys_subcategories:
    subcat_slug = subcat_data['slug']
    subcat_name = subcat_data['name']
    
    # Create subcategory if it doesn't exist
    subcat, created = SubCategory.objects.get_or_create(
        slug=subcat_slug,
        category=kids_category,
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
    if subcat_slug in toys_products:
        products_data = toys_products[subcat_slug]
        print(f"  Creating products for {subcat_name}:")
        
        for product_data in products_data:
            if not Product.objects.filter(name=product_data['name'], subcategory=subcat).exists():
                product = Product.objects.create(
                    name=product_data['name'],
                    slug=f"{product_data['name'].lower().replace(' ', '-').replace('&', 'and').replace('/', '-')}-{random.randint(1000, 9999)}",
                    description=product_data['description'],
                    short_description=product_data['description'][:100] + "...",
                    category=kids_category,
                    subcategory=subcat,
                    brand=random.choice(brands),
                    gender='kids',
                    price=product_data['price'],
                    discount_price=product_data['discount'],
                    is_active=True,
                    is_featured=random.choice([True, False]),
                    stock_quantity=random.randint(20, 100),
                    sku=f"KIDS-{subcat_slug.upper()}-{random.randint(10000, 99999)}"
                )
                print(f"    Created: {product.name} - ${product.discount_price} (was ${product.price})")
            else:
                print(f"    Already exists: {product_data['name']}")

print("\nKids toys and games population completed!")
