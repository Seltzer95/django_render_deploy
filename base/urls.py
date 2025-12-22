from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('', views.index),
    path('hello/', views.hello),
    path('test/', views.test),
    path('cars/', views.cars, name='cars'),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.register_user),
    path('members/', views.only_members),
    path('buy/', views.buy_product, name='buy_product'),
    path('orders/', views.my_orders, name='my_orders'),
]

