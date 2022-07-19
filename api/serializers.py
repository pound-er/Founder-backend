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

    magazinecontent_brand = BrandSerializer(many=True)

    class Meta:
        model = MagazineContent
        fields = ['id', 'detail_title', 'detail_content', 'detail_img', 'magazinecontent_brand']


class MagazineSerializer(serializers.ModelSerializer):

    magazine_magazinecontent = MagazineContentSerializer(many=True, read_only=True)

    class Meta:
        model = Magazine
        fields = [
            'id',
            'title',
            'author',
            'tag_arr',
            'created_at',
            'episode_num',
            'main_img',
            'magazine_type',
            'intro_title',
            'intro_content',
            'magazine_magazinecontent',
        ]


class UserSerializer(serializers.ModelSerializer):

    surveyResults = SurveyResultSerializer(many=True)
    review = ReviewSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
