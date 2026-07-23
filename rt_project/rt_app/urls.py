from django.urls import path
from .views.main_view import home_view
from .views.auth_view import register_view, login_view, logout_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.product_view import add_product_view, delete_product_view, edit_product_view, is_active_toggle_view, products_view, product_detail_view
from .views.payment_view import initiate_payment_view
from .views.dashboard import customer_dashboard_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/<int:user_id>/', delete_profile_view, name='delete_profile'),
    path('products/', products_view, name='products'),
    path('products/add/', add_product_view, name='add_product'),
    path('products/edit/<int:product_id>/', edit_product_view, name='edit_product'),
    path('products/delete/<int:product_id>/', delete_product_view, name='delete_product'),
    path('products/status/toggle/<int:product_id>/', is_active_toggle_view, name='toggle_product_active'),
    path('products/<int:product_id>/', product_detail_view, name='product_detail'),
    path('payment/initiate/', initiate_payment_view, name='initiate_payment'),
    path('dashboard/', customer_dashboard_view, name='customer_dashboard'),
]