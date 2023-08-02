from rest_framework import serializers
from .models import Product, Category, Bill, BillDetail


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, product):
        request = self.context.get("request")
        return request.build_absolute_uri('/static/%s' % product.image.name) if request else ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_image(instance)
        return representation

class ProductSerializer(ImageSerializer):
    category_id = serializers.CharField(required=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unitPrice', 'unitsInStock', 'image', 'category_id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'subTotal']
