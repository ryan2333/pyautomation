# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def hello(request):
    return HttpResponse("hello django")

def helloNumber(request,id): #隐式参数获取
    print id
    return HttpResponse(id)

def add(request, n1,n2):
    c = int(n1) + int(n2)
    return HttpResponse(c)

def add1(request,**kwargs): #显示参数获取
    n1 = kwargs.get('n1')
    n2 = kwargs.get('n2')
    sum = int(n1)+int(n2)
    return HttpResponse("%s + %s = %d" %(n1,n2,sum))

def argstest(request): #get请求参数获取
    n1 = request.GET.get('n1')
    n2 = request.GET.get('n2')
    sum = int(n1)+int(n2)
    return JsonResponse({"n1":n1, "n2":n2, "sum":sum})

# def index1(request):
#     return render(request,'index2.html')
