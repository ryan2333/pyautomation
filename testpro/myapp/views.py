# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, request

from django.shortcuts import render

# Create your views here.

from base import CklistView
from models import *

class index(CklistView):
    context_object_name = 'users'
    template_name = 'index.html'
    ckmodel = Myusers

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['testname'] = 'chenkun1998'
        context['testjob'] = 'Linux'
        context['len'] = len(self.object_list)
        return context