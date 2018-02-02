#-*- coding: utf-8 -*-

from rest_framework import serializers
from .models import *

# class AccountSerializer(serializers.ModelSerializer):
#     books = serializers.SerializerMethodField()
#     class Meta:
#         model = Account
#         fields = ('id','account_name','users','created')
#         exclude = ()
#         fields = '__all__'
#
#     def get_books(self,obj):
#         return ""

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myusers
        fields = ('id','name')   #需要序列化的字段