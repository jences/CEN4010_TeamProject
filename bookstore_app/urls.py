from django.urls import path
from bookstore_app import views

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name="register"),
    path('login/', views.LoginAPI.as_view(), name="login"),
    path('profile/', views.WebsiteUserAPI.as_view(), name='profile'),
    path('logout/', views.LogoutAPI.as_view(), name='logout'),
    path('cart/<int:user_id>', views.CartOwnerID.as_view(), name='cart_items_by_user'),

]
