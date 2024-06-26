from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_fullname = models.CharField(max_length=255)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255)
    shipping_city= models.CharField(max_length=255)
    shipping_state= models.CharField(max_length=255, null = True, blank=True)
    shipping_zipcode = models.CharField(max_length=255, null = True, blank=True)
    shipping_country = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
#Order Model
class Order(models.Model):
    #Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True, blank=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=250)
    shipping_address= models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status =  models.CharField(max_length=25, default='Pending')
    shipped_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f'Order - {str(self.id)}'
    
   
#Auto add shipping Date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.status == 'Shipped' and obj.status != 'Shipped':
            instance.shipped_date = now
    
    

#Order Items Model
class OrderItem(models.Model):
    #Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE ,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True, blank=True)
    
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # size = models.CharField()
    
    def __str__(self):
        return f'Order Items - {str(self.id)}'
    
class CancellationOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    cancelled_date = models.DateTimeField(auto_now_add=True)
    mark_as_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Canceled Order - {str(self.id)}'
        