#-*- coding: utf-8 -*-
from django.views.generic import ListView
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.http import request, Http404


class CklistView(ListView):
    '''对get_queryset,get_context_data, get方法重写'''

    context_object_name = None #前端模板变量为users，用于模板循环显示
    template_name = None  #渲染前端的模板名
    ckmodel = None
    paginate_by = 10 #分页中每一页显示的记录条目数
    pk_url_kwarg = 'pk'
    souword = 'souward'
    orderkey = '-id'


    def get_queryset(self):
        objectsdata = self.ckmodel.objects.all().order_by(self.orderkey)
        souword = self.request.GET.get(self.souword)
        if souword:
            objectsdata = objectsdata.filter(Q(name__contains=souword)|Q(note__contains=souword))

        return objectsdata

    def get_object(self,pk):
        try:
            oneObj = self.ckmodel.objects.get(pk=pk)
        except self.ckmodel.DoesNotExist:
            data = None
            status = -1
        else:
            data = model_to_dict(oneObj)
            status = 0
        return {'data':data, 'status': status}

    def get_context_data(self, **kwargs):
        context = super(CklistView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        is_empty = None
        if pk:  #请求单用户数据
            ret = self.get_object(pk)
            return JsonResponse(ret)
        else: #请求所有用户数据
            self.object_list = self.get_queryset()
            allow_empty = self.get_allow_empty()

        if not allow_empty:
            if (self.get_paginate_by(self.object_list) is not None
                and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404("Empty list and '%(class_name)s.allow_empty' is False." %{'class_name':self.__class__.__name__})
        context = self.get_context_data()
        return self.render_to_response(context)