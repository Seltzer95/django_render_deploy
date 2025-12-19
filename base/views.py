from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category



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