from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Category, Product


class CategorySerializer(ModelSerializer):
    category = ReadOnlyField(source='subcategory.category.name', read_only=True)
    class Meta:
        model = Category
        #exclude=['id',]
        fields=['name','slug', 'image', 'category',]

class ProductSerializer(ModelSerializer):
    sub_category = ReadOnlyField(source='sub_category.name', read_only=True)
    category=ReadOnlyField(source='sub_category.category.name', read_only=True)
    class Meta:
        model = Product
        #exclude=['id','description']
        fields=['name','slug','sub_category', 'category', 'price', 'image',]