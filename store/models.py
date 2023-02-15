import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    stripe_product_price_id = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Варианты покупки'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        amount = round(self.price * 100)
        stripe_product_price = stripe.Price.create(product=stripe_product['id'],
                                                   unit_amount=amount,
                                                   currency='rub')
        return stripe_product_price


class Lessons(models.Model):
    LIGHT = 1
    OPTIMAL = 2
    FULL = 3
    access_levels = (
        (LIGHT, 'Лайт'),
        (OPTIMAL, 'Оптимальный'),
        (FULL, 'Полный'),
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000, blank=True, null=True)
    access_level = models.SmallIntegerField(choices=access_levels)
    video_file = models.FileField(upload_to='files', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Уроки'


class Order(models.Model):
    CREATED = 0
    PAID = 1
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
    )

    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Покупки"




