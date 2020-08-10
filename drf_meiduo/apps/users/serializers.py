import re

from django_redis import get_redis_connection
from rest_framework import  serializers

from drf_meiduo.apps.users.models import User

from rest_framework_jwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议',write_only=True)
    token = serializers.CharField(label='JWT token',read_only=True)

    class Meta:
        model = User
        fields = ('id','username','mobile','password','password2','sms_code','allow','token')

        extra_kwargs = {
            'username':{
                'min_length':5,
                'max_length':20,
                'error_messages':{
                    'min_length':'最小长度为5',
                    'max_length':'最大长度为20'
                }
            },
            'password':{
                'write_only':True,
                'min_length':8,
                'max_length':20,
                'error_messages':{
                    'min_length': '最小长度为5',
                    'max_length': '最大长度为20'
                }
            }
        }

    # 验证手机号
    def validate_mobile(self,value):
        if not re.match(r'^1[3-9]\d{9}$',value):
            raise serializers.ValidationError('手机号格式不对')
        count = User.objects.filter(mobile=value).count()
        if count != 0:
            raise serializers.ValidationError('手机号已经注册')
        return value

    # 验证协议
    def validate_allow(self,allow):
        if allow != 'true':
            raise serializers.ValidationError('请同意协议')
        return allow

    # 验证两次密码是否一致
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('两次密码不一致')

        mobile = attrs['mobile']
        redis_conn = get_redis_connection('sms_code')
        real_sms = redis_conn.get('sms_code_%s'%mobile)
        print(real_sms)
        if real_sms is None:
            raise serializers.ValidationError('短信验证码过期')
        sms_code = attrs['sms_code']
        if real_sms.decode() != sms_code:
            raise serializers.ValidationError('验证码错误')
        return attrs

    def create(self,validated_data):
        '删除校验后的无用字段'
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = User.objects.create_user(**validated_data)

        # 生成jwt

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        jwt_token = jwt_encode_handler(payload)


        user.token = jwt_token
        return user




