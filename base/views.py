from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Product, Category
from django.contrib.auth.models import User
from rest_framework import status



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
