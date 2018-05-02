#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse, HttpResponseRedirect, QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.conf import settings
from cmdb.models import AssetIDC
from cmdb.forms import AssetIDCForm

class IdcListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = AssetIDC
    template_name = 'cmdb/idc_list.html'
    context_object_name = 'idc_list'
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(IdcListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IdcListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request):
        form = AssetIDCForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '机房添加成功'}

        else:
            res = {'code': 1, 'errmsg': form.errors}
            print form.errors
        return JsonResponse(res, safe=True)


class IdcDetailView(LoginRequiredMixin, DetailView):
    model = AssetIDC
    template_name = 'cmdb/idc_detail.html'
    context_object_name = 'idc'
    next_url = '/cmdb/idclist/'

    def get_context_data(self, **kwargs):
        context = super(IdcDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = AssetIDCForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '更新机房成功', 'next_url': self.next_url}
        else:
            res = {'code': 1, 'errmsg': form.errors, 'next_url': self.next_url}

        return render(request, settings.JUMP_PAGE, res)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            idcobj = self.model.objects.get(pk=pk)
            if not idcobj.physicaldevice_set.all():
                idcobj.delete()
                res = {'code': 0, 'result': '机房删除成功'}
            else:
                res = {'code': 1, 'errmsg': '该机房有相关物理设备，请联系管理员'}
        except:
            res = {'code': 1, 'errmsg': '删除错误，请联系管理员'}
        return JsonResponse(res, safe=True)