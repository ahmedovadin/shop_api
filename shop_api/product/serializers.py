from rest_framework import serializers
from .models import Category, Product, Review

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

