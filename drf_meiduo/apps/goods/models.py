from django.db import models

# Create your models here.
from drf_meiduo.utils.models import BaseModel


class GoodsCategory(BaseModel):
    '''商品类别'''
    name = models.CharField(max_length=20,verbose_name='类别名称')
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,verbose_name='父类别')
    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsChannel(BaseModel):
    '''商品频道'''
    group_id = models.IntegerField(verbose_name='组号')
    category = models.OneToOneField(GoodsCategory,on_delete=models.CASCADE,verbose_name='顶级商品类别')
    url = models.CharField(max_length=50,verbose_name='频道页连接地址')
    sequence = models.IntegerField(verbose_name='组内序号')
    class Meta:
        db_table = 'tb_goods_channel'
        verbose_name = '商品频道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name

class Brand(BaseModel):
    '''品牌'''
    name = models.CharField(max_length=20,verbose_name='品牌名称')
    logo = models.ImageField(max_length=50,verbose_name='logo连接地址')
    first_letter = models.CharField(max_length=1,verbose_name='品牌首字母')
    class Meta:
        db_table = 'tb_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Goods(BaseModel):
    '''商品'''
    name = models.CharField(max_length=50,verbose_name='商品名称')
    brand = models.ForeignKey(Brand,on_delete=models.PROTECT,verbose_name='品牌ID')
    category1 = models.ForeignKey(GoodsCategory,related_name='cat_goods1',on_delete=models.PROTECT,verbose_name='一级类别')
    category2 = models.ForeignKey(GoodsCategory,related_name='cat_goods2',on_delete=models.PROTECT,verbose_name='二级类别')
    category3 = models.ForeignKey(GoodsCategory,related_name='cat_goods3',on_delete=models.PROTECT,verbose_name='三级类别')
    saies = models.IntegerField(default=0,verbose_name='销量')
    comments = models.IntegerField(default=0,verbose_name='评论量')

    class Meta:
        db_table = 'tb_goods'
        verbose_name = '商品spu'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSpecification(BaseModel):
    '''商品规格'''
    name = models.CharField(max_length=50,verbose_name='规格名称')
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品')
    class Meta:
        db_table = 'tb_goods_specification'
        verbose_name = '商品规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s:%s'%(self.goods.name,self.name)



class SpecificationOption(BaseModel):
    '''规格选项'''
    spec = models.ForeignKey(GoodsSpecification,on_delete=models.CASCADE,verbose_name='规格id')
    value = models.CharField(max_length=20,verbose_name='选项值')
    class Meta:
        db_table = 'tb_specification_option'
        verbose_name = '规格选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-%s"%(self.spec,self.value)



class SKU(BaseModel):
    '''SKU信息'''
    name = models.CharField(max_length=50,verbose_name='sku名称')
    caption = models.CharField(max_length=100,verbose_name='副标题')
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='商品ID')
    category = models.ForeignKey(GoodsCategory,on_delete=models.PROTECT,verbose_name='商品类别id')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='单价')
    cost_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='进价')
    market_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='市场价')
    sales = models.IntegerField(default=0,verbose_name='销量')
    comments = models.IntegerField(default=0,verbose_name='评论量')
    is_launched = models.BooleanField(default=True,verbose_name='是否上架')
    default_inage_url = models.CharField(max_length=100,null=True,default='',blank=True,verbose_name='默认图片地址')
    class Meta:
        db_table = 'tb_sku'
        verbose_name = '商品SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s : %s'%(self.id,self.name)


class SKUImage(BaseModel):
    '''SKU图片'''
    sku = models.ForeignKey(SKU,on_delete=models.CASCADE,verbose_name='所属SKU')
    image = models.CharField(max_length=100,verbose_name='图片连接地址')

    class Meta:
        db_table = 'tb_sku_image'
        verbose_name = 'sku图片地址'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '%s:%s'%(self.sku.name,self.id)


class SKUSpecition(BaseModel):
    '''规格信息'''
    sku = models.ForeignKey(SKU,on_delete=models.CASCADE,verbose_name='所属sku')
    spec = models.ForeignKey(GoodsSpecification,on_delete=models.PROTECT,verbose_name='规格ID')
    option = models.ForeignKey(SpecificationOption,on_delete=models.PROTECT,verbose_name='规格选项ID')
    class Meta:
        db_table = 'tb_sku_specification'
        verbose_name = '规格信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '%s %s %s'%(self.sku,self.spec.name,self.option.value)