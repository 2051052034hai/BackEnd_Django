from .models import Category, Product
from rest_framework import viewsets, generics, status, permissions
from .serializers import CategorySerializer, ProductSerializer
from .paginator import ProductPaginator
from rest_framework.decorators import action
from rest_framework.views import Response


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

    @action(methods=['post'], detail=False, url_path = 'create')
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
