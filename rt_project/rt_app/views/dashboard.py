from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from ..models import User, Product, Order

@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Only staff members can access the admin dashboard.")
        return redirect('/')
    
    section = request.GET.get('section', 'user-management')
    
    context = {
        'section': section,
        'active_count': Product.objects.filter(is_active=True).count(),
    }
    
    if section == 'user-management':
        context['users'] = User.objects.filter(is_staff=False).order_by('-date_joined')
        
    elif section == 'listed-products':
        context['products'] = Product.objects.all().order_by('-created_at')
        
    elif section == 'track-orders':
        context['orders'] = Order.objects.all().order_by('-created_at')
        
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot access the customer dashboard.")
        return redirect('/')
    
    section = request.GET.get('section', 'product-management')
    
    context = {
        'section': section,
        'active_count': Product.objects.filter(seller=request.user, is_active=True).count(),
        'total_earning_amount': Order.objects.filter(seller=request.user, status=Order.Status.COMPLETED).aggregate(total=models.Sum('amount'))['total'] or 0,
        'total_spent_amount': Order.objects.filter(buyer=request.user, status=Order.Status.COMPLETED).aggregate(total=models.Sum('amount'))['total'] or 0,
    }
    
    if section == 'product-management':
        context['products'] = Product.objects.filter(seller=request.user).order_by('-created_at')
        
    elif section == 'pending-sales':
        context['pending_sales'] = Order.objects.filter(seller=request.user).exclude(status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED, Order.Status.REJECTED]).order_by('-created_at')
        
    elif section == 'pending-purchase':
        context['pending_purchase'] = Order.objects.filter(buyer=request.user).exclude(status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED, Order.Status.REJECTED]).order_by('-created_at')
        
    elif section == 'sales-history':
        context['sales_history'] = Order.objects.filter(seller=request.user, status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED, Order.Status.REJECTED]).order_by('-created_at')
        
    elif section == 'purchase-history':
        context['purchase_history'] = Order.objects.filter(buyer=request.user, status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED, Order.Status.REJECTED]).order_by('-created_at')
        
    elif section == 'total-earning':
        context['total_earning'] = Order.objects.filter(seller=request.user, status=Order.Status.COMPLETED).order_by('-created_at')
        
    elif section == 'total-spent':
        context['total_spent'] = Order.objects.filter(buyer=request.user, status=Order.Status.COMPLETED).order_by('-created_at')
        
    return render(request, 'dashboard/customer_dashboard.html', context)