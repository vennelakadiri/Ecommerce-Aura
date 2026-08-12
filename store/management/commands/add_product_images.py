from django.core.management.base import BaseCommand
from store.models import Product, ProductImage
from django.core.files.base import ContentFile
import random
import urllib.request

class Command(BaseCommand):
    help = 'Add default images to products that have no images'

    def handle(self, *args, **options):
        self.stdout.write('Adding images to products without images...')
        
        # Kids wear image URLs - using placeholder images that are appropriate for kids clothing
        kids_image_urls = [
            'https://picsum.photos/seed/kidswear1/400/400.jpg',  # Kids wear placeholder 1
            'https://picsum.photos/seed/kidswear2/400/400.jpg',  # Kids wear placeholder 2
            'https://picsum.photos/seed/kidswear3/400/400.jpg',  # Kids wear placeholder 3
            'https://picsum.photos/seed/kidswear4/400/400.jpg',  # Kids wear placeholder 4
            'https://picsum.photos/seed/kidswear5/400/400.jpg',  # Kids wear placeholder 5
            'https://picsum.photos/seed/kidswear6/400/400.jpg',  # Kids wear placeholder 6
            'https://picsum.photos/seed/kidswear7/400/400.jpg',  # Kids wear placeholder 7
            'https://picsum.photos/seed/kidswear8/400/400.jpg',  # Kids wear placeholder 8
        ]
        
        # Get all products without images
        products_without_images = Product.objects.filter(images__isnull=True).order_by('-created_at')
        
        if not products_without_images.exists():
            self.stdout.write(self.style.WARNING('No products without images found.'))
            return
        
        self.stdout.write(f'Found {products_without_images.count()} products without images.')
        
        for product in products_without_images:
            try:
                # Select a random image URL
                image_url = random.choice(kids_image_urls)
                
                # Download image using urllib
                urllib.request.urlretrieve(image_url, f"temp_image_{product.id}.jpg")
                
                # Read the downloaded image
                with open(f"temp_image_{product.id}.jpg", 'rb') as f:
                    image_content = f.read()
                
                # Create image filename
                filename = f"{product.slug}_{random.randint(1000, 9999)}.jpg"
                
                # Save image
                product_image = ProductImage.objects.create(
                    product=product,
                    is_primary=True,
                    alt_text=f"{product.name} - Default image"
                )
                
                # Save image content
                product_image.image.save(filename, ContentFile(image_content), save=True)
                
                self.stdout.write(f'Added image to: {product.name}')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to add image to {product.name}: {str(e)}'))
                # Continue with next product
                continue
        
        self.stdout.write(self.style.SUCCESS('Successfully added images to products!'))
