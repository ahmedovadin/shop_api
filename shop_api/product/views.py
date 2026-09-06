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
    ReviewListSerializer,
    ProductReviewListSerializer,
    ProductValidator,
    CategoryValidator,
    ReviewValidator
)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(data='Category not found!', status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        validator = CategoryValidator(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)

        # step 1: receive data
        category.name = request.data['name']
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailSerializer(category).data)


@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.prefetch_related('products').all()
        list_ = CategoryListSerializer(categories, many=True).data

        return Response(data=list_)
    
    elif request.method == 'POST':
        validator = CategoryValidator(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)
        validated = validator.validated_data

        # step 1: receive data
        name = validated.get('name')

        category = Category.objects.create(
            name=name
        )
        category.save()
        return Response(status=status.HTTP_201_CREATED, data=CategoryListSerializer(category).data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(data='Product not found!', status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        validator = ProductValidator(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)
         
        product.title = request.data['title']
        product.description = request.data['description']
        product.price = request.data['price']
        product.category_id = request.data['category_id']
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)

@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        list_ = ProductListSerializer(products, many=True).data

        return Response(data=list_)

    elif request.method == 'POST':
        validator = ProductValidator(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)
        validated = validator.validated_data

        # step 1: receive data
        title = validated.get('title')
        description = validated.get('description')
        price = validated.get('price')
        category_id = validated.get('category_id')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category_id
        )
        product.save()
        return Response(status=status.HTTP_201_CREATED, data=ProductListSerializer(product).data)

@api_view(['GET'])
def product_review_list_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    list_ = ProductReviewListSerializer(products, many=True).data

    return Response(data=list_)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(data='Review not found!', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        validator = ReviewValidator(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)

        validated = validator.validated_data
        
        # step 1: receive data
        review.text = validated.get('text')
        review.product_id = validated.get('product_id')
        review.stars = validated.get('stars', review.stars)
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailSerializer(review).data)

@api_view(['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        list_ = ReviewListSerializer(reviews, many=True).data
        return Response(data=list_)
    elif request.method == 'POST':
        validator = ReviewValidator(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=validator.errors)
        validated = validator.validated_data

        # step 1: receive data
        text = validated.get('text')
        product_id = validated.get('product_id')
        stars = validated.get('stars', 3)

        review = Review.objects.create(
            text=text,
            product_id=product_id,
            stars=stars
        )
        review.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewListSerializer(review).data)

    