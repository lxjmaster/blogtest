from ..models import Article,Category,Tag
from django import template


register = template.Library()

class RecentArticles(template.Node):
    def render(self, context):
        context["ArticleList"] = Article.objects.all().order_by("-creat_time")[:5]#一个最新5篇文章的模板标签
        context["ArchivesDate"] = Article.objects.dates("creat_time","month",order="DESC")#文章创建时间的模板标签
        context["CategoryList"] = Category.objects.all()#所有分类模板标签
        context["TagList"] = Tag.objects.all() #标签模板标签
        return ""

# 注册模板标签
@register.tag
def get_recent_articles(parser,token):
    return RecentArticles()




