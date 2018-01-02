#-*-coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def mylogin(request):
    if request.method == 'GET':
        return render(request,'pages/examples/login.html')
    if request.method == 'POST':
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
def index1(request):
    return render(request, 'index2.html')