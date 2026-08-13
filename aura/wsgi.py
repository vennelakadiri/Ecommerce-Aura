import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')

application = get_wsgi_application()

if os.environ.get('RENDER'):
    from aura.bootstrap import bootstrap_render_database

    bootstrap_render_database()
