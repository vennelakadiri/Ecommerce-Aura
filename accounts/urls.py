from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='api_login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('subscription/', views.subscription_management, name='subscription_management'),
    path('analytics/', views.dashboard_analytics, name='dashboard_analytics'),
    path('notifications/', views.notifications_management, name='notifications_management'),
    path('reports/', views.reports_management, name='reports_management'),
    path('advertisements/', views.advertisements_management, name='advertisements_management'),
]
