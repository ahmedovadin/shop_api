from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name products_count'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = 'id updated'.split()

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price category'.split()

class ProductReviewListSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = 'id title price category reviews rating'.split()

    def get_reviews(self, product):
        return product.review_list()

    def get_rating(self, product):
            return product.rating()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['id']

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CategoryValidator(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, min_length=1)

class ProductValidator(serializers.Serializer):
    title = serializers.CharField(required=True,max_length=255, min_length=1)
    description = serializers.CharField(required=False, default="No Description")
    price = serializers.FloatField()
    category_id = serializers.IntegerField()
        
    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category_id

class ReviewValidator(serializers.Serializer):
    text = serializers.CharField(required=False, default="No Review text")
    product_id = serializers.IntegerField()
    stars = serializers.IntegerField(required=False, default=3, min_value=1, max_value=5)
            
    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product_id