# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import *
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from django.utils.decorators import method_decorator  #装饰器装饰类
from datetime import datetime
from django.http import QueryDict
from page import JuncheePaginator  #使用重写后的分面
from django.db.models import Q
from django.forms import model_to_dict

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

def index1(request):
    return render(request,'index.html')

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
    model = Author #读取哪个表
    template_name = 'app2/authors.html'  #前端模板名称
    context_object_name = 'authors'  #前端页面循环进读取的变量
    # paginate_by = 5  #分页数据，每页多少条
    #
    # def get_context_data(self, **kwargs):
    #     context = super(authorlist, self).get_context_data(**kwargs) #生成分页数据
    #     context['job'] = 'pythoner'
    #     return context

    def get_queryset(self,search): #按条件查询，默认是返回所有，可以生写，根据条件返回数据
        qs = self.model.objects.order_by('-id')
        if search:
            qs = qs.filter(Q(name__contains=search)|Q(address__contains=search))
        return  qs

    def get(self, request, *args, **kwargs):  #如果请求url带ID，则显示单用户信息，如果不带id则显示所有用户信息
        pk = kwargs.get('pk')
        if pk:
            obj = self.model.objects.get(id=pk)
            data = model_to_dict(obj, exclude=[])
            return JsonResponse({'status':0, 'data':data})
        else:
            page_num = request.GET.get('page', 1)
            search = request.GET.get('search')
            qs = self.get_queryset(search)
            pageobj = JuncheePaginator(qs)
            wdata = pageobj.pagecomputer(page_num)
            return render(request, self.template_name,{'authors': wdata[0], 'allpages': wdata[1], 'search':search})

    def post(self, request, *args, **kwargs):
        # name = request.POST.get('name')
        # phone = request.POST.get('phone')
        # address = request.POST.get('address')
        #
        # Author.objects.create(name=name,phone=phone,address=address)
        #
        # #等价于
        # #Author.objects.create(**QueryDict(request.body).dict())
        self.model.objects.create(**QueryDict(request.body).dict())
        return JsonResponse({'status':0})

    def put(self, request,*args,**kwargs):
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**QueryDict(request.body).dict())
        return JsonResponse({'status': 0})

    def delete(self,request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.get(id=pk).delete()
        return JsonResponse({'status':0})


    @method_decorator(login_required) #只作用于该方法
    def test(self):
        pass

class authorDetail(DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'app2/author.html'
    def get_context_data(self, **kwargs):
        kwargs['timenow'] = datetime.now()
        return super(authorDetail, self).get_context_data(**kwargs)


    def post(self, request, *args, **kwargs):
        # name = request.POST.get('name')
        # phone = request.POST.get('phone')
        # address = request.POST.get('address')
        #
        # Author.objects.create(name=name,phone=phone,address=address)
        #
        # #等价于
        # #Author.objects.create(**QueryDict(request.body).dict())
        self.model.objects.create(**QueryDict(request.body).dict())
        return JsonResponse({'status':0})

    def put(self, request,*args,**kwargs):
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(**QueryDict(request.body).dict())
        return JsonResponse({'status': 0})

    def delete(self,request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.get(id=pk).delete()
        return JsonResponse({'status':0})