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

