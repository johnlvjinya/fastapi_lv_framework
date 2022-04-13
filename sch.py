import os
import config
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import data_analysis.data_offline.s02_get_data_from_kudu as s2gdfk

import algorithms.algori_route.s21_route_clean_local_pickle as route21
import algorithms.algori_route.s22_route_region_df_route as route22
import algorithms.algori_route.s30_get_node_connection as route30

print('启动定时程序')
################ 测试
def job():
    print('job 3s')

def my_job():
    print('my_job')

def start_sch():
    ################# 任务初始化
    sched = BlockingScheduler(timezone='Asia/Shanghai')
    ################# 添加任务
    sched.add_job(job, 'interval', id='3_second_job', seconds=3)
    sched.add_job(my_job, 'cron', month='1-12', day_of_week='mon-sun', hour=16, minute=11)
    # sched.add_job(log_test, 'interval', id='log_testdd', hours=1)
    # sched.add_job(get_data_from_kudu, 'cron', month='1-12', day_of_week='mon-sun', hour='0-23', minute=1)
    # sched.add_job(get_data_from_kudu_all, 'cron', month='1-12', day_of_week='mon-sun', hour='8', minute=42)
    # sched.add_job(run_bin_daily, 'cron', month='1-12', day_of_week='mon-sun', hour='0', minute=11)
    # sched.add_job(refresh_route_data, 'cron', month='1-12', day_of_week='mon-sun', hour='1', minute=39)

    sched.start()


if __name__=='__main__':
    start_sch()

 