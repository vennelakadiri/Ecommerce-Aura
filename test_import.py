#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

try:
    from store.models import CustomerProfile
    print("✅ CustomerProfile imported successfully")
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Checking available models in store.models:")
    import store.models
    import inspect
    for name, obj in inspect.getmembers(store.models):
        if inspect.isclass(obj):
            print(f"  - {name}")
