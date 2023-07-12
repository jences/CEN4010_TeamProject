from django.contrib import admin
from .models import Book, Author, Publisher, WebsiteUser, Cart, CartItem

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(WebsiteUser)
admin.site.register(Cart)
admin.site.register(CartItem)