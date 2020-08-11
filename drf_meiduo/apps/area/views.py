from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_meiduo.apps.area.serializers import AreaSearializer,RetriverAreasSerializer
from . models import Area
from rest_framework_extensions.cache.decorators import cache_response


class AreasView(ListAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSearializer

    def get_queryset(self):
        return Area.objects.filter(parent=None).all()

    # def get(self,request):
    #     queryset = Area.objects.filter(parent=None).all()
    #     serializer = AreaSearializer(queryset,many=True)
    #     return Response(serializer.data)



class RetriveAreasView(APIView):
    # @cache_response(timeout=60*60,key_func='cache_key_func',cache='session')
    @cache_response(key_func='cache_key_func')
    def get(self,request,pk):
        queryset = Area.objects.filter(id=pk).first()
        serailizer = RetriverAreasSerializer(queryset)
        return Response(serailizer.data)

    def cache_key_func(self,view_instance,view_method,request,args,kwargs):
        print(view_instance)
        print(view_method)
        print(request)
        print(args)
        print(kwargs)
        print(kwargs.get('pk'))
        return kwargs.get('pk')
