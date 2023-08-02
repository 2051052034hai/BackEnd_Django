from rest_framework import serializers
from .models import Product, Category, Bill, BillDetail, User


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source="image")

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
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='avatar')

    def get_image(self, user):
        if user.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % user.avatar.name) if request else ''

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()
        return u

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'address', 'email', 'image', 'avatar']

        extra_kwargs = {
            'avatar': {'write_only': 'True'},
            'password': {'write_only': 'True'}
        }


class BillDetailSerializer(serializers.ModelSerializer):
    bill_id = serializers.IntegerField(read_only=False)
    product_id = serializers.IntegerField(read_only=False)

    class Meta:
        model = BillDetail
        fields = ['id', 'price', 'quantity', 'bill_id', 'product_id']
