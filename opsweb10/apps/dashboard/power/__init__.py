#-*- coding: utf-8 -*-

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import Permission, ContentType
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from dashboard.forms import PermForm, PermUpdateForm

#自定义模块导入

from django.conf import settings
from pure_pagination.mixins import PaginationMixin
import traceback, json, logging



class PermissionListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Permission
    template_name = 'dashboard/power_list.html'
    context_object_name = 'powerlist'
    paginate_by = 10
    keyword=''

    def get_queryset(self):
        queryset = super(PermissionListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset(Q(name__icontains=self.keyword)|Q(codename__icontains=self.keyword))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(PermissionListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        # context['all_content_type'] = ContentType.objects.all()
        return context

    def post(self, request):
        form = PermForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加权限成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
            logging.error("add power error: %s" % traceback.format_exc())
        return JsonResponse(res, safe=True)


class PermissionDetailView(LoginRequiredMixin, DetailView):
        '''
        动作：getone, update, delete
        '''
        model = Permission
        template_name = "dashboard/power_edit.html"
        context_object_name = 'power'
        next_url = '/dashboard/powerlist/'

        def get_context_data(self, **kwargs):
            context = super(PermissionDetailView, self).get_context_data(**kwargs)
            context['all_content_type'] = ContentType.objects.all()
            return context

        def post(self, request, *args, **kwargs):
            pk = kwargs.get('pk')
            p = self.model.objects.get(pk=pk)
            form = PermUpdateForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
                res = {"code": 0, "result": "更新权限成功", 'next_url': self.next_url}
            else:
                res = {"code": 1, "errmsg": '更新权限失败', 'next_url': self.next_url}
                logging.error("update power error: %s" % traceback.format_exc())
            return render(request, settings.JUMP_PAGE, res)
            # return HttpResponseRedirect(reverse('books:publish_detail',args=[pk]))

        def delete(self, request, *args, **kwargs):
            pk = kwargs.get('pk')
            # 通过出版社对象查所在该出版社的书籍，如果有关联书籍不可以删除，没有关联书籍可以删除
            try:
                obj = self.model.objects.get(pk=pk)
                if not obj.user_set.all() or not obj.group_set.all():
                    self.model.objects.filter(pk=pk).delete()
                    res = {"code": 0, "result": "删除权限成功"}
                else:
                    res = {"code": 1, "errmsg": "该权限被调用,请联系管理员"}
                    logging.error("delete power error: %s" % traceback.format_exc())
            except:
                res = {"code": 1, "errmsg": "删除错误请联系管理员"}
                logging.error("delete power error: %s" % traceback.format_exc())
            return JsonResponse(res, safe=True)
