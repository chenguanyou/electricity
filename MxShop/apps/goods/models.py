from datetime import datetime

from django.db import models


from DjangoUeditor.models import UEditorField   #富文本编辑器

# Create your models here.
class GoodsCategory(models.Model):
    '''
    商品类别：
    name = 类别名称
    code = 编码
    desc = 简单描述
    category_type = 分类级别
    parent_category = 父类别指向自己，父类别self
    is_tab = 是否放到导航页面，布尔类型
    add_time = 类别添加时间
    help_text用于文档说明
    '''
    CATEGORY_TYPE = ((1, "一级类别"),
                     (2, "二级类别"),
                     (3, "三级类别"))  #类别的分类，用choices来进行连接

    name = models.CharField(default="", max_length=30, verbose_name="商品名称", help_text="商品名称")
    code = models.CharField(default="", max_length=32, null=True, blank=True, verbose_name="英文名称", help_text="英文名称")
    desc = models.TextField(default="", verbose_name="简单描述", help_text="商品描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="商品类别", help_text="商品类别")
    parent_category = models.ForeignKey("self", null=True, blank=True, related_name="sub_cat", verbose_name="父类别", help_text="父类别")
    is_tab = models.BooleanField(default=False, verbose_name="是否显示导航", help_text="是否显示导航")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "商品类别管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class GoodsCategoryBrand(models.Model):
    '''
    商品类别的品牌信息
    name = 品牌名称
    desc = 品牌的简单描述
    image = 品牌的logo  保存到目录brand
    add_time = 添加时间
    '''
    category = models.ForeignKey(GoodsCategory, related_name="brandss", null=True, blank=True, verbose_name="商品类别")
    name = models.CharField(default="", max_length=50, verbose_name="商品品牌名称", help_text="商品品牌名称")
    desc = models.TextField(default="", max_length=100, verbose_name="商品品牌描述", help_text="商品的品牌描述")
    image = models.ImageField(max_length=200, null=True, blank=True, upload_to="GoodsCategoryBrand/%Y/%m", verbose_name="品牌图片", help_text="品牌图片")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "商品品牌管理"
        verbose_name_plural = verbose_name
        db_table = "goods_goodsbrand"

    def __str__(self):
        return self.name



class Goods(models.Model):
    '''
    商品：
    category = 类别
    goods_sn = 商品的编码
    name = 商品的名称
    click_num = 商品的点击数
    sold_num = 商品卖出的数量
    fav_num = 商品被收藏了多少次
    goods_num = 商品的库存数量
    market_price = 商品的市场价
    shop_price = 商店的价格
    goods_brief = 商品的简介
    goods_desc = 商品的描述，需要用到富文本编辑器
    ship_free = 是否免运费
    goods_front_image = 封面图片
    is_new = 是否是新品
    is_hot = 是否热卖
    '''
    category = models.ForeignKey(GoodsCategory, related_name="brands", verbose_name="商品类别", help_text="商品的类别")
    goods_sn = models.CharField(default="", max_length=100, verbose_name="商品的编号", help_text="商品的编号")
    name = models.CharField(default="", max_length=100, verbose_name="商品的名称", help_text="商品的名称")
    click_num = models.IntegerField(default=0, verbose_name="商品的点击数", help_text="商品的点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品卖出数量", help_text="商品卖出数量")
    fav_num = models.IntegerField(default=0, verbose_name="商品的收藏数", help_text="商品的收藏数")
    goods_num = models.IntegerField(default=0, verbose_name="商品的库存数量", help_text="商品的库存数量")
    market_price = models.FloatField(default=0 ,verbose_name="商品的市场价", help_text="商品的市场价")
    shop_price = models.FloatField(default=0, verbose_name="现价", help_text="现价")
    goods_brief = models.TextField(default="", verbose_name="商品的简介", help_text="商品的简介")
    goods_desc = UEditorField(default="", width=900, height=300, toolbars="full", imagePath="Goods/image/%(basename)s_%(datetime)s.%(extname)s",filePath="Goods/file/%(basename)s_%(datetime)s.%(extname)s", settings={}, command=None, blank=True, verbose_name="商品的描述", help_text="商品描述")
    ship_free = models.BooleanField(default=False, verbose_name="是否承担运费", help_text="是否承担运费")
    goods_front_image = models.ImageField(max_length=200, null=True, blank=True, upload_to="Goods/%Y/%m", verbose_name="商品封面图", help_text="商品封面图")
    is_new = models.BooleanField(default=False, verbose_name="是非新品", help_text="是非新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否热卖", help_text="是否热卖")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "商品信息管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class IndexAD(models.Model):
    '''
    首页商品广告位
    category:商品类目
    Goods:商品
    '''
    category = models.ForeignKey(GoodsCategory, related_name="category", verbose_name="商品类目")
    Goods = models.ForeignKey(Goods, related_name="goods", verbose_name="商品")

    class Meta:
        verbose_name = "首页商品广告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category.name


class GoodsImage(models.Model):
    '''
    商品轮播图：
     goods = 商品
     image = 商品轮播图
     image_url = 图片的url
     add_time = 上传时间
    '''
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品", related_name="images")
    image = models.ImageField(max_length=200, upload_to="GoodsImage/%Y/%m", null=True, blank=True, verbose_name="轮播图图片", help_text="轮播图图片")
    image_url = models.URLField(max_length=100, default="", verbose_name="图片地址", help_text="图片地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="上传时间", help_text="上传时间")

    class Meta:
        verbose_name = "商品轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name



class Banner(models.Model):
    '''
    首页轮播图:
    goods = 指向商品
    image = 首页轮播图图片
    index = 轮播图的顺序
    add_time = 上传时间
    '''
    goods = models.ForeignKey(Goods, verbose_name="商品名称", help_text="商品名称")
    image = models.ImageField(max_length=200, upload_to="Banner/%Y/%m", null=True, blank=True, verbose_name="商品首页轮播图", help_text="商品首页轮播图")
    index = models.IntegerField(default=0, verbose_name="轮播图顺序", help_text="轮播图顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "首页轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name