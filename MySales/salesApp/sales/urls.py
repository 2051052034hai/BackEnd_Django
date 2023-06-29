from django.urls import path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet)
r.register('products', views.ProductViewSet)


urlpatterns = [
    path('', include(r.urls)),
]