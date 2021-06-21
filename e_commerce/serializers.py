from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)
    company = CompanySerializer()
    class Meta:
        model = Product
        fields = ('id','name','image_url','price','category','company','description','discount','quantity')

    def get_image_url(self, product):
        request = self.context.get('request')
        image_url = product.image.url
        return request.build_absolute_uri(image_url)


'''
class SingleProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    company = CompanySerializer()
    class Meta:
        model = Product
        fields = ('id','name','category','company','price','image')
'''








'''class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)'''
