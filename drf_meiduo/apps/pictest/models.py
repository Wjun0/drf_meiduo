from django.db import models

# Create your models here.


class PicTest(models.Model):
    '''上传图片测试'''
    image = models.ImageField(verbose_name='图片')
    class Meta:
        db_table = 'tb_pics'
        verbose_name = '上传图片'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '图片：%s'%(self.image)