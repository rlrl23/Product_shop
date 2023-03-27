from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='products')

urlpatterns = [
    path('product/', views.product_list, name='product_list'),
    path('product/<slug:category_slug>/',views.product_list,name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/',views.product_detail,name='product_detail'),
    path('', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/',views.category_list, name='category_list_by_category'),
path('api/', include(router.urls)),
]