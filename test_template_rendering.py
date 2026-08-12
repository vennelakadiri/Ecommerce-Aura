import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory, Category
from django.template import Context, Template
from django.test import RequestFactory
from store.views import products_view

# Create a mock request
factory = RequestFactory()
request = factory.get('/store/products/?category=kids&subcategory=party-wear')

# Get the view response
response = products_view(request)

# Check if response has context
if hasattr(response, 'context_data'):
    products = response.context_data['products']
    print(f"Products in context: {len(products)}")
    print("First 5 products:")
    for i, product in enumerate(products[:5]):
        print(f"  {i+1}. {product.name} (ID: {product.id})")
else:
    print("Response doesn't have context_data")
    print(f"Response type: {type(response)}")
    print(f"Response status: {response.status_code}")

# Let's also try to render a simple template with these products
simple_template = Template("""
{% for product in products %}
{{ product.name }}
{% endfor %}
""")

context = Context({'products': products})
rendered = simple_template.render(context)
print("\nTemplate rendering test:")
print(rendered[:200])  # First 200 characters
