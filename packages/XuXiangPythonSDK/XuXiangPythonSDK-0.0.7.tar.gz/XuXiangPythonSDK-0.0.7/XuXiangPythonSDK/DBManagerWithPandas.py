#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/3/2 5:28 下午
# @Author   : xuxiang
# @Project  : ReportUserFriendBindFileDetail
# @File     : DBManagerWithPandas.py
# @Software : PyCharm

import pandas as pd
from pandas import DataFrame
from XuXiangPythonSDK.Log import logger

from sqlalchemy import create_engine


class DBManagerWithPandas(object):
    # 初始化对象
    def __init__(self, host, user, password, dbname, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port

    def getData(self, sql, values=None, chunksize=None):
        conn = create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8'.format(user=self.user,
                                                                                           password=self.password,
                                                                                           host=self.host,
                                                                                           port=self.port,
                                                                                           dbname=self.dbname),
            pool_size=0,  # 连接池数量，无限制

        )
        df = DataFrame()
        try:
            df = pd.read_sql_query(sql=sql, params=values, con=conn, chunksize=chunksize)

        except Exception as e:
            logger.error('Pandas读取数据库失败', e)
            logger.info(sql, values)
        finally:
            conn.dispose()
            return df

    def insertData(self, df: DataFrame, tableName):
        conn = create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8'.format(user=self.user, password=self.password, host=self.host, port=self.port, dbname=self.dbname))
        code = False
        msg = '失败'

        try:
            df.to_sql(tableName, conn, if_exists='append', index=False)
            code = True
            msg = '成功'

        except Exception as e:
            logger.error('Pandas写入数据库失败', e)
            logger.info(tableName)
            code = False
            msg = e

        finally:
            conn.dispose()
            return code, msg
