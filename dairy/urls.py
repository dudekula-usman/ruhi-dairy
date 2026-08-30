from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:variant_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/increase/<int:variant_id>/',
        views.increase_cart,
        name='increase_cart'
    ),

    path(
        'cart/decrease/<int:variant_id>/',
        views.decrease_cart,
        name='decrease_cart'
    ),

    path(
        'cart/remove/<int:variant_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
]