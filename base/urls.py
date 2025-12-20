from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('', views.index),
    path('hello/', views.hello),
    path('test/', views.test),
    path('cars/', views.cars, name='cars'),
    path('login/', TokenObtainPairView.as_view()),
    path('register/', views.register_user),
]
