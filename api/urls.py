from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


app_name = 'api'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/kakao/signin/', KakaoSignInView.as_view()),
    path('auth/kakao/signin/callback/', KaKaoSignInCallBackView.as_view()),

    path('type/recommend/', Type4RecommendView.as_view()),
    path('survey/', SurveyView.as_view()),
    path('type/category/<str:category_name>/', Type4CategoryView.as_view()),
    path('brand/<str:type_name>/', Brand4TypeView.as_view()),
    path('type/category/<str:category>/', Type4CategoryView.as_view()),
    path('review/<int:pk>/', ReviewView.as_view()),
    path('product/detail/<int:pk>/', ProductDetailView.as_view()),
]
