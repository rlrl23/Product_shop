from django.shortcuts import render, get_object_or_404
from .models import Category, Subcategory, Product, Token
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.order_by('subcategory')
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


def token_auth(request):
    try:
        user_token = request.headers.get('Authorization')
        words, token = user_token.split(' ')
        get_object_or_404(Token, key=token)
        request.user = {'is_authenticated': True}
        return(request)
    except:
        pass

def category_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(subcategory=None)
    subcategories = Subcategory.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = subcategories.filter(category=category)

    paginator = Paginator(subcategories, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    token_auth(request)

    return render(request,
                  'shop/category_list.html',
                  {'category': category,
                   'categories': categories,
                   'subcategories': subcategories,
                   'page_obj': page_obj,
                   })

def product_list(request, category_slug=None):
    category = None
    categories = Subcategory.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Subcategory, slug=category_slug)
        products = products.filter(sub_category=category)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    token_auth(request)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'page_obj': page_obj,
                   })

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug)
    cart_product_form = CartAddProductForm()
    token_auth(request)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   })