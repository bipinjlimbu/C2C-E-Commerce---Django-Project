from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Product, Order, Review

@login_required
def customer_dashboard_view(request):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot access the customer dashboard.")
        return redirect('/')
    
    section = request.GET.get('section', 'product-management')
    
    context = {
        'section': section,
        'active_count': Product.objects.filter(seller=request.user, is_active=True).count(),
    }
    
    if section == 'product-management':
        context['products'] = Product.objects.filter(seller=request.user).order_by('-created_at')
        
    elif section == 'pending-sales':
        context['pending_sales'] = Order.objects.filter(seller=request.user).exclude(status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
        
    elif section == 'pending-purchase':
        context['pending_purchase'] = Order.objects.filter(buyer=request.user).exclude(status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
        
    elif section == 'order-history':
        context['order_history'] = None
        
    elif section == 'purchase-history':
        context['purchase_history'] = None
        
    elif section == 'reviews-received':
        context['reviews_received'] = None
        
    elif section == 'reviews-provided':
        context['reviews_provided'] = None
        
    elif section == 'total-earning':
        context['total_earning'] = None
        
    elif section == 'total-spent':
        context['total_spent'] = None
        
    return render(request, 'dashboard/customer_dashboard.html', context)