from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('type/category/<str:category>/', views.Type4CategoryView.as_view()),
]
