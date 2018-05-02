#-*- coding: utf-8 -*-

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, Http404
from dashboard.forms import UserForm
from dashboard.models import UserProfile
from datetime import datetime

#自定义模块导入

from django.conf import settings
from pure_pagination.mixins import PaginationMixin
import traceback, json, logging



class UserListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = UserProfile
    template_name = 'dashboard/user_list.html'
    context_object_name = 'userlist'
    paginate_by = 10
    keyword=''

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset(name__icontains=self.keyword)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        # context['all_content_type'] = ContentType.objects.all()
        return context

    def post(self, request):
        webdata = QueryDict(request.body).dict()
        webdata['password'] = make_password(webdata['password'])

        if webdata['password'].strip() == 0:
            res = {'code':1, 'errmsg': '密码不能为空', 'next_url': self.next_url}
            return JsonResponse(res, safe=True)

        try:
            self.model.objects.create(**webdata)
        except BaseException:
            res = {'code':255, 'errmsg':"帐号添加失败", 'next_url': self.next_url}
        else:
            res = {'code':0, 'result': "帐号添加成功", 'next_url': self.next_url}

        # form = UserForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     res = {'code': 0, 'result': '添加用户成功'}
        # else:
        #     # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
        #     res = {'code': 1, 'errmsg': form.errors}
            # logging.error("add user error: %s" % traceback.format_exc())
        # return JsonResponse(res, safe=True)
        return JsonResponse(res, safe=True)


class UserDetailView(LoginRequiredMixin, DetailView):
        '''
        动作：getone, update, delete
        '''
        model = UserProfile
        template_name = "dashboard/user_edit.html"
        context_object_name = 'user'
        next_url = '/dashboard/userlist/'

        def get_context_data(self, **kwargs):
            context = super(UserDetailView, self).get_context_data(**kwargs)
            return context

        def post(self, request, *args, **kwargs):
            webdata = QueryDict(request.body).dict()

            try:
                self.model.objects.filter(id=kwargs.get('pk')).update(**webdata)
                res = {'code': 0, 'next_url': self.next_url, 'result': '用户更新成功'}
            except:
                res = {"code": 1, "errmsg": '用户更新失败'}
                logging.error("update role error: %s" % traceback.format_exc())

            return JsonResponse(res, safe=True)


        def delete(self, request, *args, **kwargs):
            pk = kwargs.get('pk')
            print pk
            # 通过出版社对象查所在该出版社的书籍，如果有关联书籍不可以删除，没有关联书籍可以删除
            try:
                obj = self.model.objects.get(pk=pk)
                if not obj.groups.all() and not obj.user_permissions.all():
                    self.model.objects.filter(pk=pk).delete()
                    res = {"code": 0, "result": "删除用户成功"}

                else:
                    res = {"code": 1, "errmsg": "该用户还存在组或个人权限,请联系管理员"}
                    logging.error("delete role error: %s" % traceback.format_exc())
            except:
                res = {"code": 1, "errmsg": "删除错误请联系管理员"}
                logging.error("delete role error: %s" % traceback.format_exc())
            return JsonResponse(res, safe=True)


class ChangeUserPwd(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'dashboard/change_passwd.html'
    context_object_name = 'user'
    next_url = '/dashboard/userlist/'

    def get_context_data(self, **kwargs):
        context = super(ChangeUserPwd, self).get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        print webdata
        if webdata['password1'] == webdata['password2'] and len(webdata['password1']) != 0:
            try:
                self.model.objects.filter(pk=webdata['uid']).update(password=make_password(webdata['password1']))
                res = {'code': 0, 'result': '密码修改成功', 'next_url': self.next_url}
            except BaseException,e:
                res = {'code': 1, 'errmsg': '密码修改失败', 'next_url': self.next_url}
                print e
        else:
            res = {'code':1, 'errmsg': '两次输入密码不一致', 'next_url': self.next_url}

        print res
        # return JsonResponse(res, safe=True)
        return render(request, settings.JUMP_PAGE, res)


class ChangePermissionView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'dashboard/user_group_power.html'
    context_object_name = 'user'
    next_url = '/dashboard/userlist/'

    def get_context_data(self, **kwargs):
        context = super(ChangePermissionView, self).get_context_data(**kwargs)
        context['user_has_groups'] = self.get_user_has_group()
        context['user_not_groups'] = self.get_user_not_group(context['user_has_groups'])
        context['user_has_permissions'] = self.get_user_has_permission()
        context['user_not_permissions'] = self.get_user_not_permission(context['user_has_permissions'])
        return context


    def get_user_has_group(self):
        pk = self.kwargs.get('pk')
        group = self.model.objects.get(pk=pk).groups.all()
        return group

    def get_user_not_group(self, usergroups):
        group = Group.objects.all()

        groups = [g for g in group if g not in usergroups]
        return groups

    def get_user_has_permission(self):
        pk = self.kwargs.get('pk')
        perms = self.model.objects.get(pk=pk).user_permissions.all()
        return perms

    def get_user_not_permission(self, perm):
        ps = Permission.objects.all()
        perms = [p for p in ps if p not in perm ]
        return perms

    def post(self, request, **kwargs):
        group_id_list = request.POST.getlist('groups_selected', [])
        perm_id_list = request.POST.getlist('perms_selected')
        pk = request.POST.get('uid')
        print pk
        user = self.model.objects.get(pk=request.POST.get('uid'))
        print user, group_id_list, perm_id_list
        try:
            user.groups.set(group_id_list)
            user.user_permissions.set(perm_id_list)
            user.save()
            res = {'code': 0, 'result': '用户权限修改成功', 'next_url': self.next_url}
        except BaseException, e:
            print e
            res = {'code':1, 'errmsg': e, 'next_url': self.next_url}

        # return JsonResponse(res, safe=True)
        return render(request, settings.JUMP_PAGE, res)



