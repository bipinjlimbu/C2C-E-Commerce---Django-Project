from django.urls import path
from .views.main_view import home_view
from .views.auth_view import register_view, login_view, logout_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.product_view import add_product_view, is_active_toggle_view
from .views.dashboard import customer_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/<int:user_id>/', delete_profile_view, name='delete_profile'),
    path('products/add/', add_product_view, name='add_product'),
    path('products/status/toggle/<int:product_id>/', is_active_toggle_view, name='toggle_product_active'),
    path('dashboard/', customer_dashboard_view, name='customer_dashboard'),
]