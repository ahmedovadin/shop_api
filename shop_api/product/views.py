from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from django.forms import model_to_dict
from .serializers import (
    CategoryListSerializer, 
    CategoryDetailSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ReviewDetailSerializer,
    ReviewListSerializer
)

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(data='Category not found!', status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category, many=False).data

    return Response(data=data)

@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    list_ = CategoryListSerializer(categories, many=True).data

    return Response(data=list_)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(data='Product not found!', status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product, many=False).data

    return Response(data=data)

@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    list_ = ProductListSerializer(products, many=True).data

    return Response(data=list_)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(data='Review not found!', status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review, many=False).data
    
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    list_ = ReviewListSerializer(reviews, many=True).data

    return Response(data=list_)