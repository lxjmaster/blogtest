from django.db import models
from django.utils.six import python_2_unicode_compatible

# Create your models here.

#创建评论的数据库模型
@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    url = models.URLField(blank=True)
    text = models.TextField()
    creat_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey("Blog.Article")

    def __str__(self):
        return self.text[:20]