from django.shortcuts import get_object_or_404, render
from bookstore_app.models import Book
from django.contrib.auth.models import User
from .models import Cart, CartItem

# Create your views here.
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(User, user=request.user)
    
    product = Book.objects.filter(id=kwargs.get('isbn', "")).first()

    order_item, status = CartItem.objects.get_or_create(product=product)

