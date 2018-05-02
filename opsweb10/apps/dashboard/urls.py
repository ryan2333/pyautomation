#-*- coding: utf-8 -*-

from django.conf.urls import url
from dashboard import power, role, users

urlpatterns = [

    url(r'^powerlist/?$', power.PermissionListView.as_view(), name='power_list'),
    url(r'^powerdetail/(?P<pk>\d+)?/?$', power.PermissionDetailView.as_view(), name="power_detail"),

    url(r'^grouplist/?$', role.GroupListView.as_view(), name='role_list'),
    url(r'^groupdetail/(?P<pk>\d+)?/?$', role.GroupDetailView.as_view(), name="role_detail"),
    url(r'^groupusers/?$', role.GroupUsersView.as_view(), name="group_users"),

    url(r'^userlist/?$', users.UserListView.as_view(), name='user_list'),
    url(r'^userdetail/(?P<pk>\d+)?/?$', users.UserDetailView.as_view(), name="user_detail"),
    url(r'^modifypwd/(?P<pk>\d+)?/?$', users.ChangeUserPwd.as_view(), name='modify_pwd'),
    url(r'^usergrouppower/(?P<pk>\d+)?/?$', users.ChangePermissionView.as_view(), name='user_group_power'),

]