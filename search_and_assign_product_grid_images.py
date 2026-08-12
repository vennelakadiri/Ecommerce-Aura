import os
import sys
import django
import hashlib

sys.path.insert(0, r"c:\Users\kadirivennela\OneDrive\Miniproject")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage, Banner

# High-resolution Unsplash photo pools organized by product sub-types
IMAGE_POOLS = {
    # WATCHES & TIMEPIECES
    'watch': [
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30',
        'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9',
        'https://images.unsplash.com/photo-1524805444758-089113d48a6d',
        'https://images.unsplash.com/photo-1542496658-e33a6d0d50f6',
        'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1',
        'https://images.unsplash.com/photo-1533139502658-0198f920d8e8',
        'https://images.unsplash.com/photo-1526045612212-70caf35c14df',
    ],
    
    # WALLETS & PURSES
    'wallet': [
        'https://images.unsplash.com/photo-1590737051993-55b0c2c9e1c3',
        'https://images.unsplash.com/photo-1627123424574-724758594e93',
        'https://images.unsplash.com/photo-1553062407-98eeb64c6a62',
        'https://images.unsplash.com/photo-1606503830023-e29f032225ca',
    ],
    
    # BELTS
    'belt': [
        'https://images.unsplash.com/photo-1553062407-98eeb64c6a62',
        'https://images.unsplash.com/photo-1624222247344-550fb60583dc',
        'https://images.unsplash.com/photo-1585832770485-e68a5fcfad52',
    ],
    
    # SUNGLASSES
    'sunglasses': [
        'https://images.unsplash.com/photo-1473496169904-658ba7c44d8a',
        'https://images.unsplash.com/photo-1511499767150-a48a237f0083',
        'https://images.unsplash.com/photo-1572635196237-14b3f281503f',
        'https://images.unsplash.com/photo-1577803645773-f96470509666',
    ],
    
    # BAGS & HANDBAGS & BACKPACKS
    'bag': [
        'https://images.unsplash.com/photo-1584917865442-de89df76afd3',
        'https://images.unsplash.com/photo-1590874103328-eac38a683ce7',
        'https://images.unsplash.com/photo-1548036328-c9fa89d128fa',
        'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1',
        'https://images.unsplash.com/photo-1553062407-98eeb64c6a62',
    ],
    
    # FOOTWEAR (SNEAKERS, SHOES, HEELS, SANDALS)
    'footwear_sneakers': [
        'https://images.unsplash.com/photo-1549298916-b41d501d3772',
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff',
        'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a',
        'https://images.unsplash.com/photo-1560769629-975ec94e6a86',
        'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77',
    ],
    'footwear_heels': [
        'https://images.unsplash.com/photo-1543163521-1bf539c55dd2',
        'https://images.unsplash.com/photo-1596147250787-349f82631557',
        'https://images.unsplash.com/photo-1581101767113-1677fc2beaa8',
    ],
    'footwear_sandals': [
        'https://images.unsplash.com/photo-1603808033192-082d6919d3e1',
        'https://images.unsplash.com/photo-1562273138-f46be4ebdf33',
    ],
    
    # LAMPS & LIGHTING
    'lamp': [
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
        'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15',
        'https://images.unsplash.com/photo-1540932239986-30128078f3c5',
    ],
    
    # HOME DECOR & VASES & ART
    'homedecor': [
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96',
        'https://images.unsplash.com/photo-1581783342308-f792dbdd27c5',
        'https://images.unsplash.com/photo-1533158307587-50cd1c35e15',
        'https://images.unsplash.com/photo-1513519245088-0e12902e5a38',
    ],
    
    # CUSHIONS & BEDDING
    'bedding_cushion': [
        'https://images.unsplash.com/photo-1586023492125-27b2c045efd7',
        'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace',
        'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2',
    ],
    
    # KITCHEN & STORAGE
    'kitchen': [
        'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136',
        'https://images.unsplash.com/photo-1584622650111-993a426fbf0a',
        'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce',
    ],
    
    # TOYS
    'toy': [
        'https://images.unsplash.com/photo-1515488344751-661a8d1e8de1',
        'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088',
        'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1',
    ],
    
    # PAJAMAS & SLEEPWEAR
    'pajama': [
        'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea',
        'https://images.unsplash.com/photo-1523381210434-271e8be1f52b',
        'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786',
    ],
    
    # JACKETS, COATS, BLAZERS & SWEATERS
    'outerwear': [
        'https://images.unsplash.com/photo-1551028719-00167b16eac5',
        'https://images.unsplash.com/photo-1544923246-77307dd654cb',
        'https://images.unsplash.com/photo-1548883354-7622d03aca27',
        'https://images.unsplash.com/photo-1591047139829-d91aecb6caea',
    ],
    
    # DRESSES, SKIRTS & ETHNIC SUITS
    'dress_skirt': [
        'https://images.unsplash.com/photo-1515372039744-b28f8a3ed786',
        'https://images.unsplash.com/photo-1539109136881-3be0616acf4b',
        'https://images.unsplash.com/photo-1496747611176-843222e1e57c',
        'https://images.unsplash.com/photo-1572804013309-59a88b7e92c1',
        'https://images.unsplash.com/photo-1617137968427-85924c800a22',
    ],
    
    # JEANS, PANTS, TROUSERS, SHORTS & LEGGINGS
    'bottoms': [
        'https://images.unsplash.com/photo-1542272617-08f086302d36',
        'https://images.unsplash.com/photo-1541099649105-f69ad21f3246',
        'https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec',
        'https://images.unsplash.com/photo-1506629082925-2368c7f76df1',
    ],
    
    # SHIRTS, T-SHIRTS & TOPS
    'tops_shirts': [
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab',
        'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a',
        'https://images.unsplash.com/photo-1576566588028-4147f3842f27',
        'https://images.unsplash.com/photo-1618354691373-d851c5c3a990',
        'https://images.unsplash.com/photo-1562157873-818bc0726f68',
    ],
    
    # TIES & SCARVES & HATS
    'accessories_fashion': [
        'https://images.unsplash.com/photo-1520903920243-00d872a2d1c9',
        'https://images.unsplash.com/photo-1588850561407-ed78c282e89b',
        'https://images.unsplash.com/photo-1583744983541-9a548a6af254',
    ],
    
    # COSMETICS & LIPSTICK
    'lipstick': [
        'https://images.unsplash.com/photo-1586495777744-4413f21062fa',
        'https://images.unsplash.com/photo-1596462502278-27bfdc403348',
        'https://images.unsplash.com/photo-1625093742435-6fa192b6fb10',
    ],
    
    # NAIL POLISH
    'nailpolish': [
        'https://images.unsplash.com/photo-1610990837682-c590686d7015',
        'https://images.unsplash.com/photo-1604654894610-df63bc536371',
    ],
    
    # PERFUMES
    'perfume': [
        'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539',
        'https://images.unsplash.com/photo-1541643600914-78b084683601',
        'https://images.unsplash.com/photo-1523293182086-7651a899d37f',
    ],
    
    # HAIRCARE & SHAMPOO
    'haircare': [
        'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e',
        'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d',
        'https://images.unsplash.com/photo-1608248597379-e075e7144e51',
    ],
    
    # SKINCARE & CREAMS & OILS & WAX
    'skincare': [
        'https://images.unsplash.com/photo-1556228724-3a12d6e4e0e3',
        'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881',
        'https://images.unsplash.com/photo-1608248597379-e075e7144e51',
        'https://images.unsplash.com/photo-1567928269937-ae146e45b428',
    ],
    
    # JEWELRY & RINGS & NECKLACES
    'jewelry': [
        'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338',
        'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f',
        'https://images.unsplash.com/photo-1605100804763-247f67b3557e',
        'https://images.unsplash.com/photo-1603561591411-07134e71a2a9',
    ],
    
    # GENERAL FASHION
    'general_fashion': [
        'https://images.unsplash.com/photo-1483985988355-763728e1935b',
        'https://images.unsplash.com/photo-1441986300917-64674bd600d8',
        'https://images.unsplash.com/photo-1490481651871-ab68de25d43d',
    ]
}

