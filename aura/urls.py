import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.csrf import ensure_csrf_cookie
from store.views import home_view
from accounts.views import signup_view, forgot_password_view

login_template_view = ensure_csrf_cookie(TemplateView.as_view(template_name='login.html'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('login/', login_template_view, name='login'),
    path('signup/', signup_view, name='signup_root'),
    path('forgot-password/', forgot_password_view, name='forgot_password_root'),
    path('home/', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('orders/', include('orders.urls')),
    path('delivery/', include('delivery.urls')),
    path('api/', include('store.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
elif os.environ.get('RENDER'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
