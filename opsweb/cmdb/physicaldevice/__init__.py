#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import JsonResponse, HttpResponseRedirect, QueryDict
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.conf import settings
from cmdb.models import PhysicalDevice, AssetVendor, AssetIDC, AssetCategory
from cmdb.forms import PhysicalDeviceForm
from dashboard.models import UserProfile

# Create your views here.

class AssetCab(View):
    model = AssetIDC

    def post(self, request):
        idc_id = self.request.POST.get('idcid', '')
        idcobj = self.model.objects.get(id=idc_id)
        cab = idcobj.rental_pods.split(',')
        cabs = [i.strip() for i in cab]
        return JsonResponse({'status':0, 'cabs':cabs})


class physicalListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = PhysicalDevice
    template_name = 'cmdb/physical_list.html'
    context_object_name = 'physical_list'
    paginate_by = 10
    keyword = ''

    def get_queryset(self):
        queryset = super(physicalListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword)|
                                       Q(vendor__icontains=self.keyword)|
                                       Q(mgrip__icontains=self.keyword)|
                                       Q(purchase_date__icontains=self.keyword)|
                                       Q(sn__icontains=self.keyword)
                                       )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(physicalListView, self).get_context_data(**kwargs)
        context['category'] = AssetCategory.objects.all()
        context['asset_idc'] = AssetIDC.objects.all()
        context['asset_admin'] = UserProfile.objects.all()
        context['keyword'] = self.keyword
        return context

    def post(self, request):
        form = PhysicalDeviceForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '物理设备添加成功'}
        else:
            res = {'code': 1, 'errmsg': form.errors}
            print form.errors
        return JsonResponse(res, safe=True)


class physicalDetailView(LoginRequiredMixin, DetailView):
    model = PhysicalDevice
    template_name = 'cmdb/physicaldevice_detail.html'
    context_object_name = 'device'
    next_url = '/cmdb/physicallist/'

    def get_context_data(self, **kwargs):
        context = super(physicalDetailView, self).get_context_data(**kwargs)
        context['vendor'] = AssetVendor.objects.all()
        context['category'] = AssetCategory.objects.all()
        context['asset_idc'] = AssetIDC.objects.all()
        context['asset_admin'] = UserProfile.objects.all()
        idcname = context['object'].asset_idc #取出设备对应的IDC
        context['asset_cabs'] = cabs = self.get_cabs(idcname) #根据对应的IDC，返回租用的机柜
        return context

    def get_cabs(self, asset_idc):
        idcobj = AssetIDC.objects.get(name=asset_idc)
        cab = idcobj.rental_pods.split(',')
        cabs = [i.strip() for i in cab]
        return cabs

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = PhysicalDeviceForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '更新设备成功', 'next_url': self.next_url}
        else:
            res = {'code': 1, 'errmsg': form.errors, 'next_url': self.next_url}

        return render(request, settings.JUMP_PAGE, res)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            pdobj = self.model.objects.get(pk=pk)
            pdobj.delete()
            res = {'code': 0, 'result': '设备删除成功'}
        except:
            res = {'code': 1, 'errmsg': '该设备不存在'}
        return JsonResponse(res, safe=True)