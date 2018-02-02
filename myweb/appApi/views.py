#-*- coding:utf-8 -*-

from models import Myusers
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer   #序列器
from rest_framework import status
from rest_framework import mixins, generics

class testapi(APIView): #不带分页功能
    url_pk = 'pk'
    ckmodel = Myusers
    serializer_class = TaskSerializer


    def get(self,request,*args,**kwargs):
        pk = kwargs.get(self.url_pk)

        if pk: #取单条数据
            s = self.serializer_class(self.ckmodel.objects.get(pk=pk)) #序列化
            return Response(s.data)
        else: #取所有数据
            qs = self.ckmodel.objects.all()
            s = self.serializer_class(qs, many=True)  #序列化所有数据，需要加many=True参数
            return Response(s.data)

    def post(self,request,*args,**kwargs):  #POST请求
        s = self.serializer_class(data = request.data)  #反序列化
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, *args, **kwargs):
        obj = Myusers.objects.get(pk=kwargs.get('pk'))
        s = self.serializer_class(obj,data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_202_ACCEPTED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class testapi1(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin, generics.GenericAPIView): #带分页功能
    url_pk = 'pk'
    ckmodel = Myusers
    serializer_class = TaskSerializer
    #queryset = ckmodel.objects.all()  #此处变量名必须为queryset,并且只能写到此处，或者写一个get_queryset方法

    def get_queryset(self):
        return self.ckmodel.objects.all()


    def get(self,request,*args,**kwargs):
        pk = kwargs.get(self.url_pk)
        if pk: #取单条数据
            return self.retrieve(request, *args,**kwargs)
        else: #取所有数据
            return self.list(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):  #POST请求
        s = self.serializer_class(data = request.data)  #反序列化
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, *args, **kwargs):
        obj = Myusers.objects.get(pk=kwargs.get('pk'))
        s = self.serializer_class(obj,data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_202_ACCEPTED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)