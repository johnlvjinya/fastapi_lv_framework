import time
import pandas as pd
from impala.dbapi import connect


class MyImpalaConnect():
    def __init__(self, host='101.132.107.216', port=21050, db='kudu_pro'):
        self.conn = connect(host='101.132.107.216', port=21050)
        self.cur = self.conn.cursor()
        self.cur.execute('use %s;'%db)

    def get_tb_describe(self, tb):
        # self.cur.execute('use %s;'%tb)
        self.cur.execute('DESCRIBE %s;'%tb)                            
        res = self.cur.fetchall()
        df = pd.DataFrame(res, columns='col_en,col_type,col_cn,x,x,x,x,x,x'.split(','))
        # print(df)
        # df.to_excel('col_type.xlsx', index=False)
        # print(dict(zip(df['col_en'].tolist(), df['col_cn'].tolist())))
        return df

    def get_tb_df_limit10(self, tb):  # 得到某个库，一个表的dataframe
        df1 = self.get_tb_describe(tb)

        sql = '''
        select * from %s limit 10
        '''%tb
        self.cur.execute(sql)

        res = [df1['col_cn'].tolist()]+list(list(x) for x in self.cur.fetchall())
        df = pd.DataFrame(res, columns=df1['col_en'])
        print(df)
        # print(df[:3])
        return df

    def sql_tb_col_col_v(self, tb, col, col_v):  # 得到某个库，一个表的dataframe

        df1 = self.get_tb_describe(tb)

        sql = '''
        select * from %s where %s='%s'
        '''%(tb, col, col_v)
        self.cur.execute(sql)

        res = [df1['col_cn'].tolist()]+list(self.cur.fetchall())
        df = pd.DataFrame(res, columns=df1['col_en'])
        df.to_excel('test.xlsx', index=False)
        


    def run(self):
        # self.get_tb_df_limit10(tb='order_goods')
        # 62640806 transport_order
        # self.sql_tb_col_col_v(tb='order_goods', col='to_id', col_v=1581117)
        
        ## to_no
        self.sql_tb_col_col_v(tb='transport_order', col='to_no', col_v='62640806')

        pass



if __name__=='__main__':
    MyImpalaConnect().run()