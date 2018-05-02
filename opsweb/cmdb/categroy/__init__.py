#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, QueryDict
from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from cmdb.models import AssetCategory
from cmdb.forms import AssetCategoryForm

class AssetCategoryListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = AssetCategory
    template_name = 'cmdb/category_list.html'
    context_object_name = 'category_list'
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(AssetCategoryListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AssetCategoryListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request):
        form = AssetCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '设备类别添加成功'}

        else:
            res = {'code': 1, 'errmsg': form.errors}
            print form.errors
        return JsonResponse(res, safe=True)


class AssetCategoryDetailView(LoginRequiredMixin, DetailView):
    model = AssetCategory
    template_name = 'cmdb/category_detail.html'
    context_object_name = 'category'
    next_url = '/cmdb/assetcategorylist/'

    def get_context_data(self, **kwargs):
        context = super(AssetCategoryDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = AssetCategoryForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '更新类别成功', 'next_url': self.next_url}
        else:
            res = {'code': 1, 'errmsg': form.errors, 'next_url': self.next_url}

        return render(request, settings.JUMP_PAGE, res)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            categoryobj = self.model.objects.get(pk=pk)
            if not categoryobj.physicaldevice_set.all():
                categoryobj.delete()
                res = {'code': 0, 'result': '设备类别删除成功'}
            else:
                res = {'code': 1, 'errmsg': '该类别有相关物理设备，请联系管理员'}
        except:
            res = {'code': 1, 'errmsg': '删除错误，请联系管理员'}
        return JsonResponse(res, safe=True)