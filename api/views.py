from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *


class Brand4TypeView(APIView):
    def get(self, request, type_name):
        products = Product.objects.filter(type__type_name=type_name).values('brand')
        brand_arr = []
        for idx in products:
            brand = Brand.objects.get(pk=idx['brand'])
            serializer = BrandSerializer(brand)
            brand_arr.append(serializer.data)
        return Response(brand_arr, status=status.HTTP_200_OK)


class Type4CategoryView(APIView):
    def get(self, request, category_name):
        types = Type.objects.filter(category__category_name=category_name)
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
