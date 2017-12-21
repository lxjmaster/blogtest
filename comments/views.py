from django.shortcuts import render_to_response,redirect,get_object_or_404,render
from Blog.models import Article
from .models import Comment
from .forms import CommentForm
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
# from django.core.context_processors import csrf


# 定义一个评论POST视图
@csrf_protect
def comment_post(request,article_pk):
    # 检测在Article中是否有参数为pk的文章,没有就返回404
    article = get_object_or_404(Article,pk=article_pk)
    # 判断请求方式是什么(POST OR GET)
    if request.method == "POST":
        #当方式正确时,先生成一个表单实例
        form = CommentForm(request.POST)
        # 验证from中的数据是否合法
        if form.is_valid():
            # 由于需要将评论与被评论的文章关联,所以不能直接保存,要先把表单实例写进去,等关联评论和文章之后再保存到数据库
            comment = form.save(commit=False)#commit=False(提交=False),即不提交到数据库
            # 关联评论和文章
            comment.article = article
            # 保存到数据库
            comment.save()
            # 此时提交评论,页面重定向回评论页面,state=False则阅读量不会增加
            article.clean_views(state=False)
            # 然后重定向到网页(即把更新的内容重定向到网页)
            return redirect(article)#detail?
        # 检测到数据不合法时
        else:
            # 重定向回网页(新的数据并没有添加进去)
            # comment_list为已存在的评论(即原网页已经显示的),
            # 使用反向查询(以下查上),查询该文章下的全部评论
            # 某文章(article)的(.)评论(comment_set)
            comment_list = article.comment_set.all()
            # 重定向回的内容
            context = {
                "article":article,
                "form":form,
                "comment_list":comment_list,
            }
            # 或者注释下面一行,并把render_to_response改成render
            context.update(csrf(request))
            return render_to_response("Blog/detail.html",context)
    # 如果提交的方式不是POST
    else:
        return redirect(article)