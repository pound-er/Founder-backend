from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


app_name = 'api'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/kakao/signin/', KakaoSignInView.as_view()),


    path('survey/', SurveyView.as_view()),
    path('type/category/<str:category>/', Type4CategoryView.as_view()),
]
