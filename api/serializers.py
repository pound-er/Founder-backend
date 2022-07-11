from rest_framework import serializers
from .models import *


class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResult
        fields = '__all__'


class ReviewMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMedia
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):

    reviewMedia = ReviewMediaSerializer(many=True)

    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    review = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    products = ProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = '__all__'


class MagazineContentSerializer(serializers.ModelSerializer):

    brands = BrandSerializer(many=True)

    class Meta:
        model = MagazineContent
        fields = '__all__'


class MagazineSerializer(serializers.ModelSerializer):

    magazineContents = MagazineContentSerializer(many=True)

    class Meta:
        model = Magazine
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    surveyResults = SurveyResultSerializer(many=True)
    review = ReviewSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'