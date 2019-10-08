from django.shortcuts import render,redirect
import markdown
# Create your views here.
# 导入 HttpResponse 模块
from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm
# 视图函数
def article_list(request):
        # 取出所有博客文章
        articles = ArticlePost.objects.all()
        # 需要传递给模板（templates）的对象
        context = {'articles': articles}
        # render函数：载入模板，并返回context对象
        return render(request, 'article/list.html', context)
# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])
    # 需要传递给模板的对象
    context = { 'article': article }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)
# 删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        context = {'article': article}
        return render(request,"article/list.html",context)
    else:
        return HttpResponse("仅允许post请求")
def article_update(request,id):
    article=ArticlePost.objects.get(id=id)
    if request.method=="POST":
        article_post_form=ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title=request.POST['title']
            article.body=request.POST['body']
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
