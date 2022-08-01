from rest_framework import serializers
from .models import *


class SurveyResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = SurveyResult
        fields = [
            'id',
            'user',
            'type',
            'rec_result',
        ]


class MagazineContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MagazineContent
        fields = [
            'id',
            'brand',
            'detail_title',
            'detail_content',
            'detail_img',
        ]


class MagazineMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine
        fields = [
            'id',
            'title',
            'tag_arr',
            'intro',
            'img_main',
        ]


class MagazineSerializer(serializers.ModelSerializer):

    magazine_magazinecontent = MagazineContentSerializer(many=True, read_only=True)

    class Meta:
        model = Magazine
        fields = [
            'id',
            'magazine_type',
            'title',
            'author',
            'tag_arr',
            'created_at',
            'episode_num',
            'img_main',
            'img_header',
            'intro',
            'magazine_magazinecontent',
        ]


class ReviewMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewMedia
        fields = [
            'id',
            'review',
            'review_img',
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
            'review_tag_arr',
            'review_text',
            'review_img_main',
            'created_at',
            'review_reviewmedia',
        ]


class ProductSerializer(serializers.ModelSerializer):

    # product_review = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'type',
            'brand',
            'product_name',
            'product_img',
            'product_img_detail',
            'custom_flag',
            'discount_flag',
            'delivery_cycle',
            'delivery_cycle_detail',
            'min_price',
            'min_std_price',
            'max_std_price',
            'star_rate_avg',
            'purchase_link',
            # 'product_review',
        ]


class BrandSerializer(serializers.ModelSerializer):

    # brand_product = ProductSerializer(many=True)
    # brand_magazinecontent = MagazineContentSerializer(many=True)

    class Meta:
        model = Brand
        fields = [
            'id',
            'brand_name',
            'brand_name_eng',
            'brand_img_logo',
            'brand_link',
            'brand_desc',
            'brand_img_bg',
            'curation',
            # 'brand_product',
            # 'brand_magazinecontent',
        ]


class TypeSerializer(serializers.ModelSerializer):

    type_brand = BrandSerializer(many=True)
    type_product = ProductSerializer(many=True)

    class Meta:
        model = Type
        fields = [
            'id',
            'category',
            'type_name',
            'type_desc',
            'type_desc_detail',
            'type_tag_arr',
            'type_img_footer',
            'type_brand',
            'type_product',
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


class UserSerializer(serializers.ModelSerializer):

    user_review = ReviewSerializer(many=True)
    user_surveyresult = SurveyResultSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'email',
            'gender',
            'set_curation',
            'user_review',
            'user_surveyresult',
        ]

