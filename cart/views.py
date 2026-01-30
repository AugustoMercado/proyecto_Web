import base64
from io import BytesIO

import qrcode
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from myarticles.models import Products
from .models import Cart, CartsItems

def get_active_cart(user):
    """Retrieves the current active cart for the user."""
    return Cart.objects.filter(user=user, active=True).first()

def get_or_create_active_cart(user):
    """Retrieves the active cart or creates a new one if it does not exist."""
    return Cart.objects.get_or_create(user=user, active=True)

def generate_qr_image(cart_id, user, total):
    """
    Generates a QR code image encoded in base64.
    """
    qr_text = f"ORDER #{cart_id}\nClient: {user.first_name} {user.last_name}\nEmail: {user.email}\nTotal: ${total}\nStatus: PAY"
    qr = qrcode.make(qr_text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def deduct_order_stock(cart):
    """
    Deducts purchased quantities from product stock.
    Ensures stock does not go below zero.
    """
    for item in cart.cartbuy.all():
        product = item.product
        product.stock = max(0, product.stock - item.quantity)
        product.save()

@staff_member_required(login_url='login')
def mark_as_paid(request, cart_id):
    """
    Marks a cart as paid and renders the success page.
    """
    cart = get_object_or_404(Cart, id=cart_id)

    if cart.is_paid:
        return redirect('main')

    cart.is_paid = True
    cart.save()

    return render(request, 'User/Successful_payment.html', {'cart': cart})

def send_owner_notification(request, cart):
    """
    Sends email notification to owner with order details.
    """
    try:
        subject = f'🚀 NEW SALE #{cart.id} - {request.user.first_name} {request.user.last_name}'
        owner_email = 'juanabrahamcorales@gmail.com'
        protocol = 'https' if request.is_secure() else 'http'

        context = {
            'user': request.user,
            'cart': cart,
            'domain': request.get_host(),
            'protocol': protocol
        }

        html_message = render_to_string('Emails/email.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, owner_email, [owner_email], html_message=html_message)
    except Exception as e:
        print(f"Error sending email: {e}")


def add_to_cart(request, product_id):
    """
    API endpoint to add or update item quantity in cart.
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'login_required',
            'message': 'Debes iniciar sesión para agregar productos'
        })

    product = get_object_or_404(Products, id=product_id)
    cart, _ = get_or_create_active_cart(request.user)
    cart_item, is_new = CartsItems.objects.get_or_create(cart_id=cart, product=product)

    quantity = parse_quantity(request.GET.get('cantidad', 1))

    if is_new:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    return JsonResponse({
        'status': 'ok',
        'message': f'{quantity} x {product.name} agregado',
        'total_quantity': cart_item.quantity
    })


def parse_quantity(quantity_str):
    """
    Parses quantity from string, returns 1 if invalid.
    """
    try:
        return int(quantity_str)
    except ValueError:
        return 1

def show_my_cart(request):
    """
    Renders the cart page.
    """
    if not request.user.is_authenticated:
        return render(request, 'Articles/cart_article.html', {'cart': None})

    cart, _ = get_or_create_active_cart(request.user)
    return render(request, 'Articles/cart_article.html', {'cart': [cart]})

def cart_detail(request, cart_id):
    """
    Renders the detail of a specific cart.
    """
    cart = get_object_or_404(Cart, id=cart_id)
    cart_items = CartsItems.objects.filter(cart_id=cart_id)
    return render(request, 'Articles/cart_article.html', {'cart': [cart], 'cart_items': cart_items})

def remove_product_from_cart(request, product_id):
    """
    Removes a specific product from the active cart.
    """
    if request.user.is_authenticated:
        cart = get_active_cart(request.user)
        if cart:
            CartsItems.objects.filter(cart_id=cart, product_id=product_id).delete()

    return redirect('show_my_cart') 

def update_item(request, product_id, action):
    """
    API endpoint to increment or decrement item quantity in cart.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'quantity': 0, 'total': 0})

    cart = get_active_cart(request.user)
    if not cart:
        return JsonResponse({'quantity': 0, 'total': 0})

    item = CartsItems.objects.filter(cart_id=cart, product_id=product_id).first()
    if not item:
        return JsonResponse({'quantity': 0, 'total': cart.get_total()})

    if action == 'add':
        item.quantity += 1
        item.save()
    elif action == 'subtract':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            return JsonResponse({'quantity': 0, 'total': cart.get_total()})

    return JsonResponse({'quantity': item.quantity, 'total': cart.get_total()})

def cancel_cart(request):
    """
    Deletes the entire active cart.
    """
    if request.user.is_authenticated:
        cart = get_active_cart(request.user)
        if cart:
            cart.delete()

    return redirect('main')

def process_buy(request):
    """
    Processes checkout: deducts stock, closes cart, generates QR, sends email.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    cart = get_active_cart(request.user)
    if not cart:
        return redirect('main')

    deduct_order_stock(cart)
    cart.active = False
    cart.save()

    qr_image = generate_qr_image(cart.id, request.user, cart.get_total())
    send_owner_notification(request, cart)

    return render(request, 'User/ticket.html', {
        'qr_image': qr_image,
        'cart': cart,
        'date': timezone.now()
    })

def view_ticket(request, cart_id):
    """
    Renders a ticket for a past order.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

    qr_image = generate_qr_image(cart.id, cart.user, cart.get_total())

    return render(request, 'User/ticket.html', {
        'qr_image': qr_image,
        'cart': cart,
        'date': timezone.now()
    })