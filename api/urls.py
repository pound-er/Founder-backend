from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


app_name = 'api'

urlpatterns = [

    # token
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),

    # Kakao
    path('auth/kakao/signin', KakaoSignInView.as_view()),
    path('auth/kakao/signin/callback', KaKaoSignInCallBackView.as_view()),
    path('auth/kakao/signout', KakaoSignOutView.as_view()),
    path('auth/kakao/signout/callback', KaKaoSignOutCallBackView.as_view()),

    # User
    path('user', UserDetailView.as_view()),

    # Recommend
    path('recommend', RecommendView.as_view()),

    # Survey
    path('survey', SurveyView.as_view()),

    # Product
    path('product/<int:pk>', ProductDetailView.as_view()),
    path('product/<int:pk>/review', ReviewView.as_view()),

    # Category
    path('category/<str:category_name>', CategoryDetailView.as_view()),

    # Brand
    path('brand/<int:pk>', BrandDetailView.as_view()),

    # Magazine
    path('magazine', MagazineView.as_view()),
    path('magazine/<int:pk>', MagazineDetailView.as_view()),

]