def determine_pool_key(product):
    name = product.name.lower()
    cat = product.category.name.lower()
    subcategory = product.subcategory.name.lower() if product.subcategory else ''
    brand = product.brand.name.lower()
    
    combined = f"{name} {cat} {subcategory} {brand}"
    
    if any(w in combined for w in ['watch', 'smartwatch', 'timepiece']):
        return 'watch'
    elif any(w in combined for w in ['wallet', 'card holder', 'purse']):
        return 'wallet'
    elif any(w in combined for w in ['belt', 'leather belt']):
        return 'belt'
    elif any(w in combined for w in ['sunglass', 'spectacles', 'eyewear', 'shades']):
        return 'sunglasses'
    elif any(w in combined for w in ['handbag', 'tote', 'clutch', 'bag', 'backpack', 'satchel']):
        return 'bag'
    elif any(w in combined for w in ['heel', 'stiletto', 'pump']):
        return 'footwear_heels'
    elif any(w in combined for w in ['sandal', 'flip flop', 'slipper']):
        return 'footwear_sandals'
    elif any(w in combined for w in ['boot', 'sneaker', 'shoe', 'footwear', 'flat', 'loafer']):
        return 'footwear_sneakers'
    elif any(w in combined for w in ['lamp', 'lighting', 'light']):
        return 'lamp'
    elif any(w in combined for w in ['vase', 'decor', 'art', 'wall art', 'showpiece']):
        return 'homedecor'
    elif any(w in combined for w in ['cushion', 'pillow', 'bedding', 'blanket', 'sheet', 'towel']):
        return 'bedding_cushion'
    elif any(w in combined for w in ['kitchen', 'storage', 'container', 'jar', 'cookware']):
        return 'kitchen'
    elif any(w in combined for w in ['toy', 'doll', 'game', 'play']):
        return 'toy'
    elif any(w in combined for w in ['pajama', 'nightwear', 'sleepwear']):
        return 'pajama'
    elif any(w in combined for w in ['jacket', 'coat', 'blazer', 'sweater', 'sweatshirt', 'hoodie', 'suit', 'sherwani']):
        return 'outerwear'
    elif any(w in combined for w in ['skirt', 'dress', 'gown', 'frock', 'kurti', 'saree', 'lehenga', 'salwar']):
        return 'dress_skirt'
    elif any(w in combined for w in ['jeans', 'pant', 'trouser', 'legging', 'short', 'track', 'jogger', 'yoga', 'dhoti']):
        return 'bottoms'
    elif any(w in combined for w in ['tshirt', 't-shirt', 'shirt', 'top', 'blouse', 'polos', 'polo', 'vest', 'kurta', 'uniform']):
        return 'tops_shirts'
    elif any(w in combined for w in ['tie', 'scarf', 'glove', 'cap', 'hat']):
        return 'accessories_fashion'
    elif any(w in combined for w in ['lipstick', 'lip', 'gloss', 'balm']):
        return 'lipstick'
    elif any(w in combined for w in ['nail', 'polish', 'manicure']):
        return 'nailpolish'
    elif any(w in combined for w in ['perfume', 'fragrance', 'cologne', 'mist', 'deodorant']):
        return 'perfume'
    elif any(w in combined for w in ['shampoo', 'conditioner', 'hair', 'haircare', 'hair wax']):
        return 'haircare'
    elif any(w in combined for w in ['ring', 'necklace', 'bracelet', 'earring', 'jewellery', 'jewelry']):
        return 'jewelry'
    elif any(w in combined for w in ['cream', 'moisturizer', 'lotion', 'skincare', 'face wash', 'scrub', 'mask', 'cleanser', 'oil', 'fluid', 'beard oil', 'body butter', 'soap']):
        return 'skincare'
    elif any(w in combined for w in ['makeup', 'palette', 'foundation', 'compact', 'concealer']):
        return 'lipstick'
    else:
        return 'general_fashion'

