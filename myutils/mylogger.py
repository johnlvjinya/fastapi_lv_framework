import os
import logging
import pandas as pd
import logging.handlers
from datetime import datetime

def create_lg_path(lg_path):
    fsplit = os.path.split(lg_path)
    f_path = fsplit[0]
    if os.path.exists(f_path) is False:
        os.makedirs(f_path)

def my_date_loger(lg_path='test/class_logging_test.log', filemode='a', level='debug', ADD_DATE=True):

    if ADD_DATE:  # 自动增加日期
        now = datetime.now()                # current date and time
        today1 = datetime.now().strftime("%Y-%m-%d")

        fsplit = os.path.split(lg_path)  # 原来的路径
        new_p = os.path.join(fsplit[0], today1)
        lg_path = os.path.join(new_p, fsplit[1])
   
    create_lg_path(lg_path)  # 创建文件目录
    level_dict = {
        'critical':logging.CRITICAL,
        'error':logging.ERROR,
        'warning':logging.WARNING,
        'info':logging.INFO,
        'debug':logging.DEBUG,
    }
    level_x = level_dict.get(level)
    if not level_x:
        level_x = logging.INFO # 默认为info
    logging.basicConfig(
                        level=level_x, # 打印到控制台的级别为INFO， CRITICAL > ERROR > WARNING > INFO > DEBUG
                        format='%(asctime)s=@@=%(name)-5s=@@=%(levelname)-5s=@@=%(message)-5s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename=lg_path,
                        filemode=filemode,
                        )
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # console = logging.StreamHandler()
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)     # 打印到控制台
    file_handler = logging.handlers.RotatingFileHandler(lg_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    return logging

def analysis_df_log(lg_path):
    f = open(lg_path)
    line = f.readline()
    rows = []
    while line:
        # print(line.strip('\n'))
        l = line.strip('\n')
        row_i = l.split('=@@=')
        rows.append(row_i)
        line = f.readline()
    df = pd.DataFrame(rows, columns='时间,logger名称,级别,message'.split(','))
    # df.to_excel()
    return df


###############测试
if __name__=='__main__':
    lg = my_date_loger()
    lg.info('test')

    lg1 = lg.getLogger('myloggr1')
    lg1.debug('test lg1')

    lg1.debug('Quick zephyrs blow, vexing daft Jim.')
    lg1.info('How quickly daft jumping zebras vex.')
    lg1.warning('Jail zesty vixen who grabbed pay from quack.')
    lg1.error('The five boxing wizards jump quickly.')

    ##### 分析log
    df = analysis_df_log('test/class_logging_test.log')
    print(df)



