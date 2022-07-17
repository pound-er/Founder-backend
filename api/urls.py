from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('type/recommend/', views.Type4RecommendView.as_view()),
    path('survey/', views.SurveyView.as_view()),
    path('type/category/<str:category_name>/', views.Type4CategoryView.as_view()),
    path('brand/<str:type_name>/', views.Brand4TypeView.as_view()),
    path('type/category/<str:category>/', views.Type4CategoryView.as_view()),
    path('product/detail/<int:pk>/', views.ProductDetailView.as_view()),
]