def generate_relevant_product_image_url(product):
    pool_key = determine_pool_key(product)
    urls = IMAGE_POOLS.get(pool_key, IMAGE_POOLS['general_fashion'])
    
    # Pick deterministic image from pool based on hash of product.name + product.id
    unique_str = f"{product.id}_{product.name}_{product.category.name}"
    h = int(hashlib.md5(unique_str.encode('utf-8')).hexdigest(), 16)
    selected_base_url = urls[h % len(urls)]
    
    # Format with parameters for crisp 500x500 crop and unique seed parameter
    full_url = f"{selected_base_url}?w=500&h=500&fit=crop&q=80&v={h % 10000}"
    return full_url

def update_all_product_grids():
    print("=" * 60)
    print("STARTING PRODUCT GRID IMAGE UPDATE FOR CUSTOMER SIDE")
    print("Note: Banner table will be 100% UNTOUCHED.")
    print("=" * 60)
    
    products = Product.objects.all()
    total = products.count()
    print(f"Total product grid items to process: {total}")
    
    updated_count = 0
    for idx, product in enumerate(products, 1):
        image_url = generate_relevant_product_image_url(product)
        
        # Get or create primary ProductImage for this product
        img_obj, created = ProductImage.objects.get_or_create(
            product=product,
            defaults={'image': image_url, 'alt_text': product.name, 'is_primary': True}
        )
        if not created:
            img_obj.image = image_url
            img_obj.alt_text = product.name
            img_obj.is_primary = True
            img_obj.save()
            
        updated_count += 1
        if idx % 100 == 0 or idx == total:
            print(f"Progress: [{idx}/{total}] products updated with relevant image URLs.")
            
    print("=" * 60)
    print(f"SUCCESSFULLY UPDATED {updated_count} PRODUCT GRID IMAGES.")
    
    # Verification: Check banner count and ensure untouched
    banners = Banner.objects.all()
    print(f"Verified Banners count: {banners.count()} (UNTOUCHED)")
    for b in banners:
        print(f"  Banner {b.id}: {b.title} -> {b.image}")
    print("=" * 60)

if __name__ == '__main__':
    update_all_product_grids()
