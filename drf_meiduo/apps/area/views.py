from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_meiduo.apps.area.serializers import AreaSearializer
from . models import Area

class AreasView(APIView):

    def get(self,request):
        queryset = Area.objects.filter(parent=None).all()
        serializer = AreaSearializer(queryset,many=True)
        return Response(serializer.data)
