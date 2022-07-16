from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('survey/', SurveyView.as_view()),
    path('type/category/<str:category>/', Type4CategoryView.as_view()),
    path('brand/<int:pk>/', BrandDetailView.as_view()),
]
