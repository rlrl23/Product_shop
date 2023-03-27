from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mainapp.models import Product, Token
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return render(request, 'cart/detail.html', {'cart_product_form': form})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('/cart/')


def cart_clean(request):
    cart = Cart(request)
    cart.clear()
    return redirect('/cart/')

def token_auth(request):
    try:
        user_token = request.headers.get('Authorization')
        words, token = user_token.split(' ')
        get_object_or_404(Token, key=token)
        return True
    except:
        return False

def cart_detail(request):
    cart = Cart(request)
    if token_auth(request):
        return render(request, 'cart/detail.html', {'cart': cart})
    else:
        return render(request, 'cart/detail.html')