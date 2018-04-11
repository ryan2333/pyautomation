#-*- coding: utf-8 -*-

from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

@login_required
def index(request):
    loginuser = request.user
    return render(request, 'index.html',{'loginuser': loginuser})

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

class mylogin1(TemplateView):#mylogin登陆的TemplateView类视图
    template_name = 'pages/examples/login.html'

    def get_context_data(self, **kwargs):
        nexturl = self.request.GET.get('next','/')
        return {'nexturl': nexturl}

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