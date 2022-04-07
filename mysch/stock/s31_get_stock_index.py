
import sys
sys.path.append('../..')


import os
import time
import random
import config
import datetime
import numpy as np
import pandas as pd
import baostock as bs
import seaborn as sns

import mysch.stock.index_cal as mic

from multiprocessing import Pool
from sklearn import preprocessing
import matplotlib.pyplot as plt


def boll_bands(data, ndays):
    """
    计算布林带
    :param data: 股票的df格式数据
    :param ndays: 计算使用的简单移动均线周期
    :return:
    """
    ma = pd.Series(np.round(data['close'].rolling(ndays).mean(), 2), name='MA%s'%ndays)  # 计算nday均线
    # pandas.std() 默认是除以n-1 的，即是无偏的，如果想和numpy.std() 一样有偏，需要加上参数ddof=0
    # 此处添加ddof的原因是wind和yahoo的计算均采用的有偏值进行的计算
    std = pd.Series(np.round(data['close'].rolling(ndays).std(ddof=0), 2))  # 计算nday标准差，有偏
    b1 = ma + (2 * std)  # 此处的2就是Standard Deviations
    B1 = pd.Series(b1, name='UpperBollingerBand')
    data = data.join(ma)  # 上边不写name 这里报错
    data = data.join(B1)

    b2 = ma - (2 * std)
    B2 = pd.Series(b2, name='LowerBollingerBand')
    data = data.join(B2)

    data = data.fillna(method='bfill')
    return data


