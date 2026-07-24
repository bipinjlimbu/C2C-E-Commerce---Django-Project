from django.shortcuts import render
from ..models import Product

def home_view(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    
    for product in products:
        product.is_in_wishlist = False
        if request.user.is_authenticated:
            product.is_in_wishlist = product.wishlist_set.filter(user=request.user).exists()
            
    return render(request, 'main/home_page.html', {'products': products})