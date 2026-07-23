from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product

@login_required
def add_product_view(request):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot add products.")
        return redirect('/')
    
    errors = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        battery_health = request.POST.get('battery_health')
        has_bill_or_warranty = request.POST.get('has_bill_or_warranty') == 'true'
        has_original_box = request.POST.get('has_original_box') == 'true'
        is_active = request.POST.get('is_active') == 'true'
        product_image = request.FILES.get('product_image')
        
        if not title:
            errors['title'] = "Title is required."
        if not description:
            errors['description'] = "Description is required."
        if not brand:
            errors['brand'] = "Brand is required."
        if not price:
            errors['price'] = "Price is required."
        if not category:
            errors['category'] = "Category is required."
        if not condition:
            errors['condition'] = "Condition is required."
        if not product_image:
            errors['product_image'] = "Product image is required."
        if battery_health == '' or battery_health is None:
            battery_health = None
            
        if errors:
            return render(request, 'main/add_product_page.html', {'errors': errors, 'data': request.POST})
        
        product = Product.objects.create(
            seller=request.user,
            title=title,
            description=description,
            brand=brand,
            price=price,
            category=category,
            condition=condition,
            battery_health=battery_health,
            has_bill_or_warranty=has_bill_or_warranty,
            has_original_box=has_original_box,
            is_active=is_active,
            product_image=product_image
        )
        product.save()
        messages.success(request, "Product added successfully.")
        return redirect('/dashboard/?section=product-management')
        
    return render(request, 'main/add_product_page.html')