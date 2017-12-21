"""BlogProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Blog import views as blog
from comments import views as comments

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',blog.IndexView.as_view(),name="index"),
    url(r'^article/(?P<pk>[0-9]+)/$',blog.detail,name="detail"),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',blog.archives,name="archives"),
    url(r'^categorys/(?P<category>[\S]+)/$',blog.categorys,name="categorys"),
    url(r'^tags/(?P<tag>[\S]+)/$',blog.tags,name="tags"),
    url(r'^comment/post/(?P<article_pk>[0-9]+)/$', comments.comment_post, name="comment_post"),
    url(r'^search/$',blog.search,name="search")
]