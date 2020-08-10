from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from drf_meiduo.apps.users.models import User


def jwt_response_paylod_handler(token,user=None,request=None):
    '''自定义jwt认证成功后的返回数据'''
    return {
        'token':token,
        'user_id':user.id,
        'username':user.username
    }




class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user

