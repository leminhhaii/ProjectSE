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



from django.core.paginator import Paginator

def products(request):
    shoes = Product.objects.filter(in_stock__gt=0)
    sort = request.GET.get('sort')
    if sort == 'price':
        shoes = shoes.order_by('original_price')
    elif sort == 'price_desc':
        shoes = shoes.order_by('-original_price')
    # Pagination
    paginator = Paginator(shoes, 8)  # 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'page_obj': page_obj, 'sort': sort})

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
    
    image_list = []
    if shoe.image_urls:
        image_list = [img.strip().strip("'").strip('"') for img in shoe.image_urls.strip("[]").split(",") if img.strip()]
    related_products = Product.objects.filter(brand=shoe.brand, in_stock__gt=0).exclude(sku=shoe.sku)[:4]

    return render(request, 'products-details.html', {
        'shoe': shoe,
        'available_sizes': available_sizes,
        'image_list': image_list,
        'related_products': related_products,
    })


def home(request):
    # Get 4 featured products (customize the filter as needed)
    featured_products = Product.objects.filter(in_stock__gt=0)[:4]
    # Get 4 latest products (ordered by id or created_at)
    latest_products = Product.objects.filter(in_stock__gt=0).order_by('-sku')[:8]
    return render(request, 'index.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
    })

@login_required
def remove_from_cart(request, sku):
    product = get_object_or_404(Product, sku=sku)
    cart = Cart.objects.filter(user=request.user, is_completed=False).first()
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            # Cộng lại số lượng vào kho
            product.in_stock += cart_item.quantity
            product.save()
            cart_item.delete()
    return redirect('cart')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user, is_completed=False).first()
    items = CartItem.objects.filter(cart=cart) if cart else []
    return render(request, 'cart.html', {'cart': cart, 'items': items})

@login_required
def add_to_cart(request, sku):
    product = get_object_or_404(Product, sku=sku)
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, is_completed=False)

    quantity = int(request.POST.get('quantity', 1))

    # Check if product is out of stock
    if not product.in_stock or product.in_stock < quantity:
        messages.error(request, "Sản phẩm đã hết hàng hoặc không đủ số lượng trong kho.")
        return redirect('shoe_detail', sku=sku)

    # Subtract from stock
    product.in_stock -= quantity
    product.save()

    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size="N/A",
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    # messages.success(request, "Đã thêm sản phẩm vào giỏ hàng.")
    return redirect('cart')

def search_products(request):
    query = request.GET.get('q', '').strip()
    shoes = Product.objects.filter(in_stock__gt=0)
    if query:
        shoes = shoes.filter(
            Q(shoe_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(color__icontains=query)
        )
    return render(request, 'products.html', {'shoes': shoes, 'search_query': query})

def about_us(request):
    return render(request, 'web/aboutus.html')