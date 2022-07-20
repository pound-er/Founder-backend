from rest_framework import serializers
from .models import *


class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResult
        fields = ['user', 'type', 'rec_result']


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

    user_surveyresult = SurveyResultSerializer(many=True)
    user_review = ReviewSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'nickname',
            'email',
            'gender',
            'set_curation',
            'user_surveyresult',
            'user_review',
        ]

