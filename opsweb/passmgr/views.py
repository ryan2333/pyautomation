# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from models import *
from django.views.generic import ListView,DetailView,View
from pymkAes import prpcrypt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse,QueryDict
from django.db.models import Q
import datetime

# Create your views here.
class pyaes(object):
    pc = prpcrypt('Czmfbcuw46FtsaOgtrtVn?az96sjiw5R')

    def myencrypt(self, arg):
        if arg:
            arg = self.pc.encrypt(arg)
        return arg


    def mydecrypt(self, arg):
        if arg:
            arg = self.pc.decrypt(arg)
        return arg

@method_decorator(login_required, name='dispatch')
class passList(ListView):
    model = passmgr
    template_name = 'passmgr/passwds.html'
    paginate_by = 10
    context_object_name = 'passwds'
    p = pyaes()
    souword = ''
    # def get_context_data(self, **kwargs):
    #     context = super(passList, self).get_context_data(**kwargs)
    #     for i in context['object_list']:
    #         i.password=self.p.mydecrypt(i.password)
    #         i.bpasswd1 = self.p.mydecrypt(i.bpasswd1)
    #         i.bpasswd2 = self.p.mydecrypt(i.bpasswd2)
    #         i.bpasswd3 = self.p.mydecrypt(i.bpasswd3)
    #     return context

    def get_queryset(self):
        qs = self.model.objects.all()
        souword = self.request.GET.get('souword')
        if souword:
            qs = qs.filter(Q(host__contains=souword)|Q(account__contains=souword))
        for i in qs:
            i.password = self.p.mydecrypt(i.password)
            i.bpasswd1 = self.p.mydecrypt(i.bpasswd1)
            i.bpasswd2 = self.p.mydecrypt(i.bpasswd2)
            i.bpasswd3 = self.p.mydecrypt(i.bpasswd3)
        return qs

    def get_context_data(self, **kwargs):
        context = super(passList, self).get_context_data(**kwargs)
        context['souword'] = self.souword
        return context


@method_decorator(login_required, name='dispatch')
class passApi(View):
    p = pyaes()
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        passobj = passmgr.objects.get(pk=pk)
        data = passobj.todict
        data['password'] = self.p.mydecrypt(data['password'])
        data['bpasswd1'] = self.p.mydecrypt(data['bpasswd1'])
        data['bpasswd3'] = self.p.mydecrypt(data['bpasswd3'])
        data['bpasswd2'] = self.p.mydecrypt(data['bpasswd2'])
        data['timenow'] = datetime.datetime.now()
        return render(request,'passmgr/passwd.html',{'passmgr':data})


@method_decorator(login_required, name='dispatch')
class passDetail(DetailView):
    model = passmgr
    template_name = "passmgr/passwd.html"
    context_object_name = 'passmgr'

    p = pyaes()

    def get_context_data(self, **kwargs):
        context = super(passDetail, self).get_context_data(**kwargs)
        # context['password'] = self.p.mydecrypt(context['password'])
        # context['bpasswd1'] = self.p.mydecrypt(context['bpasswd1'])
        # context['bpasswd3'] = self.p.mydecrypt(context['bpasswd3'])
        # context['bpasswd2'] = self.p.mydecrypt(context['bpasswd2'])
        return context

    def post(self,request, **kwargs):
        errors = []
        passdata = QueryDict(request.body).dict()

        if not passdata['password'] or not passdata['bpasswd1'] or not passdata['bpasswd2'] or not passdata['bpasswd3'] :
            errors.append('密码不能为空')
            return JsonResponse({'status': 255, 'resdata': errors})

        passdata['password'] = self.p.myencrypt(passdata['password'])
        passdata['bpasswd1'] = self.p.myencrypt(passdata['bpasswd1'])
        passdata['bpasswd2'] = self.p.myencrypt(passdata['bpasswd2'])
        passdata['bpasswd3'] = self.p.myencrypt(passdata['bpasswd3'])


        try:
            self.model.objects.create(**passdata)
        except BaseException:
            return JsonResponse({'status':255, 'resdata':"帐号添加失败"})
        else:
            return JsonResponse({'status':0, 'resdata': "帐号添加成功"})

    def put(self,request, **kwargs):
        errors = []
        passdata = QueryDict(request.body).dict()

        if not passdata['password'] or not passdata['bpasswd1'] or not passdata['bpasswd2'] or not passdata['bpasswd3']:
            errors.append('密码不能为空')
            return JsonResponse({'status': 255, 'resdata': errors})

        passdata['password'] = self.p.myencrypt(passdata['password'])
        passdata['bpasswd1'] = self.p.myencrypt(passdata['bpasswd1'])
        passdata['bpasswd2'] = self.p.myencrypt(passdata['bpasswd2'])
        passdata['bpasswd3'] = self.p.myencrypt(passdata['bpasswd3'])
        pk = kwargs.get('pk')
        try:
            passobj = self.model.objects.filter(pk=pk).update(**passdata)

        except BaseException:
            return JsonResponse({'status': 255})
        else:
            return JsonResponse({'status': 0})

    def delete(self,request, **kwargs):
        pk = kwargs.get('pk')
        try:
            passobj = self.model.objects.get(pk=pk).delete()
        except BaseException:
            return JsonResponse({'status': 255})
        else:
            return JsonResponse({'status':0})