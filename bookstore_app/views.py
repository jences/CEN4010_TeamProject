from bookstore_app.models import Book, Author, Publisher, WebsiteUser, Cart, CartItem
from bookstore_app.serializers import BookSerializer, AuthorSerializer, PublisherSerializer, WebsiteUserSerializer, CartItemSerializer, CartSerializer
from rest_framework.response import Response
from rest_framework import views, response, exceptions, permissions, viewsets, status, generics
from bookstore_app import serializers as user_serializers, user_services
from bookstore_app import authentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class WebsiteUserViewSet(viewsets.ModelViewSet):
    queryset = WebsiteUser.objects.all()
    serializer_class = WebsiteUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

#API endpoint that creates a user profile
class RegisterAPI(views.APIView):
    def post(self, request):
        serializer = WebsiteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check if a user with the same username or email already exists
        if WebsiteUser.objects.filter(username=data.username).exists():
            return response.Response(data={"message": "Username already in use."}, status=status.HTTP_400_BAD_REQUEST)

        if WebsiteUser.objects.filter(email=data.email).exists():
            return response.Response(data={"message": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        serializer.instance = user_services.create_user(user_dc=data)
    
        print(data)

        return response.Response(data={"User": "created"})

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAuthorID(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        books = Book.objects.filter(author__id=author_id)
        return books
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            # Return a custom response if there are no books
            message = "No books found for the specified author."
            return Response({'message': message})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


#API endpoint that lets users log into their account, if they have one   
class LoginAPI(views.APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = user_services.user_username_selector(username=username)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        #Creates a token from the authentication.py file to let users log in with their credentials
        token = user_services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)
        resp.data = {"message" : "You're now logged in."}

        return resp

#Profile view endpoint    
class WebsiteUserAPI(views.APIView):

    #this endpoint is accessible only if user is authenticated

    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user

        serializer = user_serializers.WebsiteUserSerializer(user)

        return response.Response(serializer.data)

#Logout endpoint  
class LogoutAPI(views.APIView):

    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "You're now logged out."}

        return resp
    

#API endpoint that allows superusers to view all website users and edit if needed.
class UserViewSet(viewsets.ModelViewSet):
    queryset = WebsiteUser.objects.all().order_by('-date_joined')
    serializer_class = WebsiteUserSerializer
    permission_classes = [IsAdminUser]


class CartOwnerID(generics.ListAPIView):
    #@api_view(['GET', 'POST'])
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        try:
            user_profile = WebsiteUser.objects.get(pk=user_id)
        except WebsiteUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user_cart = Cart.objects.filter(owner=user_profile)
        #user_items = CartItem.objects.filter(cart=user_cart)
        #serializer = CartSerializer(user_items, many=True)
        #return user_items
        return user_cart

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            message = "There is no shopping cart found for the specified user."
            return Response({'message': message})
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CartItemAPI(views.APIView):
    def adjust_quantity(request, user_id, book_id, format=None):

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = WebsiteUser.objects.get(pk=user_id)
        except WebsiteUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#   
# def user_cart_list(request, id, format=None):
#
#        try:
#            user_profile = WebsiteUser.objects.get(pk=id)
#        except WebsiteUser.DoesNotExist:
#            return Response(status=status.HTTP_404_NOT_FOUND)
#        
#        if request.method == 'GET':
#            user_cart = Cart.objects.filter(owner=user_profile, is_ordered=False)
#            user_items = CartItem.objects.filter(cart=user_cart, is_ordered=False)
#            serializer = CartSerializer(user_items, many=True)
#            
#            return Response(serializer.data)
#            #if user_cart.exists():
#                #cart_items = Cart.get_cart_items
#                #return cart_items
#                
#        if request.method == 'POST':
#            serializer = CartSerializer(data=request.data)
#            if serializer.is_valid():
#                serializer.save()
#                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#            else:
#                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
#    def post(self, request):
#        serializer = CartSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#        else:
#            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
                             
