#-*- coding: utf-8 -*-

from django.http import HttpResponse

def indexpage(request):
    indexpage='''
        <div style="margin-left:100px">
        <br /><br /><br />
        <a href="/myapp/index/"><b>myapp</b></a>
        </div>
    '''
    return HttpResponse(indexpage)