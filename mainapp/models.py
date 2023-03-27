from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='templates/categories/', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Subcategory(Category):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)

class Product(models.Model):
    sub_category = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image= models.ImageField(upload_to='products', blank=True)
    # image_medium = models.ImageField(upload_to='products/medium/', blank=True)
    # image_large = models.ImageField(upload_to='products/large/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    img_small = ImageSpecField(source='image', processors=[ResizeToFill(50, 50)],
                                 format='JPEG', options={'quality': 90})
    img_medium = ImageSpecField(source='image', processors=[ResizeToFill(300, 200)],
                                  format='JPEG', options={'quality': 90})
    img_big = ImageSpecField(source='image', processors=[ResizeToFit(640, 480)],
                           format='JPEG', options={'quality': 90})

    # stock = models.PositiveIntegerField() #Это поле PositiveIntegerField для хранения остатков данного продукта.
    # available = models.BooleanField(default=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    def __str__(self):
        return self.name

