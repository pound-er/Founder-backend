from rest_framework import serializers
from .models import *


class SurveyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResult
        fields = [
            'id',
            'user',
            'type',
            'rec_result'
        ]


class ReviewMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMedia
        fields = [
            'id',
            'review',
            'review_img',
            'img_num',
        ]


class ReviewSerializer(serializers.ModelSerializer):

    review_reviewmedia = ReviewMediaSerializer(many=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'product',
            'user',
            'star_rate',
            'review_text',
            'review_tag_arr',
            'review_main_img',
            'created_at',
            'review_reviewmedia',
        ]


class ProductSerializer(serializers.ModelSerializer):

    product_review = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'type',
            'brand',
            'product_name',
            'product_main_img',
            'product_detail_img',
            'custom_flag',
            'delivery_cycle_main',
            'delivery_cycle_detail',
            'min_price',
            'max_price',
            'star_rate_avg',
            'volume',
            'pcs',
            'std_price',
            'discount_flag',
            'purchase_link',
            'main_product_flag',
            'default_rec_flag',
            'product_review',
        ]


class TypeSerializer(serializers.ModelSerializer):

    type_product = ProductSerializer(many=True)
    type_surveyresult = SurveyResultSerializer(many=True)

    class Meta:
        model = Type
        fields = [
            'id',
            'category',
            'type_name',
            'type_desc',
            'type_desc_detail',
            'type_tag_arr',
            'type_img',
            'order',
            'type_product',
            'type_surveyresult'
        ]


class CategorySerializer(serializers.ModelSerializer):

    category_type = TypeSerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'category_name',
            'category_type',
        ]


class BrandSerializer(serializers.ModelSerializer):

    brand_product = ProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = [
            'id',
            'brand_name',
            'brand_logo',
            'brand_link',
            'brand_desc',
            'brand_bg_img',
            'brand_product',
        ]


class MagazineContentSerializer(serializers.ModelSerializer):

    magazinecontent_brand = BrandSerializer(many=True)

    class Meta:
        model = MagazineContent
        fields = [
            'id',
            'detail_title',
            'detail_content',
            'detail_img',
            'magazinecontent_brand',
        ]


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

    user_surveyresult = SurveyResultSerializer(many=True)
    user_review = ReviewSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'email',
            'gender',
            'set_curation',
            'user_surveyresult',
            'user_review',
        ]

