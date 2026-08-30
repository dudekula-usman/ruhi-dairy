from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch

from .models import Product, ProductVariant


# =========================================================
# HOME
# =========================================================

def home(request):

    products = Product.objects.filter(
        availability=True
    ).prefetch_related(
        Prefetch(
            'variants',
            queryset=ProductVariant.objects.filter(
                availability=True
            )
        )
    )[:4]

    return render(
        request,
        'home.html',
        {
            'products': products
        }
    )


# =========================================================
# PRODUCTS
# =========================================================

def products(request):

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    product_list = Product.objects.filter(
        availability=True
    ).prefetch_related(
        Prefetch(
            'variants',
            queryset=ProductVariant.objects.all().order_by('price')
        )
    ).order_by('name')

    if search_query:

        product_list = product_list.filter(
            name__icontains=search_query
        )

    return render(
        request,
        'products.html',
        {
            'products': product_list,
            'search_query': search_query,
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, variant_id):

    variant = get_object_or_404(
        ProductVariant.objects.select_related('product'),
        id=variant_id
    )

    # Product unavailable
    if not variant.product.availability:

        return redirect('products')

    # Variant unavailable
    if not variant.availability:

        return redirect('products')

    # No stock
    if variant.stock_quantity <= 0:

        return redirect('products')

    cart = request.session.get(
        'cart',
        {}
    )

    variant_id = str(variant_id)

    current_quantity = cart.get(
        variant_id,
        0
    )

    # Don't exceed stock
    if current_quantity < variant.stock_quantity:

        cart[variant_id] = current_quantity + 1

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('products')


# =========================================================
# CART
# =========================================================

def cart(request):

    cart_data = request.session.get(
        'cart',
        {}
    )

    cart_items = []

    total = 0

    for variant_id, quantity in cart_data.items():

        variant = get_object_or_404(
            ProductVariant.objects.select_related('product'),
            id=variant_id
        )

        # Automatically remove unavailable variants
        if (
            not variant.availability
            or not variant.product.availability
            or variant.stock_quantity <= 0
        ):

            del cart_data[variant_id]

            continue

        # Make sure cart quantity doesn't exceed stock
        if quantity > variant.stock_quantity:

            quantity = variant.stock_quantity

            cart_data[variant_id] = quantity

        subtotal = (
            variant.price * quantity
        )

        total += subtotal

        cart_items.append({
            'variant': variant,
            'product': variant.product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    request.session['cart'] = cart_data

    request.session.modified = True

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# =========================================================
# INCREASE CART ITEM
# =========================================================

def increase_cart(request, variant_id):

    variant = get_object_or_404(
        ProductVariant.objects.select_related('product'),
        id=variant_id
    )

    cart = request.session.get(
        'cart',
        {}
    )

    variant_id = str(variant_id)

    current_quantity = cart.get(
        variant_id,
        0
    )

    # Check stock
    if (
        variant.availability
        and variant.product.availability
        and current_quantity < variant.stock_quantity
    ):

        cart[variant_id] = (
            current_quantity + 1
        )

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')


# =========================================================
# DECREASE CART ITEM
# =========================================================

def decrease_cart(request, variant_id):

    cart = request.session.get(
        'cart',
        {}
    )

    variant_id = str(variant_id)

    if variant_id in cart:

        cart[variant_id] -= 1

        if cart[variant_id] <= 0:

            del cart[variant_id]

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')


# =========================================================
# REMOVE CART ITEM
# =========================================================

def remove_from_cart(request, variant_id):

    cart = request.session.get(
        'cart',
        {}
    )

    variant_id = str(variant_id)

    if variant_id in cart:

        del cart[variant_id]

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')