#from django.shortcuts import render

# Create your views here.

#from django.http import HttpResponse
from django.shortcuts import render_to_response,get_object_or_404,render
from .models import Article,Category,Tag
import markdown
#由此可知CommentForm是Comment的一个FORM实例
from comments.forms import CommentForm
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView

# 定义一个分页模型
class IndexView(ListView):
    model = Article     #获取Article模型里面的列表
    template_name = "Blog/index.html"       #要渲染的网页模板
    context_object_name = "article_list"    #模板列表数据传递给模板的变量名(即传给网页模板)
    paginate_by = 5     #分页的数量(即5个为一页)


# 定义首页视图
def index(request):
    article_list = Article.objects.all().order_by("-id")
    category_list = Category.objects.all().order_by("id")
    tag_list = Tag.objects.all().order_by("id")
    return render_to_response("Blog/index.html",context={
        "article_list":article_list,
    })

# 定义文章详情视图(这里使用的Markdown,Pyments语法高亮拓展)
@csrf_protect
def detail(request,pk):
    # 定义一个404页面(即查找的参数在数据库中不存在报404码)
    article = get_object_or_404(Article,pk=pk)
    # 每访问一次就调用一次阅读量方法(即阅读量+1)
    article.clean_views()
    # markdown语法高亮拓展,参数extensions为各种拓展
    article.body = markdown.markdown(article.body,extensions=[
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.toc",
    ])
    # 表单实例(在网页中创建一个form)
    form = CommentForm()
    # 获取评论
    comment_list = article.comment_set.all()
    context = {
        "form":form,
        "article":article,
        "comment_list":comment_list,
    }
    # csrf验证,需要用render,如果用render_to_response需要context.uptade(csrf(request))对数据进行csrf验证
    return render(request,"Blog/detail.html",context)

# 定义一个归档视图(时间)
def archives(request,year,month):
    # filter过滤筛选,creat_time.year因作为参数,.使用__代替
    # 这里还可以写成反向查询
    # (year,month).article_set.all().order_by("-creat_time")
    article_list = Article.objects.filter(creat_time__year=year,
                                          creat_time__month=month).order_by("-creat_time")
    return render_to_response("Blog/index.html",context={
        "article_list":article_list,
    })

# 定义一个分类视图
def categorys(request,category):
    # 反向查询
    # 即某分类下的所有文章
    # category.article_set.all().order_by("-creat_time")
    # 把分类为某分类的文章过滤出来
    article_list = Article.objects.filter(category__name=category).order_by("-creat_time")

    return render_to_response("Blog/index.html",context={
        "article_list":article_list,
    })

# 定义一个标签视图
def tags(request,tag):
    # tag.article_set.all().order_by("-creat_time")
    article_list = Article.objects.filter(tag__name=tag).order_by("-creat_time")

    return render_to_response("Blog/index.html",context={
        "article_list":article_list,
    })

# 定义一个搜索视图
def search(request):
    # 用户提交的数据保存在request.GET(字典)中,使用get获取内容(q是搜索输入框的name属性值),""当q没有数据时则为空
    q = request.GET.get("q")
    error_msg = ""

    if not q:
        error_msg = "请输入有效数据!"
        return render_to_response("Blog/error.html",{"error_msg":error_msg})

    article_list = Article.objects.filter(title__icontains=q)
    return render_to_response("Blog/search.html",{"article_list":article_list,
                                                  "error_msg":error_msg})