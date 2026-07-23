from django.urls import path
from .views.main_view import home_view
from .views.auth_view import login_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
]