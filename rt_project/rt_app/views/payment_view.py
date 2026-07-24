from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import User, Product, Order
import requests
import json
import hmac
import hashlib
import base64
import uuid

def initiate_payment_view(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        buyer_id = request.POST.get('buyer_id')
        payment_method = request.POST.get('payment_method')
        shipping_address = request.POST.get('shipping_address')
        
        if Order.objects.filter(buyer_id=buyer_id, product_id=product_id, status__in=[Order.Status.CONFIRMED, Order.Status.SHIPPING, Order.Status.DELIVERED]).exists():
            messages.error(request, "You have already placed an order for this product.")
            return redirect(f'/products/{product_id}/')
        
        try:
            product = Product.objects.get(id=product_id)
            buyer = User.objects.get(id=buyer_id)
            seller = User.objects.get(id=product.seller.id)
        except (Product.DoesNotExist, User.DoesNotExist):
            messages.error(request, "Invalid product or user details.")
            return redirect('home')
                    
        # --- CASH ON DELIVERY (COD) ---
        if payment_method != 'esewa':
            order = Order.objects.create(
                buyer=buyer,
                seller=seller,
                product=product,
                amount=product.price,
                transaction_id=str(uuid.uuid4()),
                status=Order.Status.CONFIRMED,
                shipping_address=shipping_address,
                payment_method=Order.PaymentMethod.COD
            )
            order.save()
            
            messages.success(request, "Order placed successfully. Please pay the seller upon delivery.")
            return redirect('/dashboard/?section=pending-purchase')
            
        # --- ESEWA PAYMENT INITIALIZATION ---
        total_amount = str(product.price)
        
        # eSewa v2 is extremely strict with decimal formatting for signature generation
        try:
            total_val = float(total_amount)
            if total_val.is_integer():
                total_amount = str(int(total_val))
            else:
                total_amount = "{:.2f}".format(total_val)
        except ValueError:
            messages.error(request, "Invalid product price format.")
            return redirect(f'/products/{product_id}/')

        transaction_uuid = str(uuid.uuid4())
        product_code = "EPAYTEST"
        secret_key = "8gBm/:&EnhH.1/q" # Sandbox secret key
        
        # PERSIST ORDER METADATA IN DJANGO SESSION
        # eSewa ignores custom form fields, so we save them locally tied to transaction_uuid
        request.session[f'pending_order_{transaction_uuid}'] = {
            'product_id': product_id,
            'buyer_id': buyer_id,
            'shipping_address': shipping_address
        }
        request.session.modified = True
        
        # HMAC-SHA256 Signature generation
        data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
        
        secret_key_bytes = secret_key.encode('utf-8')
        data_bytes = data_to_sign.encode('utf-8')
        hmac_sha256 = hmac.new(secret_key_bytes, data_bytes, hashlib.sha256).digest()
        
        signature = base64.b64encode(hmac_sha256).decode('utf-8')
        
        context = {
            'amount': total_amount,
            'transaction_uuid': transaction_uuid,
            'product_code': product_code,
            'signature': signature,
            'esewa_url': "https://rc-epay.esewa.com.np/api/epay/main/v2/form",
            'success_url': "http://127.0.0.1:8000/payment/success/",
            'failure_url': "http://127.0.0.1:8000/payment/failed/",
        }
        
        return render(request, 'main/esewa_redirect_page.html', context)
    
    # Fallback if GET request
    product_id = request.POST.get('product_id') or ''
    return redirect(f'/products/{product_id}/')


def payment_success_view(request):
    encoded_data = request.GET.get('data')
    if not encoded_data:
        messages.error(request, "No payment data received from eSewa.")
        return redirect('payment_failed')

    try:
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_data = json.loads(decoded_bytes.decode('utf-8'))
    except Exception as e:
        messages.error(request, "Failed to decode eSewa response payload.")
        return redirect('payment_failed')
    
    product_code = decoded_data.get('product_code', 'EPAYTEST')
    transaction_uuid = decoded_data.get('transaction_uuid')
    total_amount = decoded_data.get('total_amount')
    
    if not transaction_uuid or not total_amount:
        messages.error(request, "Missing essential payment verification keys.")
        return redirect('payment_failed')

    # RETRIEVE SAVED METADATA FROM SESSION
    session_key = f'pending_order_{transaction_uuid}'
    order_data = request.session.pop(session_key, None)
    
    if not order_data:
        messages.error(request, "Transaction session expired or invalid. Please check your orders.")
        return redirect('payment_failed')

    product_id = order_data.get('product_id')
    buyer_id = order_data.get('buyer_id')
    shipping_address = order_data.get('shipping_address', '')

    # ESEWA TRANSACTION VERIFICATION API CALL
    # Strictly pass only product_code, total_amount, and transaction_uuid
    verify_url = "https://rc-epay.esewa.com.np/api/epay/transaction/status/"
    params = {
        'product_code': product_code,
        'total_amount': total_amount,
        'transaction_uuid': transaction_uuid
    }
    
    try:
        response = requests.get(verify_url, params=params, timeout=10)
        response.raise_for_status()
        verification_status = response.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        messages.error(request, "Communication failure with eSewa servers.")
        return redirect('payment_failed')
    except Exception as e:
        messages.error(request, f"Verification request error: {str(e)}")
        return redirect('payment_failed')

    # CHECK VERIFICATION RESULT
    if verification_status.get('status') == "COMPLETE":
        try:
            product = Product.objects.get(id=product_id)
            buyer = User.objects.get(id=buyer_id)
            seller = User.objects.get(id=product.seller.id)
            
            # Create Order Record
            order = Order.objects.create(
                buyer=buyer,
                seller=seller,
                product=product,
                amount=product.price,
                transaction_id=transaction_uuid,
                status=Order.Status.CONFIRMED,
                shipping_address=shipping_address,
                payment_method=Order.PaymentMethod.ESEWA
            )
            order.save()
            
            messages.success(request, "Payment verified and order placed successfully.")
            return render(request, 'main/payment_success_page.html', {'order': order})
            
        except (Product.DoesNotExist, User.DoesNotExist):
            messages.error(request, "Payment verified, but product or user record was not found.")
            return redirect('payment_failed')

    else:
        messages.error(request, "Payment verification failed or transaction incomplete.")
        return redirect('payment_failed')


def payment_failed_view(request):
    messages.error(request, "Payment failed or was cancelled by user.")
    return render(request, 'main/payment_failed_page.html')