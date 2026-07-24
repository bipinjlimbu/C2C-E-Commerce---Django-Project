from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Wishlist, Product

@login_required
def wishlist_toggle_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('products')

    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist.delete()
        messages.success(request, f"{product.title} has been removed from your wishlist.")
    else:
        messages.success(request, f"{product.title} has been added to your wishlist.")

    return redirect(f'/products/{product_id}/')