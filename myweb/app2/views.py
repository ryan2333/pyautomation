# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import *
from django.views import View
from django.views.generic import TemplateView,ListView
from django.utils.decorators import method_decorator  #装饰器装饰类

# Create your views here.
@login_required
def hello(request): #类似于这种视图，称之为函数视图，简称fbv
    return HttpResponse("hello django")


class cbv(View):  #类似于这种视图，称之为类视图，简称cbv
    def get(self,request):
        return HttpResponse("hello class views")


class helloNumber(View):
    def get(self,request,id): #隐式参数获取,类视图
        return HttpResponse(id)

def add(request, n1,n2):
    c = int(n1) + int(n2)
    return HttpResponse(c)

def add1(request,**kwargs): #显示参数获取，函数视图
    n1 = kwargs.get('n1')
    n2 = kwargs.get('n2')
    sum = int(n1)+int(n2)
    return HttpResponse("%s + %s = %d" %(n1,n2,sum))

class argstest(View):
    def get(self,request): #get请求参数获取，类视图
        n1 = self.request.GET.get('n1')
        n2 = self.request.GET.get('n2')
        sum = int(n1)+int(n2)
        return JsonResponse({"n1":n1, "n2":n2, "sum":sum})

# def index1(request):
#     return render(request,'index2.html')

def bookQuery(request):  #使用queryset.values获取数据库书籍数据，返回Json字符串到前端
    data = [i for i in Book2.objects.all().values()]
    data1 = [i.todict for i in Book2.objects.all()]
    return JsonResponse({'status':0, 'data':data1})

def authorQuery(request):  #使用queryset.values获取数据库作者数据，返回Json字符串到前端
    qs = Author.objects.all() #取出所有作者
    qsfans = qs.order_by('-fans')[:2] #fans倒序排列
    qsincome = qs.order_by('-income')[:2]#income倒序排列
    qsret = list(set(qsfans).union(set(qsincome)))
    data1 = [i.todict for i in qsret]
    return JsonResponse({'status':0, 'data':data1})

@method_decorator(login_required, name='dispatch')  #装饰类的语法，作用于该类所有方法
class authorlist(ListView):
    model = Author
    template_name = 'app2/authors.html'
    context_object_name = 'authors'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(authorlist, self).get_context_data(**kwargs) #生成分页数据
        context['job'] = 'pythoner'
        return context

    def get_queryset(self):
        return self.model.objects.order_by('-id')

    @method_decorator(login_required) #只作用于该方法
    def test(self):
        pass