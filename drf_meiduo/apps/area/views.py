from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView,CreateAPIView,GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_meiduo.apps.area.serializers import AreaSearializer, RetriverAreasSerializer, AddressSerializer
from drf_meiduo.apps.users.models import Address
from . models import Area
from rest_framework_extensions.cache.decorators import cache_response

# POST /addresses/ 新建  -> create
# PUT /addresses/<pk>/ 修改  -> update
# GET /addresses/  查询  -> list
# DELETE /addresses/<pk>/  删除 -> destroy
# PUT /addresses/<pk>/status/ 设置默认 -> status
# PUT /addresses/<pk>/title/  设置标题 -> title

class AddressesView(APIView):
    # serializer_class = AddressSerializer
    # queryset = Address
    def get(self,request):
        queryset = Address.objects.filter(user=request.user,is_deleted=False).all()
        serializer = AddressSerializer(instance=queryset,many=True)
        default_address = request.user.default_address_id
        user_id = request.user.id
        limit = 5
        return Response({'user_id':user_id,
                         'default_address_id':default_address,
                         'limit':limit,
                         'addresses':serializer.data
                         })


    def post(self,request):
        data = request.data
        serializer = AddressSerializer(data=data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self,request,pk):
        data = request.data
        # update_data = {'city':data['city_id'],
        #                'district':data['district_id'],
        #                'province':data['province_id'],
        #                'receiver':data['receiver'],
        #                'email':data['email'],
        #                'tel':data['tel'],
        #                'title':data['title'],
        #                'place':data['place'],
        #                }
        # Address.objects.filter(id=pk).update(**update_data)    # 返回值是更新的条数
        # serializer = AddressSerializer(Address.objects.get(id=pk))
        # return Response(serializer.data)
        queryset = Address.objects.get(id=pk)
        serializer = AddressSerializer(instance=queryset,data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


    def delete(self,reqeust):
        pass


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
    @cache_response(key_func='cache_key_func')  #  添加缓存
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
