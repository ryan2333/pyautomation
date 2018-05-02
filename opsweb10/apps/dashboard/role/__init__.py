#-*- coding: utf-8 -*-

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.http import JsonResponse,QueryDict
from django.shortcuts import render, Http404
from dashboard.forms import GroupForm
from dashboard.models import UserProfile

#自定义模块导入

from django.conf import settings
from pure_pagination.mixins import PaginationMixin
import traceback, json, logging



class GroupListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Group
    template_name = 'dashboard/group_list.html'
    context_object_name = 'grouplist'
    paginate_by = 10
    keyword=''

    def get_queryset(self):
        queryset = super(GroupListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset(name__icontains=self.keyword)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        # context['all_content_type'] = ContentType.objects.all()
        return context

    def post(self, request):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加组成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
            logging.error("add role error: %s" % traceback.format_exc())
        return JsonResponse(res, safe=True)


class GroupDetailView(LoginRequiredMixin, DetailView):
        '''
        动作：getone, update, delete
        '''
        model = Group
        template_name = "dashboard/group_edit.html"
        context_object_name = 'group'
        next_url = '/dashboard/grouplist/'

        def get_context_data(self, **kwargs):
            context = super(GroupDetailView, self).get_context_data(**kwargs)
            context['group_has_permissions'] = self.get_group_has_permissions()
            context['group_not_permissions'] = self.get_group_not_permissions(context['group_has_permissions'])
            return context

        def get_group_has_permissions(self):
            pk = self.kwargs.get('pk')
            try:
                group = Group.objects.get(pk=pk)
                return group.permissions.all()
            except Group.DoesNotExist:
                raise Http404

        def get_group_not_permissions(self, grouppermissions):
            try:
                all_perms = Permission.objects.all()
                perms = [perm for perm in all_perms if perm not in grouppermissions]
                return perms
            except:
                raise Http404

        def post(self, request, *args, **kwargs):
            permission_id_list = request.POST.getlist('perms_selected',[])
            gid = request.POST.get('gid')
            name = request.POST.get('name')

            try:
                group = self.model.objects.get(pk=gid)
                group.permissions = permission_id_list
                group.name = name
                group.save()
                res = {'code': 0, 'next_url': self.next_url, 'result': '组更新成功'}
            except:
                res = {"code": 1, "errmsg": '更新组失败', 'next_url': self.next_url}
                logging.error("update role error: %s" % traceback.format_exc())
            return render(request, settings.JUMP_PAGE, res)


        def delete(self, request, *args, **kwargs):
            pk = kwargs.get('pk')
            # 通过出版社对象查所在该出版社的书籍，如果有关联书籍不可以删除，没有关联书籍可以删除
            try:
                obj = self.model.objects.get(pk=pk)
                if not obj.user_set.all():
                    self.model.objects.filter(pk=pk).delete()
                    res = {"code": 0, "result": "删除组成功"}
                else:
                    res = {"code": 1, "errmsg": "该权限被调用,请联系管理员"}
                    logging.error("delete role error: %s" % traceback.format_exc())
            except:
                res = {"code": 1, "errmsg": "删除错误请联系管理员"}
                logging.error("delete role error: %s" % traceback.format_exc())
            return JsonResponse(res, safe=True)

class GroupUsersView(LoginRequiredMixin, View):
    def get(self, request):
        pk = request.GET.get('gid', None)
        try:
            group = Group.objects.get(pk=pk)
        except BaseException,e:
            print e
            return JsonResponse([], safe=False)

        users = group.user_set.all()
        # user_list = [{'username': user.username, 'name_cn':user.name_cn, 'email':user.email, 'id': user.id} for user in users]
        user_list = list(group.user_set.values('username', 'name_cn', 'email', 'id'))
        return JsonResponse(user_list, safe=False)

    def delete(self, request):
        data = QueryDict(request.body)
        try:
            group_obj = Group.objects.get(pk=data.get('groupid', ''))
            user_obj = UserProfile.objects.get(id=data.get("userid", ""))
            user_obj.groups.remove(group_obj)
            res = {'code': 0, 'result': '删除用户成功'}
        except UserProfile.DoesNotExist:
            res = {'code': 1, 'errmsg': '用户不存在'}

        return JsonResponse(res)


