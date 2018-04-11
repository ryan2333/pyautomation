# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.base import View, TemplateView
# Create your views here.
from page import JuncheePaginator  #使用重写后的分面
from models import *
from django.forms import model_to_dict
from django.http import JsonResponse,HttpResponse,QueryDict
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import datetime, random,json

class AuthorList(ListView):
    model = Author  #表名
    template_name = 'myweb/authors.html'  #前端渲染页面
    context_object_name = 'authors'  #前端页面循环的数组名称
    paginate_by = 5  #分页，每页条目数

class AuthorApi(View):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        auobj = Author.objects.get(pk=pk)
        data = auobj.todict
        return JsonResponse({'status':0, 'data':data})


class AuthorDetail(DetailView):
    model = Author  #表名
    template_name = 'myweb/author.html'  #前端渲染页面
    context_object_name = 'author'  #前端页面循环的数组名称
    bkmodel = Book2

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['timenow'] = datetime.datetime.now()
        return context

    def post(self,request, **kwargs):
        webdata = QueryDict(request.body).dict() #获取前端传过来的数据,并进行转换为字典
        bks = webdata.get('books')  #取出书的信息
        errors = []
        books = []
        for bk in json.loads(bks):  #后端传过来的 是json串，需要先load出来
            try:
                bkobj = self.bkmodel.objects.get(name=bk)  #查询书是否存在
            except self.bkmodel.DoesNotExist:  #如果书不存在，则添加进错误信息
                errors.append({'name': bk})
            else:
                books.append(bkobj) #存在则添加到books

        if errors:
            return JsonResponse({'status': 255, 'data': errors})
        webdata.pop('books')   #将书的信息排除掉
        auobj = self.model.objects.create(**webdata)  #将作者信息写数据库
        for bk in books:
            auobj.book2_set.add(bk)  #写作者与书的关联关系
        return JsonResponse({'status': 0})

    def put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        bookids = webdata.get('bookids') #取出前端传过来的书的ID

        auobj = self.model.objects.get(pk=pk)
        bkqs = Book2.objects.filter(id__in=json.loads(bookids)) #取出前端传过来的书
        auobj.book2_set.set(bkqs)  #修改作者与书的关系

        webdata.pop('bookids') #从webData中移除book相关信息
        self.model.objects.filter(pk=pk).update(**webdata) #修改作者基本信息
        return JsonResponse({'status':0})

    def delete(self,request, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.get(id=pk).delete()
        return JsonResponse({'status':0})
