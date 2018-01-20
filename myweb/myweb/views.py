#-*-coding:utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView


@login_required
def index1(request):
    return render(request, 'index2.html')

class hello(TemplateView):
    template_name = "hello.html"
    #返回额外的变量渲染到页面
    def get_context_data(self, **kwargs): #重写get_context_data
        context = super(hello,self).get_context_data(**kwargs) #执行父类hello里的get_context_data方法
        context['username'] = '韩寒'
        context['lans'] = ['python','nginx','golang']
        return context

# def mylogin(request): #mylogin登陆的函数视图
#     if request.method == 'GET':
#         nexturl = request.GET.get('next','/')
#         return render(request,'pages/examples/login.html', {'nexturl': nexturl})  #登陆后跳转到指定url
#     if request.method == 'POST':
#         name = request.POST.get('username')
#         password = request.POST.get('password')
#         testlogin = authenticate(username=name,password=password)
#         ret = {}
#         if testlogin is not None: #如果用户存在，则给他登陆
#             login(request,testlogin)
#             ret['status'] = 0
#         else:
#             ret['status'] = 255
#     print ret
#     return JsonResponse(ret)

class mylogin(View):#mylogin登陆的类视图
    def get(self,request):
        nexturl = request.GET.get('next','/')
        return render(request,'pages/examples/login.html', {'nexturl': nexturl})  #登陆后跳转到指定url
    def post(self,request):
        name = request.POST.get('username')
        password = request.POST.get('password')
        testlogin = authenticate(username=name,password=password)
        ret = {}
        if testlogin is not None: #如果用户存在，则给他登陆
            login(request,testlogin)
            ret['status'] = 0
        else:
            ret['status'] = 255
        print ret
        return JsonResponse(ret)


@login_required
def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/login')