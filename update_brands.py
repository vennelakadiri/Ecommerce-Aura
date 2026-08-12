#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

# Brand data with correct names and image URLs
brands_data = [
    {
        'name': "Levi's",
        'slug': 'levis',
        'image_url': 'https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg'
    },
    {
        'name': 'Puma',
        'slug': 'puma',
        'image_url': 'https://i.pinimg.com/736x/e0/3b/fd/e03bfd40f39a5525c4594567ae9966ad.jpg'
    },
    {
        'name': 'H&M',
        'slug': 'hm',
        'image_url': 'https://mir-s3-cdn-cf.behance.net/project_modules/1400/85eed532794677.5694280b8e5fc.jpg'
    },
    {
        'name': 'Zara',
        'slug': 'zara',
        'image_url': 'https://folletoss.pe/wp-content/uploads/2023/06/zara34-min.jpg'
    },
    {
        'name': 'Nike',
        'slug': 'nike',
        'image_url': 'https://img.freepik.com/premium-photo/nike-brand-integration-seamlessly-blend-brand-elements-website-design_1036975-155492.jpg'
    },
    {
        'name': 'Tanishq',
        'slug': 'tanishq',
        'image_url': 'https://staticimg.tanishq.co.in/microsite/gold-exchange/images/banner/goldex-m2-new.jpg'
    },
    {
        'name': 'Biba',
        'slug': 'biba',
        'image_url': 'https://cms.landmarkshops.in/cdn-cgi/image/w=288,q=85,fit=cover/LS-Fest/LS-new/PC-2-Desktop-Women-21Apr25.jpg'
    },
    {
        'name': 'Jack & Jones',
        'slug': 'jack-jones',
        'image_url': 'https://cdn.shopify.com/s/files/1/2225/5907/files/WEB_PLP_Cards_SALE_5.jpg?v=1672748223&width=533'
    },
    {
        'name': 'USPA',
        'slug': 'uspa',
        'image_url': 'https://uspoloassn.in/cdn/shop/files/WOMEN_CURATION_BOX_01__1_1.jpg?v=1721925598'
    },
    {
        'name': 'Tommy',
        'slug': 'tommy',
        'image_url': 'https://marketplace.canva.com/EAE7HESRmfM/1/0/1131w/canva-dark-gray-modern-woman-fashion-magazine-covers-iyGKr401TZI.jpg'
    },
    {
        'name': 'ONLY',
        'slug': 'only',
        'image_url': 'https://gapinc-prod-a6bndyfubmc5d9ey.z03.azurefd.net/gapmedia/gapcorporatesite/media/images/about/gap/untitled-17.png'
    },
    {
        'name': 'Allen Solly',
        'slug': 'allen-solly',
        'image_url': 'https://theenterpriseworld.com/wp-content/uploads/2026/01/2.-Not-Just-Fashion-But-a-Lifestyle-Statement-in.pinterest.com_.jpg'
    },
    {
        'name': 'Vero Moda',
        'slug': 'vero-moda',
        'image_url': 'https://images.veromoda.com/media/s5jkcayx/row07_04_curve.jpg?v=d4502597-22e5-4fe9-a6b1-2f977643f51d&format=webp&width=512&quality=80&key=1-4-3&bg-color=F5F5F5'
    },
    {
        'name': 'Steve madden',
        'slug': 'steve-madden',
        'image_url': 'https://i.pinimg.com/736x/b7/7f/5d/b77f5dbb4f5a74dbb7a99cb0a14374b0.jpg'
    },
    {
        'name': 'Skechers',
        'slug': 'skechers',
        'image_url': 'https://img.freepik.com/premium-vector/special-shoes-collection-social-media-facebook-cover-post-template_293893-55.jpg?w=2000'
    },
    {
        'name': 'Van Heusen',
        'slug': 'van-heusen',
        'image_url': 'https://www.vanheusen.com.au/media/wysiwyg/VH/2021/710x780_VH_Suits.jpg'
    }
]

print("Updating brands...")
for brand_data in brands_data:
    brand, created = Brand.objects.update_or_create(
        slug=brand_data['slug'],
        defaults={
            'name': brand_data['name'],
            'description': f'{brand_data["name"]} brand',
            'is_active': True
        }
    )
    
    # Update image if URL is provided
    if brand_data['image_url']:
        import requests
        from django.core.files.base import ContentFile
        from io import BytesIO
        
        try:
            response = requests.get(brand_data['image_url'])
            if response.status_code == 200:
                # Get filename from URL
                filename = f"{brand_data['slug']}_brand.jpg"
                brand.logo.save(filename, ContentFile(response.content))
                brand.save()
                print(f"Updated {brand_data['name']} brand with new image")
            else:
                print(f"Failed to download image for {brand_data['name']}")
        except Exception as e:
            print(f"Error updating {brand_data['name']}: {e}")
    
    print(f"{'Created' if created else 'Updated'}: {brand.name} ({brand.slug})")

print("\nCurrent brands in database:")
for brand in Brand.objects.filter(is_active=True):
    print(f"- {brand.name} ({brand.slug}) - Logo: {'Yes' if brand.logo else 'No'}")
