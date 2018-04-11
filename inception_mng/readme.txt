#inception 安装 官方文档：http://mysql-inception.github.io/inception-document/usage/

yum -y install cmake libncurses5-dev libssl-dev  g++ gcc gcc-c++ openssl-devel ncurses-devel MySQL-python mysql git


#安装bison,只支持2.6以前的版本，Centos最新为3.0.4
curl -O http://ftp.gnu.org/gnu/bison/bison-2.5.1.tar.gz
tar zxvfp bison-2.5.1.tar.gz
cd bison-2.5.1
./configure
make -j4
make -j4 install

git clone https://github.com/mysql-inception/inception.git
cd inception/
sh inception_build.sh build linux

#如果执行报错，需删除编译目录，重新执行，否则还会报错
#osc操作大表支持需安装以下percona-tookit
curl -O https://www.percona.com/downloads/percona-toolkit/3.0.8/binary/redhat/7/x86_64/percona-toolkit-3.0.8-1.el7.x86_64.rpm
yum localinstall percona-toolkit-3.0.8-1.el7.x86_64.rpm

#Inception生成备份表及回滚语句需满足以下条件：
1. 线上服务器必须打开binlog日志,否则不会生成备份及回滚语句  log_bin=ON log_bin_index=mysql_bin.index
2. binlog_format必须为mixed或row,如果是statement模式，则不做备份及回滚语句的生成 binlog_format=mixed

vi /etc/inc.cnf

[inception]
general_log=1
general_log_file=inception.log
port=6669
socket=/自己目录，请自行修改/inc.socket
character-set-client-handshake=0
character-set-server=utf8
inception_remote_system_password=pip123456  //备份数据库的密码
inception_remote_system_user=django   //备份数据库的用户
inception_remote_backup_port=3306
inception_remote_backup_host=127.0.0.1
inception_support_charset=utf8
inception_enable_nullable=0
inception_check_primary_key=1
inception_check_column_comment=1
inception_check_table_comment=1
inception_osc_min_table_size=1
inception_osc_bin_dir=/data/temp
inception_osc_chunk_time=0.1
inception_enable_blob_type=1
inception_check_column_default_value=1

#启动inception
nohup /data/inception/builddir/mysql/bin/Inception --defaults-file=/etc/inc.cnf &

mysql -h127.0.0.1 -P6669 -uroot

mysql>inception get variables;

+------------------------------------------+-------------------------------------------+
| Variable_name                            | Value                                     |
+------------------------------------------+-------------------------------------------+
| inception_check_autoincrement_datatype   | ON                                        |
| inception_check_autoincrement_init_value | ON                                        |
| inception_check_autoincrement_name       | ON                                        |
| inception_check_column_comment           | ON                                        |
| inception_check_column_default_value     | ON                                        |
| inception_check_dml_limit                | ON                                        |
| inception_check_dml_orderby              | ON                                        |
| inception_check_dml_where                | ON                                        |
| inception_check_identifier               | ON                                        |
| inception_check_index_prefix             | ON                                        |
| inception_check_insert_field             | ON                                        |
| inception_check_primary_key              | ON                                        |
| inception_check_table_comment            | ON                                        |
| inception_check_timestamp_default        | ON                                        |
| inception_ddl_support                    | OFF                                       |
| inception_enable_autoincrement_unsigned  | ON                                        |
| inception_enable_blob_type               | ON                                        |
| inception_enable_column_charset          | OFF                                       |
| inception_enable_enum_set_bit            | OFF                                       |
| inception_enable_foreign_key             | OFF                                       |
| inception_enable_identifer_keyword       | OFF                                       |
| inception_enable_not_innodb              | OFF                                       |
| inception_enable_nullable                | OFF                                       |
| inception_enable_orderby_rand            | OFF                                       |
| inception_enable_partition_table         | OFF                                       |
| inception_enable_pk_columns_only_int     | OFF                                       |
| inception_enable_select_star             | OFF                                       |
| inception_enable_sql_statistic           | ON                                        |
| inception_max_char_length                | 16                                        |
| inception_max_key_parts                  | 5                                         |
| inception_max_keys                       | 16                                        |
| inception_max_primary_key_parts          | 5                                         |
| inception_max_update_rows                | 10000                                     |
| inception_merge_alter_table              | ON                                        |
| inception_osc_alter_foreign_keys_method  | none                                      |
| inception_osc_bin_dir                    | /usr/bin                                  |
| inception_osc_check_alter                | ON                                        |
| inception_osc_check_interval             | 5.000000                                  |
| inception_osc_check_replication_filters  | ON                                        |
| inception_osc_chunk_size                 | 1000                                      |
| inception_osc_chunk_size_limit           | 4.000000                                  |
| inception_osc_chunk_time                 | 0.100000                                  |
| inception_osc_critical_thread_connected  | 1000                                      |
| inception_osc_critical_thread_running    | 80                                        |
| inception_osc_drop_new_table             | ON                                        |
| inception_osc_drop_old_table             | ON                                        |
| inception_osc_max_lag                    | 3.000000                                  |
| inception_osc_max_thread_connected       | 1000                                      |
| inception_osc_max_thread_running         | 80                                        |
| inception_osc_min_table_size             | 1                                         |
| inception_osc_on                         | ON                                        |
| inception_osc_print_none                 | ON                                        |
| inception_osc_print_sql                  | ON                                        |
| inception_osc_recursion_method           | processlist                               |
| inception_password                       |                                           |
| inception_read_only                      | OFF                                       |
| inception_remote_backup_host             | 127.0.0.1                                 |
| inception_remote_backup_port             | 3306                                      |
| inception_remote_system_password         | *5FE69D16101ECFEAB571E80BF69E7C34861A8AF8 |
| inception_remote_system_user             | root                                      |
| inception_support_charset                | utf8                                      |
| inception_user                           |                                           |
+------------------------------------------+-------------------------------------------+

#使用示例
#!/usr/bin/python
#-*-coding: utf-8 -*-
import MySQLdb
#此处用户名密码为数据库的用户名和密码
#待审核/执行的sql语句（需包含目标数据库地址、端口等参数）
sql='/*--user=django;--password=pip123456;--host=127.0.0.1;--execute=1;--port=3306;*/\
inception_magic_start;\  #sql语句开始
use inc_test;\
insert into mytable1 (myname) values("xiayu1"),("xiayu2");\
insert into mytable1 (myname) values("xiayu3"),("xiayu4");\
inception_magic_commit;'  #sql语句结束
try:
    #此处用户名密码为inception的用户名和密码
    conn=MySQLdb.connect(host='127.0.0.1',user='',passwd='',db='',port=6669)
    cur=conn.cursor()
    ret=cur.execute(sql)
    result=cur.fetchall()
    num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]
    print field_names

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
