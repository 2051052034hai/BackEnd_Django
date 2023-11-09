from rest_framework import pagination

class ProductPaginator(pagination.PageNumberPagination):
    page_size = 50

class ProductPagination(pagination.PageNumberPagination):
    page_size = 5  # Số lượng sản phẩm trên mỗi trang