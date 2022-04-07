
import pandas as pd

class CalculateOneIndex():
    def __init__(self, df_d, df_w, df_m):
        self.df_d = df_d    # 日线
        self.df_w = df_w    # 周线
        self.df_m = df_m    # 月线

    def boll_index(self, df, n_select=5):
        '''
        收盘价与三个轨道比值平均
        下轨道击穿
        '''
        if df.shape[0] >= n_select:
            N = df.shape[0]-n_select
        else:
            N = 0
        # up_b = df['up_boll'][N:].mean()
        # gap_b = (df['low_boll'][N:]-df['up_boll'][N:]).mean()       # boll带的宽度
        # mean_b = df['mean_boll'][N:].mean()
        low_b = df['low_boll'][N:].mean()-1             # boll下均线的漂移，漂移越多说明越低
        # low_b_min = df['low_boll'][N:].min()-1          # boll下均线，最小值的漂移
        res_list = [low_b]
        # print(res_list)
        return [round(i*100,3) for i in res_list]

    def current_v_percentile(self, df, col='total_v', n_select=5):
        '''
        返回当前数值的分位数
        '''
        N = df.shape[0]
        current_v = df[col][N-1]
        v_list = df[col].tolist()
        v_list.sort()
        percentile = v_list.index(current_v)/len(v_list)
        # print(percentile)
        return [round(percentile,3)]

    def total_v_turnover_and_other(self, df):
        N = df.shape[0]
        total_v = round(df['total_v'][N-1])
        turnover =  df['turn'][N-1]
        return [total_v, turnover]

    def turnover_pulse(self, df):  # 换手率突变指标
        N = df.shape[0]
        if N>5:
            res1 = df['turn'][N-1]/(df['turn'][N-2]+0.00000001)
            res3 = df['turn'][N-1]/(df['turn'][N-4:N-1].mean()+0.00000001)
        else:
            res1 = 1
            res3 = 1
        return [round(res1, 4), round(res3, 4)]

    def price_grow(self, df, n_period=5):
        N = df.shape[0]
        if N>n_period+3:
            res1 = (df['close'][N-1]-df['close'][N-1-n_period])/df['close'][N-1-n_period]
        else:
            res1 = 0     
        return [round(100*res1)]

    def create_all_index(self):
        col_v_dict = {              # 注意这个字典的值都是List, key用都好分割字符
        '总市值,换手率':self.total_v_turnover_and_other(self.df_d),
        '月换手分位':self.current_v_percentile(self.df_m, col='turn'),
        '月市值分位':self.current_v_percentile(self.df_m, col='total_v'),
        '2日涨幅':self.price_grow(self.df_d, n_period=2),
        '5日涨幅':self.price_grow(self.df_d, n_period=5),
        '5周涨幅':self.price_grow(self.df_w, n_period=5),
        'tp1d,tp3d':self.turnover_pulse(self.df_d),
        'tp1w,tp3w':self.turnover_pulse(self.df_w),
        'B2d':self.boll_index(self.df_d, n_select=2),  # 当前价格和4日下限均值对比
        'B5d':self.boll_index(self.df_d, n_select=5),  # 当前价格和4日下限均值对比
        'B10d':self.boll_index(self.df_d, n_select=10),
        'B15w':self.boll_index(self.df_w, n_select=15),

        }

        col_list,v_list = [],[]
        for k,v in col_v_dict.items():
            col_list += k.split(',')
            v_list += v
        res = [col_list,v_list]
        return res

    def run(self):
        # res_b = self.boll_index(self.df_w)
        # self.current_v_percentile(self.df_w)
        res = self.create_all_index()

        return res


if __name__=='__main__':
    df_d = pd.read_excel('../output/sh.600000_d.xlsx')
    df_w = pd.read_excel('../output/sh.600000_w.xlsx')
    df_m = pd.read_excel('../output/sh.600000_m.xlsx')

    print(df_d.head(2))
    res=CalculateOneIndex(df_d, df_w, df_m).run()
    print(res)
