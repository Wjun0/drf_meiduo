from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer

# Create your models here.
from area.models import Area
from drf_meiduo.utils.models import BaseModel


class User(AbstractUser):
    '''自定义用户模型类'''
    mobile = models.CharField(max_length=11,unique=True,verbose_name = '手机号')
    email_active = models.BooleanField(default=False,verbose_name="邮箱验证状态")
    default_address = models.OneToOneField('Address',related_name='add_user',null=True,blank=True,on_delete=models.SET_NULL,verbose_name='默认收货地址')

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



class Address(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses',verbose_name='用户')
    title = models.CharField(max_length=20,verbose_name='地址名称')
    receiver = models.CharField(max_length=20,verbose_name='收货人')
    province = models.ForeignKey(Area,related_name='province_address',on_delete=models.PROTECT,verbose_name='省')
    city = models.ForeignKey(Area,related_name='city_address',on_delete=models.PROTECT,verbose_name='市')
    district = models.ForeignKey(Area,related_name='district_address',on_delete=models.PROTECT,verbose_name='区')
    place = models.CharField(max_length=50,verbose_name='地址')
    mobile = models.CharField(max_length=11,verbose_name='手机')
    tel = models.CharField(max_length=20,null=True,blank=True,default='',verbose_name='固定电话')
    email = models.CharField(max_length=30,null=True,blank=True,default='',verbose_name='邮箱')
    is_deleted = models.BooleanField(default=False,verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']  #查询时使用的排序方式