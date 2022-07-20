from django.shortcuts import redirect
from django.conf import settings
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .models import *
from .forms import ReviewForm

import requests


# 토큰 수동 생성
def get_tokens_for_user(User):
    refresh = RefreshToken.for_user(User)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# 카카오 회원가입+로그인 : 인가 코드 받기
class KakaoSignInView(APIView):
    def get(self, request):
        client_id = settings.KAKAO_REST_API_KEY
        redirect_uri = settings.KAKAO_SIGNIN_REDIRECT_URI

        return redirect(
            f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        )


# 카카오 회원가입+로그인 : 콜백
class KaKaoSignInCallBackView(APIView):
    def get(self, request):

        create_data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirection_uri': settings.KAKAO_SIGNIN_REDIRECT_URI,
            'code': request.GET.get("code")
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        kakao_token_json = requests.post(kakao_token_api, data=create_data).json()
        access_token = kakao_token_json.get('access_token')

        kakao_user_api = 'https://kapi.kakao.com/v2/user/me'
        auth_header = {
            "Authorization": f"Bearer ${access_token}"
        }
        user_info = requests.get(kakao_user_api, headers=auth_header).json()

        properties = user_info.get("properties")
        kakao_account = user_info.get("kakao_account")

        kakao_nickname = properties.get("nickname")
        kakao_email = kakao_account.get("email")

        try:
            user = User.objects.get(email=kakao_email)
            status = "Existing User : SignIn"   # 로그인

        except:
            user = User(email=kakao_email, nickname=kakao_nickname)
            user = user.save()
            user = User.objects.get(email=kakao_email)
            status = "New User : SignUp"    # 회원가입 : 회원 정보 저장

        token = get_tokens_for_user(user)

        res = Response({
            "nickname": kakao_nickname,
            "email": kakao_email,
            "gender": user.gender,
            "set_curation": user.set_curation,
            "status": status,
            "token": token,
        })

        refresh_token = token["refresh"]
        res.set_cookie('refresh_token', refresh_token)

        return


class UserDetailView(APIView):
    def get(self, request):

        cur_user = request.user

        if cur_user.is_anonymous:
            return Response("Anonymous User", status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserSerializer(request.user)
            return Response({
                "nickname": serializer.data["nickname"],
                "email": serializer.data["email"],
                "gender": serializer.data["gender"],
                "review_cnt": len(serializer.data["user_review"])
            }, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Brand4TypeView(APIView):
    def get(self, request, type_name):
        products = Product.objects.filter(type__type_name=type_name).values('brand')
        brand_arr = []
        for idx in products:
            brand = Brand.objects.get(pk=idx['brand'])
            serializer = BrandSerializer(brand)
            brand_arr.append(serializer.data)
        return Response(brand_arr, status=status.HTTP_200_OK)


class Type4RecommendView(APIView):
    def get(self, request):
    
        # 로그인 시 "맞춤 추천 Type" 정보 반환
        '''
        user = User.objects.get(pk=1)  # 데모데이터(admin)
        data = SurveyResult.objects.filter(user=user).values('type')
        type_arr = []
        for idx in data:
            types = Type.objects.get(pk=idx['type'])
            serializer = TypeSerializer(types)
            type_arr.append(serializer.data)
        return Response(type_arr, status=status.HTTP_200_OK)
        '''
        
        # 미 로그인 시 "식품 모두 다 / 스킨케어 팩 / 유산균 / 영양제 / 맞춤케어 영양제 팩" 정보 반환
        food_types = Type.objects.filter(category__category_name="Food")  # 식품 모두
        serializer = TypeSerializer(food_types, many=True)
        type_arr = serializer.data
        data = ["SkinCarePack", "Lacto", "Supplement", "CarePack"]  # 스킨케어 팩, 유산균, 영양제, 맞춤케어 영양제 팩
        for idx in data:
            types = Type.objects.get(type_name=idx)
            serializer = TypeSerializer(types)
            type_arr.append(serializer.data)
        return Response(type_arr, status=status.HTTP_200_OK)


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

            # 성별 문항
            if each_json['question_num'] == "0":
                if each_json['answer_num'] == "1":
                    user.gender = 'Female'
                else:
                    user.gender = 'Male'
                user.save()

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


class BrandDetailView(APIView):
    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        brand = Brand.objects.get(pk=pk)
        serializer = BrandSerializer(brand)
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

