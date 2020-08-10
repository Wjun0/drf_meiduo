from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer

# Create your models here.


class User(AbstractUser):
    '''自定义用户模型类'''
    mobile = models.CharField(max_length=11,unique=True,verbose_name = '手机号')
    email_active = models.BooleanField(default=False,verbose_name="邮箱验证状态")
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_veryify_email_url(self):
        data = {
            'id':self.id,
            'email':self.email
        }
        serializer = TJWSSerializer(secret_key=settings.SECRET_KEY, expires_in=3600)
        token = serializer.dumps(data)  #bytes
        token = token.decode()

        # 生成验证链接地址
        verify_url = 'http://127.0.0.1:8080/succes_verify_email.html?token=' + token
        return verify_url

    @staticmethod
    def check_email_token(token):
        serializer = TJWSSerializer(secret_key=settings.SECRET_KEY,expires_in=3600)
        try:
            data = serializer.loads(token)
        except:
            return None
        id = data.get('id')
        email = data.get('email')
        try:
            user = User.objects.get(id=id,email=email)
        except User.DoesNotExist:
            return None
        return user


    def __str__(self):
        return self.username
