from django.urls import path
from .views.main_view import home_view
from .views.auth_view import register_view, login_view, logout_view
from .views.profile_view import profile_view, edit_profile_view, delete_profile_view
from .views.product_view import add_product_view, delete_product_view, edit_product_view, is_active_toggle_view, products_view, product_detail_view
from .views.payment_view import initiate_payment_view, payment_success_view, payment_failed_view
from .views.order_view import ship_order_view, deliver_order_view, order_complete_view, reject_order_view, cancel_order_view
from .views.wishlist_view import wishlist_toggle_view
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
    path('payment/success/', payment_success_view, name='payment_success'),
    path('payment/failed/', payment_failed_view, name='payment_failed'),
    path('order/ship/<int:order_id>/', ship_order_view, name='ship_order'),
    path('order/deliver/<int:order_id>/', deliver_order_view, name='deliver_order'),
    path('order/complete/<int:order_id>/', order_complete_view, name='order_complete'),
    path('order/cancel/<int:order_id>/', cancel_order_view, name='cancel_order'),
    path('order/reject/<int:order_id>/', reject_order_view, name='reject_order'),
    path('wishlist/toggle/<int:product_id>/', wishlist_toggle_view, name='wishlist_toggle'),
    path('dashboard/', customer_dashboard_view, name='customer_dashboard'),
]