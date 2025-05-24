from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from .models import Product, Cart, CartItem
from django.contrib import messages
from .serializers import ProductSerializer, CartSerializer
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



def products(request):
    shoes = Product.objects.all()
    return render(request, 'products.html', {'shoes': shoes})

def shoe_detail(request, sku):
    shoe = get_object_or_404(Product, sku=sku)
    # Clean up available_sizes string
    if shoe.available_sizes:
        # Remove brackets and split by comma
        sizes = shoe.available_sizes.strip("[]").split(",")
        # Remove quotes and whitespace
        available_sizes = [size.strip().strip("'").strip('"') for size in sizes if size.strip()]
    else:
        available_sizes = []
    return render(request, 'products-details.html', {'shoe': shoe, 'available_sizes': available_sizes})

def home(request):
    # Get 4 featured products (customize the filter as needed)
    featured_products = Product.objects.all()[:4]
    # Get 4 latest products (ordered by id or created_at)
    latest_products = Product.objects.order_by('-sku')[:8]
    return render(request, 'index.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
    })

@login_required
def add_to_cart(request, sku):
    product = get_object_or_404(Product, sku=sku)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, is_completed=False)

    quantity = int(request.POST.get('quantity', 1))

    if product.in_stock is None or product.in_stock < quantity:
        messages.error(request, "Sản phẩm không còn đủ hàng trong kho.")
        return redirect('shoe_detail', sku=sku)

    # Trừ vào tồn kho
    product.in_stock -= quantity
    product.save()

    # Tạo hoặc cập nhật cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size="N/A",  # size không quan trọng nữa
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, "Đã thêm sản phẩm vào giỏ hàng.")
    return redirect('cart')

@login_required
def remove_from_cart(request, sku):
    product = get_object_or_404(Product, sku=sku)
    cart = Cart.objects.filter(user=request.user, is_completed=False).first()
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            cart_item.delete()
    return redirect('cart')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user, is_completed=False).first()
    items = CartItem.objects.filter(cart=cart) if cart else []
    return render(request, 'cart.html', {'cart': cart, 'items': items})