class RefreshLocalData():
    def __init__(self):     # N_Period K线的周期
        self.t1_start = time.time()
        self.stock_list_date = '2022-03-16'
        self.today = time.strftime('%Y-%m-%d',time.localtime(time.time()))  # 今天的日期
        self.df_cols_float_str = "open,high,low,close,turn,volume,amount,pctChg"  # 选择查询的列
        self.query_str =  "date,code,"+self.df_cols_float_str   # 加上日期

        if __name__=='__main__':
            if os.path.exists('test_output') is False:os.mkdir('test_output')

    def get_stock_list(self):
        bs.login()          # 登陆系统
        rs = bs.query_all_stock(self.stock_list_date)   # self.today
        data_list = []
        while (rs.error_code == '0') & rs.next():data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)
        df['tradeStatus'] = df['tradeStatus'].astype(int)
        df = df[(df['code']>='sh.600000')&(df['code']<'sz.310000')&(df['tradeStatus']==1)]  # 排除各类指数

        f_path = os.path.join(config.f_path['excel'], 'stock_list.pickle')
        # if os.path.exists(f_path) is False:
        df.to_pickle(f_path)

        if __name__=='__main__':
            df.to_excel('test_output/stock_list.xlsx', index=False)

    
    def get_one_stock(self, stock_id='sh.600008', frequency="d"):
        bs.login()          # 登陆系统
        now = datetime.datetime.now()
        if frequency=="d":delta = datetime.timedelta(days=80)
        if frequency=="w":delta = datetime.timedelta(days=80*7)  # 周线和月线日期要移动更多
        if frequency=="m":delta = datetime.timedelta(days=80*30)
        n_days = now - delta
        start_date =  n_days.strftime('%Y-%m-%d')
        
        rs = bs.query_history_k_data(stock_id, self.query_str,  start_date, end_date=self.today, frequency=frequency, adjustflag="2") # adjustflag=2前复权
        data_list = []
        while (rs.error_code == '0') & rs.next():
            row_i = rs.get_row_data()
            add_bool = True
            for j in row_i:
                if len(j)<=4:
                    add_bool = False
                    break
            if add_bool:
                data_list.append(row_i)
        df = pd.DataFrame(data_list, columns=rs.fields)
        df = df.fillna(method='bfill').fillna(method='ffill').fillna(0)

        # df.to_excel('test_%s.xlsx'%frequency, index=False)
        for ci in self.df_cols_float_str.split(','):
            df[ci] = df[ci].astype(float)
        
        df['total_v'] = df['volume']*df['close']*100/(df['turn']+0.0000000001)/100000000 # 亿元

        df = boll_bands(df, 10)
        df['up_boll'] =  df['close']/df['UpperBollingerBand']
        df['mean_boll'] =  df['close']/df['MA10']
        df['low_boll'] =  df['close']/df['LowerBollingerBand']
        df = df['close,turn,total_v,up_boll,mean_boll,low_boll'.split(',')]

        if stock_id=='sh.600000':
            f_path = os.path.join(config.f_path['excel'], 'sh.600000.xlsx')
            df.to_excel(f_path, index=False)
        return df

    def calculate_one_stock(self, stock_id='sh.600000'):
        df_d = self.get_one_stock(stock_id, frequency="d")
        df_w = self.get_one_stock(stock_id, frequency="w")
        df_m = self.get_one_stock(stock_id, frequency="m")
        COI = mic.CalculateOneIndex(df_d, df_w, df_m)
        col_list,v_list = COI.create_all_index()
        return col_list,v_list       

    def calculate_all_stock_multi_process(self):
        n = os.cpu_count()
        pool = Pool(processes=n-2)  # 默认cpu_count()

        f_path = os.path.join(config.f_path['excel'], 'stock_list.pickle')
        stock_list_df = pd.read_pickle(f_path).reset_index(drop=True)
        # print(stock_list_df.columns)
        N = 100  # stock_list_df.shape[0]
        N = stock_list_df.shape[0]
        wrong_list = []
        rows=[]
        res_list = []
        for i in range(N):
            time.sleep(0.3*random.random())
            # print(stock_list_df['code'][i])
            # print('...................................................', i,'/',N)
            res = pool.apply_async(self.calculate_one_stock,args=(stock_list_df['code'][i],))#.get()
            res_list.append(res)
        pool.close()
        pool.join()

        for i,res in enumerate(res_list):
            try:
                rows.append([stock_list_df['code'][i]]+res.get()[1])
            except:
                wrong_list.append(stock_list_df['code'][i])


        print('这些code报错了==>', wrong_list)
        df = pd.DataFrame(rows, columns=['code']+res.get()[0])
        df1 = stock_list_df['code,code_name'.split(',')]
        df = pd.merge(df1,df,on='code', how='inner')
        return df

        # print(df)
        # writer=pd.ExcelWriter('output/myindex_%s.xlsx'%self.today) # %self.today
        # df.to_excel(writer,sheet_name='myindex',index=False)
        # writer.save()

    def color_excel(self):
        df = self.calculate_all_stock_multi_process()

        sort_col = '月市值分位'
        df = df.fillna(0).sort_values(sort_col)  # 读取数据
        cols_list = df.columns.tolist()
        temp_l = cols_list[2:]
        temp_l.remove(sort_col)
        cols_list = cols_list[:2]+[sort_col]+temp_l
        print(cols_list)
        df = df[cols_list]

        def quantile_5_95_df_col(df, col):      # 将某一列的极大极小值设置为边界值
            quantile_5 = df[col].quantile(0.025)
            quantile_95 = df[col].quantile(0.975)
            # Series.clip(lower=None, upper=None, axis=None, inplace=False)
            clip_res = df[col].clip(quantile_5, quantile_95)
            return clip_res

        for col in cols_list[2:]:
            df[col] = quantile_5_95_df_col(df, col)

        ## YlGnBu  gist_earth_r  GnBu  
        color_map = plt.get_cmap('GnBu')  # 颜色选择参考
        df = df.style.background_gradient(
            color_map, subset=['总市值']).background_gradient(
            color_map, subset=['换手率']).background_gradient(
            color_map, subset=['月换手分位']).background_gradient(
            color_map, subset=['月市值分位']).background_gradient(
            color_map, subset=['2日涨幅']).background_gradient(
            color_map, subset=['5日涨幅']).background_gradient(
            color_map, subset=['5周涨幅']).background_gradient(
            color_map, subset=['B2d']).background_gradient(
            color_map, subset=['B5d']).background_gradient(
            color_map, subset=['B10d']).background_gradient(
            color_map, subset=['B15w']).background_gradient(
            color_map, subset=['tp1d']).background_gradient(
            color_map, subset=['tp3d']).background_gradient(
            color_map, subset=['tp1w']).background_gradient(
            color_map, subset=['tp3w'])

        f_path = os.path.join(config.f_path['excel'], 'myindex_%s.xlsx'%self.today)
        df.to_excel(f_path, index=False)
        return df


    def run(self):
        # self.get_stock_list()
        # self.get_stock_list()
        # self.get_one_stock(frequency="d")
        # self.get_one_stock(frequency="w")
        # self.get_one_stock(frequency="m")
        # self.calculate_one_stock()
        # self.calculate_all_stock()
        # self.calculate_all_stock_multi_process()
        self.color_excel()
        # run_cost_t = round(time.time()-self.t1_start)
        # print('运行耗时============================================>', run_cost_t)

        pass

if __name__=='__main__':
    RefreshLocalData().run()