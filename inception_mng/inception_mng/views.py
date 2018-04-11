#-*- coding: utf-8 -*-
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render

# class mylogin(TemplateView):#mylogin登陆的TemplateView类视图
#     template_name = 'login.html'
#
#     def get_context_data(self, **kwargs):
#         nexturl = self.request.GET.get('next','/')
#         return super(mylogin, self).get_context_data(**kwargs)
#
#     def post(self,request):
#         name = request.POST.get('username')
#         password = request.POST.get('password')
#         testlogin = authenticate(username=name,password=password)
#         nexturl = request.POST.get('next', '/')
#         ret = {}
#         if testlogin is not None: #如果用户存在，则给他登陆
#             login(request,testlogin)
#             ret['status'] = 0
#             ret['next'] = nexturl
#         else:
#             ret['status'] = 255
#         print ret
#         return JsonResponse(ret)

class mylogin(TemplateView):
    template_name = 'login.html'
    def get_context_data(self, **kwargs):
        kwargs['next'] = self.request.GET.get('next','/')
        return super(mylogin, self).get_context_data(**kwargs)
    def post(self, request):
        uname = request.POST.get('username',None)
        passwd = request.POST.get('password',None)
        ret = {}
        user = authenticate(username=uname, password=passwd)  # django鉴权
        if user is not None:  # 用户密码及token正确
            login(request, user)
            next = request.get_full_path()
            ret['status'] = 0
            ret['next'] = next
        else:
            ret['status'] = 1
        print ret
        return JsonResponse(ret)


class mylogout(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/?next=/')


def myindex(request):
    return render(request, "index.html")