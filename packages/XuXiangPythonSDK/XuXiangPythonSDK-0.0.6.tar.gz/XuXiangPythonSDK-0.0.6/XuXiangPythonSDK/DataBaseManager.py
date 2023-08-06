#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/1/25 3:32 下午
# @Author   : xuxiang
# @Project  : XuXiangPythonLibrary
# @File     : DataBaseManager.py
# @Software : PyCharm

import pymysql
from dbutils.pooled_db import PooledDB
from XuXiangPythonSDK.Log import logger


class DataBaseManager:
    # 初始化对象
    def __init__(self, host, user, password, dbname, port=3306, charset='utf8', use_unicode=True):
        self.pool = self.mysql_connection(host=host, user=user, password=password, dbname=dbname, port=port,
                                          charset=charset, use_unicode=use_unicode)

    # 连接数据库
    def mysql_connection(self, host, user, password, dbname, port=3306, charset='utf8', use_unicode=True):
        pool = PooledDB(
            creator=pymysql,
            maxconnections=0,   # 最大连接数 0和None表示不限制
            mincached=4,        # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=0,        # 链接池中最多闲置的链接，0和None不限制
            blocking=False,     # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            host=host,
            port=port,
            user=user,
            passwd=password,
            db=dbname,
            charset=charset,
            use_unicode=use_unicode,
        )
        return pool

    # 新建表 sql="create table tableName(id bigint (255) primary key auto_increment not null ,name varchar (255)not null,age int (255) not null)"
    def create_table(self, sql):
        con = self.pool.connection()
        cur = con.cursor()
        state = False
        try:
            cur.execute(sql)
            state = True
        except Exception as e:
            logger.error(f"数据库新建表操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 清空表数据
    def clear_table(self, tablename):
        con = self.pool.connection()
        cur = con.cursor()
        sql = f"truncate table {tablename}"
        state = False
        try:
            cur.execute(sql)
            state = True
        except Exception as e:
            logger.error(f"数据库清空表操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 删除表数据和表结构
    def delete_table(self, table_name):
        con = self.pool.connection()
        cur = con.cursor()
        sql = f"drop table {table_name}"
        state = False
        try:
            cur.execute(sql)
            state = True
        except Exception as e:
            logger.error(f"数据库删除表操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 复制表结构到新表
    def copy_table(self, new_table_name, old_table_name):
        con = self.pool.connection()
        cur = con.cursor()
        sql = "create table {} like {}".format(new_table_name, old_table_name)
        state = False
        try:
            cur.execute(sql)
            state = True
        except Exception as e:
            logger.error(f"数据库复制表结构操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 复制表结构和数据到新表
    def copy_table_and_data(self, new_table_name, old_table_name):
        con = self.pool.connection()
        cur = con.cursor()
        sql = "create table {} select * from {}".format(new_table_name, old_table_name)
        state = False
        try:
            cur.execute(sql)
            state = True
        except Exception as e:
            logger.error(f"数据库复制表结构和数据操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 复制表数据到新表（新表已有字段，并和旧表结构一样）
    def copy_table_data(self, new_table_name, old_table_name):
        con = self.pool.connection()
        cur = con.cursor()
        sql = "insert into {} select * from {}}".format(new_table_name, old_table_name)
        state = False
        try:
            cur.execute(sql)
            state = True
        except Exception as e:
            logger.error(f"数据库复制表数据操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 增加 sql = "insert into tableName (name, age) values (%s, %s)"  values = ('张三', 18)
    def insert_data(self, sql, values=None):
        con = self.pool.connection()
        cur = con.cursor()
        state = False
        try:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            con.commit()
            state = True
        except Exception as e:
            con.rollback()  # 回滚
            logger.error(f"数据库插入数据操作有误，原因：{e}")
            logger.info(values)
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 批量插入数据  "insert into tableName (name, age) values (%s, %s)"  values = [('张三', 18), ('李四', 19), ('王五', 20)]
    def insert_many_data(self, sql, values):
        con = self.pool.connection()
        cur = con.cursor()
        state = False
        try:
            cur.executemany(sql, values)
            con.commit()
            state = True
        except Exception as e:
            con.rollback()  # 回滚
            logger.error(f"数据库批量插入数据操作有误，原因：{e}")
            logger.info(values)
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 删除 values=18 sql="delete from tableName where age > %s"
    def delete_data(self, sql, values=None):
        con = self.pool.connection()
        cur = con.cursor()
        state = False
        try:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            con.commit()
            state = True
        except Exception as e:
            con.rollback()  # 回滚
            logger.error(f"数据库删除数据操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 批量删除 values = (18, 19, 20)
    #         sql = "delete from tableName where age = %s"
    def delete_many_data(self, sql, values):
        con = self.pool.connection()
        cur = con.cursor()
        state = False
        try:
            cur.executemany(sql, values)
            con.commit()
            state = True
        except Exception as e:
            con.rollback()  # 回滚
            logger.error(f"数据库批量删除数据操作有误，原因：{e}")
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 更新 values=('李四', 18)  sql="update tableName set name = %s where age = %s"
    def update_data(self, sql, values=None):
        con = self.pool.connection()
        cur = con.cursor()
        state = False
        try:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            con.commit()
            state = True
        except Exception as e:
            con.rollback()  # 回滚
            logger.error(f"数据库更新数据操作有误，原因：{e}")
            logger.info(values)
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 批量更新 values=[('李四', 18), ('王五',19), ('张三', 20)]  sql="update tableName set name = %s where age = %s"
    def update_many_data(self, sql, values):
        con = self.pool.connection()
        cur = con.cursor()
        state = False
        try:
            cur.executemany(sql, values)
            con.commit()
            state = True
        except Exception as e:
            con.rollback()  # 回滚
            logger.error(f"数据库批量更新数据操作有误，原因：{e}")
            logger.info(values)
            state = False
        finally:
            cur.close()
            con.close()
            return state

    # 查询全部数据 age=18 sql="select * from tableName where age=%s"
    def select_all_data(self, sql, values=None):
        con = self.pool.connection()
        cur = con.cursor()
        result = []
        try:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            result = cur.fetchall()

        except Exception as e:
            logger.error(f"数据库查询全部数据操作有误，原因：{e}")
        finally:
            cur.close()
            con.close()
            return result

    # 查询一条数据 age=18 sql="select * from tableName where age=%s"
    def select_one_data(self, sql, values=None):
        con = self.pool.connection()
        cur = con.cursor()
        result = ()
        try:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            result = cur.fetchone()
        except Exception as e:
            logger.error(f"数据库查询一条数据操作有误，原因：{e}")
        finally:
            cur.close()
            con.close()
            return result

    # 查询指定条数数据 age=18 sql="select * from tableName where age=%s"
    def select_many_data(self, sql, values=None, rows=None):
        con = self.pool.connection()
        cur = con.cursor()
        result = []
        try:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            result = cur.fetchmany(size=rows)

        except Exception as e:
            logger.error(f"数据库查询多条数据操作有误，原因：{e}")
        finally:
            cur.close()
            con.close()
            return result
