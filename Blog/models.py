# --*--coding:utf-8--*--

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

# Create your models here.


# 创建分类表
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=20,verbose_name="分类名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类名称"
        verbose_name_plural = "分类名称"

# 创建标签表
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name="标签名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签名称"
        verbose_name_plural = "标签名称"


# 创建文章表
@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=70,verbose_name="标题")
    # 一篇文章只能有一个作者,而一个作者可以有多篇文章,所以是一对多关系
    author = models.ForeignKey(User,verbose_name="作者")
    excerpt = models.CharField(max_length=200,blank=True,verbose_name="摘要")
    body = models.TextField(verbose_name="内容")
    creat_time = models.DateTimeField(verbose_name="创建时间")
    last_time = models.DateTimeField(verbose_name="修改时间")
    # 一篇文章只能有一个分类,而一个分类可以有多篇文章,所以是一对多关系
    category = models.ForeignKey(Category,verbose_name="分类")
    # 一篇文章可以有多个标签,而一个标签也可以有多篇文章,所以是多对多关系
    tag = models.ManyToManyField(Tag,blank=True,verbose_name="标签")
    # 增加一个阅读量的字段以方便统计阅读量
    views = models.PositiveIntegerField(default=0,editable=False)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"

    # 生成一个根据文章id的URL
    def get_absolute_url(self):
        return reverse("detail",kwargs={"pk":self.pk})

#     定义一个统计阅读量的方法,即每次阅读量+1并保存到数据库
    def clean_views(self,state=True):
        if state:
            self.views += 1
            # update_fields的作用为告诉数据库只更新views字段
            self.save(update_fields=["views"])
        # 设置一个state参数,使得评论提交之后重定向回评论页面时,阅读量不会增加
        else:
            self.views -= 1
            self.save(update_fields=["views"])

