from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order

@login_required
def ship_order_view(request, order_id):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot mark orders as shipping.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id, seller=request.user)
        if order.status == Order.Status.CONFIRMED:
            order.status = Order.Status.SHIPPING
            order.save()
            messages.success(request, "Order has been marked as shipping.")
        else:
            messages.error(request, "Order cannot be marked as shipping in its current status.")
    except Order.DoesNotExist:
        messages.error(request, "Order not found or you do not have permission to update it.")
    
    return redirect('/dashboard/?section=pending-sales')

@login_required
def deliver_order_view(request, order_id):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot mark orders as delivered.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id, seller=request.user)
        if order.status == Order.Status.SHIPPING:
            order.status = Order.Status.DELIVERED
            order.save()
            messages.success(request, "Order has been marked as delivered.")
        else:
            messages.error(request, "Order cannot be marked as delivered in its current status.")
    except Order.DoesNotExist:
        messages.error(request, "Order not found or you do not have permission to update it.")
    
    return redirect('/dashboard/?section=pending-sales')

@login_required
def reject_order_view(request, order_id):
    if request.user.is_staff:
        messages.error(request, "Access denied. Staff members cannot reject orders.")
        return redirect('/')
    
    try:
        order = Order.objects.get(id=order_id, seller=request.user)
        if order.status == Order.Status.CONFIRMED:
            order.status = Order.Status.REJECTED
            order.save()
            messages.success(request, "Order has been rejected.")
        else:
            messages.error(request, "Order cannot be rejected in its current status.")
    except Order.DoesNotExist:
        messages.error(request, "Order not found or you do not have permission to update it.")
    
    return redirect('/dashboard/?section=sales-history')