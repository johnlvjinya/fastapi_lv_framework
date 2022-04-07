
import sys
sys.path.append('../..')
import os
import time
import config
import datetime
import numpy as np
import pandas as pd
import baostock as bs


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

        pickle_path = 'test_output/stock_list.pickle'
        if __name__=='__main__':
            if os.path.exists(pickle_path) is False:

                bs.login()          # 登陆系统
                rs = bs.query_all_stock(self.stock_list_date)   # self.today
                data_list = []
                while (rs.error_code == '0') & rs.next():data_list.append(rs.get_row_data())
                df = pd.DataFrame(data_list, columns=rs.fields)
                df['tradeStatus'] = df['tradeStatus'].astype(int)
                df = df[(df['code']>='sh.600000')&(df['code']<'sz.310000')&(df['tradeStatus']==1)]  # 排除各类指数

                df.to_excel('test_output/stock_list.xlsx', index=False)
                df.to_pickle(pickle_path)

        self.df = pd.read_pickle(pickle_path)
        print(self.df.shape)


    def get_classify(self):
        df = self.df
        c_dict = {
            '银行':'银行',
            '机场航空':'机场,航空,航',
            '汽车':'汽车,客车',
            '贸易':'贸',
            '环保':'环保,生态',
            '道路':'高速,路,桥',
            '港口':'港',
            '船舶':'船',
            '能源':'能,石油,石化',
            '旅游':'旅,游',
            '投资':'投资,财',
            '医药':'医,药,疗,健康,安堂',
            '矿产':'矿,稀土',
            '光学':'光学,光电',
            '材料':'材料,新材',
            '传媒':'传媒,文化',
            '电钢煤':'电力,煤,钢铁',
            '证券':'证券',
            '电子':'电子',
            '电气':'电气,电器,精密,仪',
            '电缆':'缆,线缆',
            '食品':'食品,粮,棕榈,农牧,榨菜,火腿,啤酒',
            '重工':'重工,机械',
            '化工':'化工,生化,化学',
            '新能源':'锂业,锂,核',
            '快递':'快递',
        }
        cl_list = []
        for i,r in df.iterrows():
            ci = '未分类'
            for k,v in c_dict.items():
                for v_j in v.split(','):
                    if v_j in r['code_name']:
                        ci = k
                        break
            cl_list.append(ci)
        df['类别'] = cl_list
        df = df.sort_values('类别').reset_index(drop=True)

        if __name__=='__main__':
            df.to_excel('test_output/stock_list_classify.xlsx', index=False)

    

    def run(self):
        self.get_classify()
        pass

if __name__=='__main__':
    RefreshLocalData().run()