# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import ListView,DetailView,TemplateView,View
from django.http import JsonResponse, QueryDict
from inception import table_structure, getbak
from models import *
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(login_required, name='dispatch')
class InceptionCommit(TemplateView):
    template_name = 'sqlmng/inception_commit.html'

    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        username = request.user.get_username()
        #dbname, env, sqlcontent, not
        dbname = webdata.get('dbname')
        env = webdata.get('env')
        sqlcontent = webdata.get('sqlcontent')
        dbobj = model_to_dict(DBConf.objects.get(name=dbname,env=env))
        dbhost = dbobj['host']
        dbuser = dbobj['user']
        dbpasswd = dbobj['password']
        dbport = dbobj['port']
        dbinfo = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-check;' %(dbuser,dbpasswd,dbhost, dbport)
        sql_review = table_structure(dbinfo, dbname, sqlcontent)
        for perrz in sql_review:
            if perrz[4] != "None":
                return JsonResponse({'status':-2, 'msg':perrz[4]})
        #检测sql，保存正常的sql
        userobj = User.objects.get(username=request.user)
        webdata['commiter'] = username
        # # webdata['treater'] = username
        # treater=webdata['treater']
        treaterobj = User.objects.get_or_create(username=webdata['treater'])[0]
        sqlobj = InceptSql.objects.create(**webdata)
        sqlobj.sqluser.add(userobj,treaterobj)  #绑定提交人，执行人
        return JsonResponse({'status':0})


class DBConfig(ListView):
    model = DBConf
    template_name = 'sqlmng/dbconfig.html'
    paginate_by = 10
    context_object_name = 'res_data'
    # def get(self, request, **kwargs):
    #     res_data = self.model.objects.all()
    #     return render(request, self.template_name, {'res_data':res_data})

    def get_queryset(self):

        qs = self.model.objects.all()
        souword = self.request.GET.get('souword') #搜索过滤

        if souword:
           qs =  qs.filter(name__contains=souword)
        return qs



    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        name = webdata.get('name')
        env = webdata.get('env')
        host = webdata.get('host')
        dbobj = self.model.objects.filter(name=name,env=env,host=host)
        if dbobj:
            return JsonResponse({'status': -1})
        self.model.objects.create(**webdata)
        return JsonResponse({'status': 0})

    def put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        dbobj = self.model.objects.filter(pk=pk)
        dbobj.update(**webdata)
        return JsonResponse({'status':0})

    def delete(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.get(pk=pk).delete()
        return JsonResponse({'status': 0})


class AutoSelect(View):
    model = DBConf
    def post(self, request):
        webdata = QueryDict(request.body).dict()
        env = webdata.get('env')
        dbs = [obj.name for obj in self.model.objects.filter(env=env)]
        #根据用户的身份，返回执行人数据：研发返回他的经理， 经理以上返回自己
        userobj = request.user
        role = userobj.userprofile.role
        mngs = [userobj.username]

        if userobj.is_superuser:
            return JsonResponse({'status': 0, 'dbs': dbs, 'mngs': mngs})

        if env == '1' and role == '3':
                ug = userobj.groups.first()
                if ug:
                    mngs = [ u.username for u in ug.user_set.all() if u.userprofile.role == '2']
        else:
            mngs = [userobj.username]
        return JsonResponse({'status':0,'dbs':dbs, 'mngs': mngs})

class inception_result(ListView):
    template_name = 'sqlmng/inception_result.html'
    paginate_by = 5
    model = InceptSql
    dbmodel = DBConf
    context_object_name = 'res_data'
    exe_time = 0
    affected_rows = 0

    def get_queryset(self):
        # 根据用户身份，返回相关的sql
        userobj = self.request.user
        role = userobj.userprofile.role
        if userobj.is_superuser:  # 管理员，返回所有sql
            return self.model.objects.all()

        if role == '1':  # 总监，返加他组内所有人的Sql
            qs = userobj.inceptsql_set.all()
            g = userobj.groups.first()
            for u in g.user_set.all():
                uqs = u.inceptsql_set.all()
                qs = qs | uqs
        else: #研发或经理
            qs = userobj.inceptsql_set.all()
        return qs

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        activetype = kwargs.get('actiontype')
        sqlobj = self.model.objects.get(pk=pk)
        res_data = {'status':0}
        #根据id获取sql内容，执行
        if activetype == 'execute':
            sqlcontent = sqlobj.sqlcontent
            dbobj = self.dbmodel.objects.get(name=sqlobj.dbname)
            dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-execute;' %(dbobj.user, dbobj.password, dbobj.host, dbobj.port)
            exerz = table_structure(dbaddr, sqlobj.dbname, sqlcontent) #此处已经对SQL语句执行完成
            opidlist = []

            for i in exerz:  #分析执行结果
                resultCode = i[4]
                if resultCode != None:
                    sqlobj.status = 2
                    res_data['status'] = -1
                    break
                else:
                    opidlist.append(i[7])
                    self.affected_rows += i[6]
                    self.exe_time += float(i[9])
                    sqlobj.status = 0
                    res_data['status'] = 0
                    sqlobj.rollbackdb = i[8]
                    sqlobj.status = 0

            sqlobj.rollbackopid = opidlist
        if activetype == "rollback":
            rollbackopid = sqlobj.rollbackopid  #获取sql的回滚id集合
            rollbackdb = sqlobj.rollbackdb

            #获取回滚语句
            backsqls = ''
            for opid in eval(rollbackopid)[1:]:
                #对每个回滚id，在$_$Inception_backup_infomation$_$里获取它操作的表
                sql = 'select tablename from $_$Inception_backup_information$_$ where opid_time=%s' % (opid)
                baktable = getbak(sql, rollbackdb)[0][0]
                #每个回滚id获取到的回滚语句(可能是多条)
                rollbacksql = 'select rollback_statement from %s where opid_time = %s' % (baktable, opid)
                perback = getbak(rollbacksql, rollbackdb)  #每条语句的回滚结果
                for baksql in perback:
                    #对可能多条的回滚语句，取出每一个
                    backsqls += baksql[0]
            print backsqls

            #执行回滚
            dbobj = self.dbmodel.objects.get(name=sqlobj.dbname)
            dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-execute;' % (dbobj.user, dbobj.password, dbobj.host, dbobj.port)
            exerz = table_structure(dbaddr, sqlobj.dbname, backsqls)
        sqlobj.save()
        return JsonResponse(res_data)

