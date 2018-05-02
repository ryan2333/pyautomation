# _*_ coding: utf-8 _*_

from django import forms
from django.contrib.auth.models import Group, Permission
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class UserProfileForm(forms.Form):
    username = forms.CharField(required=True, max_length=30)
    name_cn = forms.CharField(required=True, max_length=30)
    phone = forms.CharField(required=True, max_length=11)
    email = forms.EmailField(required=True, max_length=20)


class PermForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'


class PermUpdateForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['codename','name']
        #fields = '__all__'

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'