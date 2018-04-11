#!/usr/bin/python
#-*-coding: utf-8 -*-
import MySQLdb
#此处用户名密码为数据库的用户名和密码

def table_structure(dbinfo,dbname,sqlcontent):
    # sql1='/*--user=django;--password=pip123456;--host=127.0.0.1;--execute=1;--port=3306;*/\
    sql = '/* %s; */\
    inception_magic_start;\
    use %s;%s inception_magic_commit' %(dbinfo, dbname, sqlcontent)

    try:
        #此处用户名密码为inception的用户名和密码
        conn=MySQLdb.connect(host='127.0.0.1',user='',passwd='',db='',port=6669)
        cur=conn.cursor()
        ret=cur.execute(sql)
        result=cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]

        print result
        '''
        for row in result:
            print row[0], "|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",
            row[5],"|",row[6],"|",row[7],"|",row[8],"|",row[9],"|",row[10]
        '''
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return result


def getbak(sql, rollbackdb):
    pass