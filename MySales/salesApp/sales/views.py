from . import serializers
from .models import Category, Product, User, Bill, BillDetail
from rest_framework import viewsets, generics, permissions, parsers, status
from .serializers import CategorySerializer, ProductSerializer, UserSerializer, BillSerializer, BillDetailSerializer
from .paginator import ProductPaginator
from rest_framework.decorators import action, api_view
from rest_framework.views import Response
from django.db import transaction


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=True, url_path='products')
    def products(self, request, pk):
        c = self.get_object()
        products = c.product_set.all()

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPaginator

    def filter_queryset(self, queryset):
        q = queryset
        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(subject_icontains=kw)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            q = q.filter(category_id=cate_id)

        return q

    @action(methods=['post'], detail=False, url_path='create')
    def create_product(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['delete'], detail=True, url_path='delete')
    def delete_product(self, request, pk):
        try:
            p = self.get_object()
            p.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except p.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=True, url_path='update')
    def update_product(self, request, pk):
        p = self.get_object()
        serializer = ProductSerializer(p, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='get')
    def get_Product(self, request, pk):
        product = self.get_object()
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'put'], detail=False, url_path='current-user')
    def current_user(self, request):
        u = request.user
        if request.method.__eq__('PUT'):
            for k, v in request.data.items():
                setattr(u, k, v)
            u.save()

        return Response(UserSerializer(u, context={'request': request}).data)


class BillViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    parser_classes = [parsers.MultiPartParser, ]

    @transaction.atomic()
    def create(self, request):

        bill_data = {
            'subTotal': request.data.get('bill[subTotal]', 0),
            'user': request.data.get('bill[user]', None),
        }

        # Create a serializer instance with the bill data
        bill_serializer = BillSerializer(data=bill_data)
        if bill_serializer.is_valid():
            bill = bill_serializer.save()  # Save the Bill object to the database
        else:
            return Response(bill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        i = 0
        bill_details_data = []
        while f'bill_details[{i}][price]' in request.data:
            detail_data = {
                'price': request.data[f'bill_details[{i}][price]'],
                'quantity': request.data[f'bill_details[{i}][quantity]'],
                'product_id': int(request.data[f'bill_details[{i}][product_id]']),
                'bill_id': bill.id,

            }
            bill_details_data.append(detail_data)
            i += 1

        # Create serializers for BillDetails and save them to the database
        for detail_data in bill_details_data:
            detail_serializer = BillDetailSerializer(data=detail_data)
            if detail_serializer.is_valid():
                detail_serializer.save()
            else:
                return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Bill and BillDetails created successfully."}, status=status.HTTP_201_CREATED)
