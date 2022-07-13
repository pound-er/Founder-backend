from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('survey/', views.SurveyView.as_view()),
    path('type/category/<str:category_name>/', views.Type4CategoryView.as_view()),
    path('brand/<str:type_name>/', views.Brand4TypeView.as_view()),
]
