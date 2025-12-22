from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Order, OrderItem, Product, Category
from django.contrib.auth.models import User
from rest_framework import status
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    data = []
    for order in orders:
        items = []
        for item in order.items.all():
            items.append({
                'product_id': item.product.id,
                'product_desc': item.product.desc,
                'quantity': item.quantity,
                'price': str(item.product.price),
            })
        data.append({
            'order_id': order.id,
            'created_at': order.created_at,
            'is_paid': order.is_paid,
            'items': items,
        })
    return Response(data)







@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_product(request):
    items = request.data.get('items')
    if not items or not isinstance(items, list):
        return Response({'error': 'Invalid items format'}, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        order = Order.objects.create(user=request.user)
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            if not product_id:
                return Response({'error': 'Product ID is required for each item'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': f'Product with ID {product_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if quantity < 1:
                return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
    return Response({'message': 'Order created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = "staff"

        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
def index(req):
    return Response('index')

@api_view(['GET'])
def hello(req):
    return Response('hello')

@api_view(['GET'])
def test(req):
    return Response({'username': 'jseltzer'})

def cars(request):
    products = Product.objects.filter(category__name__iexact='cars')
    context = {'products': products}
    return render(request, 'base/cars.html', context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def only_members(request):
    user = request.user
    return Response({'welcome': user.username})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({'error': 'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)

    return Response({'message': 'user created successfully'}, status=status.HTTP_201_CREATED)
