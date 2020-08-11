import random

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from drf_meiduo.apps.users.models import User
from drf_meiduo.apps.users.serializers import UserSerializer, UserDetailSerializer, EmailSerializer
from . import constants
from drf_meiduo.utils.response_code import RETCODE
from rest_framework.permissions import IsAuthenticated


class EmailVerification(APIView):
    def put(self,request):
        token = request.query_params.get('token')
        if not token:
            return Response({'message':"缺少token"},status=status.HTTP_400_BAD_REQUEST)
        user = User.check_email_token(token)

        if user is None:
            return Response({'message':"连接无效"},status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()
        return Response({'message':"ok"})

class EmailView(UpdateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    def get_object(self):
        return self.request.user

#注册用户
class UserView(CreateAPIView):
    serializer_class = UserSerializer



#检查手机号是否存在
class MobileCountView(APIView):
    def get(self,request,mobile):
        count = User.objects.filter(mobile = mobile).count()
        if count > 0:
            return Response({'status':RETCODE.ALLOWERR,"message":"该手机号已存在！"})
        return Response({'status':RETCODE.OK,'message':"ok",'data':{'username':mobile,'count':1}})



#判断用户名是否重复
class UsernameCountView(APIView):
    def get(self,request,username):
        count = User.objects.filter(username = username).count()
        if count > 0:
            return Response({'status':RETCODE.ALLOWERR,"message":"该用户已存在！"})
        return Response({'status':RETCODE.OK,'message':"ok",'data':{'username':username,'count':1}})



# 获取短信验证码
class SMScode(APIView):
    def get(self,request,mobile):
        redis_conn = get_redis_connection('sms_code')
        flag = redis_conn.get('sms_code_flag_%s' % mobile)
        # 没有到期，防止频繁发送短信验证码
        if flag:
            return Response({'status':RETCODE.CPWDERR,'message':"请求过于频繁！"})
        sms_code ='%06d'%random.randint(0,999999)
        # print(mobile)
        print(sms_code)
        # redis_conn.setex('sms_code_%s' % mobile, constants.SMS_EXPIRES_TIME, sms_code)


        # 优化：
        p1 = redis_conn.pipeline()
        p1.setex('sms_code_%s' % mobile, constants.SMS_EXPIRES_TIME, sms_code)
        p1.setex('sms_code_flag_%s' % mobile, constants.SMS_FLAG,1)
        p1.execute()

        try:
            pass
            #发送短信验证码
        except:
            pass

        return Response({'status':RETCODE.OK, 'message':'ok'})