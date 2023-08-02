from django.urls import path, include
from rest_framework import routers
from . import views

r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet)
r.register('products', views.ProductViewSet)
r.register('users', views.UserViewSet)
r.register('bills', views.BillViewSet)

urlpatterns = [
    path('', include(r.urls)),
]