from django.shortcuts import render, redirect, get_object_or_404
from .models import Shoes, AvailableSizes, ShoeImages, Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator


def all_products(request):
    shoes = Shoes.objects.all().prefetch_related('availablesizes_set', 'shoeimages_set')
    search_query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '')
    brand = request.GET.get('brand', '')
    type_ = request.GET.get('type', '')

    # Search
    if search_query:
        shoes = shoes.filter(
            Q(shoe_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(type__icontains=search_query)
        )

    # Filter by brand
    if brand:
        shoes = shoes.filter(brand=brand)
    # Filter by type
    if type_:
        shoes = shoes.filter(type=type_)

    # Sort
    if sort == 'price':
        shoes = shoes.order_by('original_price')
    elif sort == 'price_desc':
        shoes = shoes.order_by('-original_price')
    elif sort == 'brand':
        shoes = shoes.order_by('brand')
    elif sort == 'type':
        shoes = shoes.order_by('type')

    # Lấy danh sách brand và type duy nhất
    brands = Shoes.objects.values_list('brand', flat=True).distinct()
    types = Shoes.objects.values_list('type', flat=True).distinct()

    paginator = Paginator(shoes, 16) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'shoes': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort': sort,
        'brands': brands,
        'types': types,
        'selected_brand': brand,
        'selected_type': type_,
    })

def product_details(request, sku):
	shoe = get_object_or_404(
		Shoes.objects.prefetch_related('availablesizes_set', 'shoeimages_set'),
		sku=sku
	)
	
	related_products = Shoes.objects.filter(brand=shoe.brand).exclude(sku=shoe.sku)[:4]
	context = {
		'shoe': shoe,
		'available_sizes': shoe.availablesizes_set.all(),
		'shoe_images': shoe.shoeimages_set.all(),
        'related_products': related_products,
	}

	return render(request, 'products-details.html', context)

def add_to_cart(request, sku):
    shoe = get_object_or_404(Shoes, sku=sku)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    # Tìm AvailableSizes object
    size_obj = get_object_or_404(AvailableSizes, sku=shoe, size=size)

    # Kiểm tra còn hàng
    if size_obj.in_stock is not None and size_obj.in_stock < quantity:
        messages.error(request, f"Size {size} chỉ còn {size_obj.in_stock} sản phẩm!")
        return redirect('products_details', sku=sku)

    key = f"{sku}_{size}"
    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'sku': sku,
            'size': size,
            'quantity': quantity
        }

    # Trừ số lượng trong kho
    size_obj.in_stock -= quantity
    size_obj.save()

    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for key, item in cart.items():
        sku = item['sku']
        size = item['size']
        quantity = item['quantity']
        try:
            product = Shoes.objects.get(sku=sku)
        except Shoes.DoesNotExist:
            continue
        subtotal = (product.original_price or 0) * quantity
        total += subtotal
        items.append({
            'key': key,
            'product': product,
            'size': size,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'cart.html', {'items': items, 'total': total})

def remove_from_cart(request, key):
    cart = request.session.get('cart', {})
    if key in cart:
        sku = cart[key]['sku']
        size = cart[key]['size']
        quantity = cart[key]['quantity']
        # Cộng lại số lượng vào kho
        size_obj = AvailableSizes.objects.filter(sku=sku, size=size).first()
        if size_obj:
            size_obj.in_stock += quantity
            size_obj.save()
        del cart[key]
    request.session['cart'] = cart
    return redirect('view_cart')

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment = request.POST.get('payment')
        cart = request.session.get('cart', {})
        total = 0
        items = []
        for key, item in cart.items():
            sku, size = key.split('_', 1)
            try:
                product = Shoes.objects.get(sku=sku)
            except Shoes.DoesNotExist:
                continue
            quantity = item['quantity']
            subtotal = (product.original_price or 0) * quantity
            total += subtotal
            items.append((product, quantity, product.original_price or 0, size))
        order = Order.objects.create(
            name=name, address=address, phone=phone, payment=payment, total=total
        )
        for product, quantity, price, size in items:
            OrderItem.objects.create(order=order, shoe=product, quantity=quantity, price=price)
        request.session['cart'] = {}  # Xóa giỏ hàng sau khi đặt
        return render(request, 'cart.html', {'order': order})
    return redirect('view_cart')


def home(request):
    featured_shoes = Shoes.objects.all().order_by('-original_price')[:4]
    latest_shoes = Shoes.objects.all().order_by('-sku')[:8]
    context = {
		'featured_shoes': featured_shoes,
		'latest_shoes': latest_shoes,
	}
    return render(request, 'index.html', context)

def products_men(request):
    shoes = Shoes.objects.filter(gender__iexact='Nam').prefetch_related('availablesizes_set', 'shoeimages_set')
    search_query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '')
    brand = request.GET.get('brand', '')
    type_ = request.GET.get('type', '')

    # Search
    if search_query:
        shoes = shoes.filter(
            Q(shoe_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(type__icontains=search_query)
        )

    # Filter by brand
    if brand:
        shoes = shoes.filter(brand=brand)
    # Filter by type
    if type_:
        shoes = shoes.filter(type=type_)

    # Sort
    if sort == 'price':
        shoes = shoes.order_by('original_price')
    elif sort == 'price_desc':
        shoes = shoes.order_by('-original_price')
    elif sort == 'brand':
        shoes = shoes.order_by('brand')
    elif sort == 'type':
        shoes = shoes.order_by('type')

    brands = Shoes.objects.filter(gender__iexact='Nam').values_list('brand', flat=True).distinct()
    types = Shoes.objects.filter(gender__iexact='Nam').values_list('type', flat=True).distinct()

    paginator = Paginator(shoes, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'shoes': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort': sort,
        'brands': brands,
        'types': types,
        'selected_brand': brand,
        'selected_type': type_,
        'gender': 'Men',
    })

def products_women(request):
    shoes = Shoes.objects.filter(gender__iexact='Nữ').prefetch_related('availablesizes_set', 'shoeimages_set')
    search_query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '')
    brand = request.GET.get('brand', '')
    type_ = request.GET.get('type', '')

    # Search
    if search_query:
        shoes = shoes.filter(
            Q(shoe_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(type__icontains=search_query)
        )

    # Filter by brand
    if brand:
        shoes = shoes.filter(brand=brand)
    # Filter by type
    if type_:
        shoes = shoes.filter(type=type_)

    # Sort
    if sort == 'price':
        shoes = shoes.order_by('original_price')
    elif sort == 'price_desc':
        shoes = shoes.order_by('-original_price')
    elif sort == 'brand':
        shoes = shoes.order_by('brand')
    elif sort == 'type':
        shoes = shoes.order_by('type')

    brands = Shoes.objects.filter(gender__iexact='Nữ').values_list('brand', flat=True).distinct()
    types = Shoes.objects.filter(gender__iexact='Nữ').values_list('type', flat=True).distinct()

    paginator = Paginator(shoes, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'shoes': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort': sort,
        'brands': brands,
        'types': types,
        'selected_brand': brand,
        'selected_type': type_,
        'gender': 'Women',
    })