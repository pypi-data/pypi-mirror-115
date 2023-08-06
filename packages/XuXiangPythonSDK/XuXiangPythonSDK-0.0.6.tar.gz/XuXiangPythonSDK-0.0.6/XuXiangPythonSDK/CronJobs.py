#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/2/23 9:45 上午
# @Author   : xuxiang
# @Project  : XuXiangPythonLibrary
# @File     : CornJobs.py
# @Software : PyCharm

# 定时任务

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

class CronJob():
    # func 执行作业
    # trigger 触发方式 date,指定时间点，触发一次，interval,指定间隔时间，周期性执行，cron,在指定时间内，定期执行

    # 主线程运行，会阻塞主线程
    # func 执行作业
    # trigger 触发方式 date,指定时间点，触发一次，interval,指定间隔时间，周期性执行，cron,在指定时间内，定期执行

    # date触发方式的参数
    # run_date, 准确的执行时间，例如'2018-09-21 15:53:00' date(2009, 11, 6)  datetime(2009, 11, 6, 16, 30, 5)
    # run_date (datetime|str) – the date/time to run the job at
    # timezone (datetime.tzinfo|str) – time zone for run_date if it doesn’t have one already

    # interval触发方式的参数
    # interval, 间隔时间
    # weeks (int) – number of weeks to wait
    # days (int) – number of days to wait
    # hours (int) – number of hours to wait
    # minutes (int) – number of minutes to wait
    # seconds (int) – number of seconds to wait
    # start_date (datetime|str) – starting point for the interval calculation
    # end_date (datetime|str) – latest possible date/time to trigger on
    # timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations

    # cron触发方式的参数
    # year (int|str) – 4-digit year
    # month (int|str) – month (1-12)
    # day (int|str) – day of the (1-31)
    # week (int|str) – ISO week (1-53)
    # day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    # hour (int|str) – hour (0-23)
    # minute (int|str) – minute (0-59)
    # second (int|str) – second (0-59)
    # start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    # end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    # timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)

    # cron方式的表达式
    # Expression    Field   Description
    # *             any     每到*执行一次
    # */a           any     从最小值开始，每隔一个a值执行一次
    # a-b           any     在a-b范围内的任何值上执行（a必须小于b）
    # a-b/c         any     在a-b范围内每c值执行一次
    # xth y         day     本月内工作日y的第x次执行
    # last x        day     本月内最后一个工作日x执行
    # last          day     本月内最后一天执行
    # x,y,z         any     激发任何匹配的表达式；可以组合任意数量的上述表达式

    def blockingScheduler(self, func, trigger, id=None, name=None, *args, **kwargs):
        # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
        scheduler = BlockingScheduler()
        # 采用阻塞的方式

        scheduler.add_job(func, trigger=trigger, id=id, name=name, misfire_grace_time=600, *args, **kwargs)

        scheduler.start()

    # 后台执行
    def backgroundScheduler(self, func, trigger, id=None, name=None, *args, **kwargs):
        # BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。
        scheduler = BackgroundScheduler()
        # 采用非阻塞的方式

        scheduler.add_job(func, trigger=trigger, id=id, name=name, misfire_grace_time=600, *args, **kwargs)
        # 这是一个独立的线程
        scheduler.start()



