from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product

@login_required
def products_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'main/products_page.html', {'products': products})

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

@login_required
def is_active_toggle_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot modify products.")
        return redirect('/')
    
    try:
        product = Product.objects.get(id=product_id, seller=request.user)
        product.is_active = not product.is_active
        product.save()
        status = "activated" if product.is_active else "deactivated"
        messages.success(request, f"Product {status} successfully.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found or you do not have permission to modify it.")
    
    return redirect('/dashboard/?section=product-management')

@login_required
def edit_product_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot edit products.")
        return redirect('/')
    
    product = Product.objects.filter(id=product_id, seller=request.user).first()
    
    if not product:
        messages.error(request, "Product not found or you do not have permission to edit it.")
        return redirect('/dashboard/?section=product-management')
    
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
        
        if battery_health == '' or battery_health is None:
            battery_health = None

        if errors:
            return render(request, 'main/edit_product_page.html', {'errors': errors, 'data': request.POST, 'product': product})

        product.title = title
        product.description = description
        product.brand = brand
        product.price = price
        product.category = category
        product.condition = condition
        product.battery_health = battery_health
        product.has_bill_or_warranty = has_bill_or_warranty
        product.has_original_box = has_original_box
        product.is_active = is_active
        
        if product_image:
            product.product_image = product_image
        
        product.save()
        
        messages.success(request, "Product updated successfully.")
        return redirect('/dashboard/?section=product-management')
    
    return render(request, 'main/edit_product_page.html', {'product': product})

@login_required
def delete_product_view(request, product_id):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot delete products.")
        return redirect('/')
    
    try:
        product = Product.objects.get(id=product_id, seller=request.user)
        product.delete()
        messages.success(request, "Product deleted successfully.")
    except Product.DoesNotExist:
        messages.error(request, "Product not found or you do not have permission to delete it.")
    
    return redirect('/dashboard/?section=product-management')