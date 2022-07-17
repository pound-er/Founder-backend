from datetime import datetime
from .forms import ReviewForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *


class Type4CategoryView(APIView):
    def get(self, request, category):
        types = Type.objects.filter(category__category_name=category)
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SurveyView(APIView):
    def put(self, request):
        user = User.objects.get(pk=1)  # 데모데이터(admin)

        # 기존의 설문 정보 삭제
        SurveyResult.objects.filter(user=user).delete()

        for each_json in request.data:

            # 큐레이션 문항
            if each_json['question_num'] == "1":
                if each_json['answer_num'] == "1":
                    user.set_curation = True
                else:
                    user.set_curation = False
                user.save()

            # 큐레이션 외 문항
            else:
                question_num = each_json['question_num']
                answer_num = each_json['answer_num']

                survey = Survey.objects.get(question_num=question_num, answer_num=answer_num)

                if survey.type_arr == "null":
                    continue

                types = survey.type_arr.split(',')  # 파싱
                for type_name in types:
                    each_type = Type.objects.get(type_name=type_name)
                    survey_result, flag = SurveyResult.objects.get_or_create(type=each_type, user=user)
                    if not flag:  # table 존재 = 가중치 True
                        continue
                    survey_result.rec_result = True
                    survey_result.save()

        data = SurveyResult.objects.filter(user=user)
        serializer = SurveyResultSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewView(APIView):  # 리뷰 전체 불러 오기
    def get(self, request, pk):  # 상품의 pk
        reviews = Review.objects.filter(product_id=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = Product.objects.get(pk=pk)
            review.user = User.objects.get(pk=1)  # 데모데이터(admin)
            review.review_main_img = request.data['review_main_img']
            review.save()
            # 다중 이미지 처리
            for img in request.FILES.getlist('reviewMedia'):
                review_media = ReviewMedia()
                review_media.review = review
                review_media.review_img = img
                review_media.save()
            return Response("Created Successfully", status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


