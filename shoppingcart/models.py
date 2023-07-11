from django.db import models
from django.contrib.auth.models import User
from bookstore_app.models import Book, Author, Publisher, WebsiteUser

class OrderItem(models.Model):
    product = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    ref_code=models.CharField(max_length=15)
# Create your models here.