from django.db import models
from django.contrib.auth.models import User
from bookstore_app.models import Book

class CartItem(models.Model):
    product = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    price_ht = models.FloatField(blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name
    
class Cart(models.Model):
    #ref_code=models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #is_ordered = models.BooleanField(default=False)

    def get_cart_items(self):
        return self.items.all()
    
    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])
    
    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)
    
# Create your models here.