import time
import pandas as pd
from impala.dbapi import connect


def test_connect():  ################ 金晨潇模板
    res = []
    cur.execute('use kudu_pro;')
    sql = "select at_filepath  from attachment where at_subtype = '207003' and at_identifier is not null limit 100"
    cur.execute(sql)
    data_list = cur.fetchall()
    for data in data_list:
        res.append(str(data).replace("('", '').replace("',)", '').replace('/upload/', '/data/oms_upload/'))
    print(res[:3])
    return res     


def get_kudu_db_info(host='101.132.107.216', port=21050):
    conn = connect(host=host, port=port)
    cur = conn.cursor()   
    cur.execute('show databases;')
    res = cur.fetchall()
    db_list = [i[0] for i in res]
    print('kudu中的库........', db_list)
    return db_list

class MyImpalaConnect():
    def __init__(self, host='101.132.107.216', port=21050, db='kudu_pro'):
        self.conn = connect(host='101.132.107.216', port=21050)
        self.cur = self.conn.cursor()
        self.cur.execute('use %s;'%db)

    def get_tb_list(self):  # 得到一个库的所有表
        self.cur.execute('show tables;')
        res = self.cur.fetchall()
        tb_list = [i[0] for i in res]
        # print(tb_list)
        return tb_list

    def get_tb_describe(self, tb):
        # self.cur.execute('use %s;'%tb)
        self.cur.execute('DESCRIBE %s;'%tb)                            
        res = self.cur.fetchall()
        df = pd.DataFrame(res, columns='col_en,col_type,col_cn,x,x,x,x,x,x'.split(','))
        # print(df)
        # df.to_excel('col_type.xlsx', index=False)
        # print(dict(zip(df['col_en'].tolist(), df['col_cn'].tolist())))
        return df

    def get_tb_df(self, tb, q_str=None):  # 得到某个库，一个表的dataframe
        df1 = self.get_tb_describe(tb)
        if q_str is None:
            q_str = ''
        sql = '''
        select * from %s %s
        '''%(tb,q_str)    ############# 增加查询条件
        '''
        #### 计算时间戳
        import time
        x = '2022-01-01'
        t_stamp = time.mktime(time.strptime(x,'%Y-%m-%d'))
        '''
        self.cur.execute(sql)
        res = self.cur.fetchall()
        df = pd.DataFrame(res, columns=df1['col_en'])
        # print(df[:3])
        return df

    def get_tb_df_limit10(self, tb):  # 得到某个库，一个表的dataframe
        df1 = self.get_tb_describe(tb)
        sql = '''
        select * from %s limit 10
        '''%tb
        self.cur.execute(sql)

        res = [df1['col_cn'].tolist()]+list(list(x) for x in self.cur.fetchall())
        df = pd.DataFrame(res, columns=df1['col_en'])
        # print(df[:3])
        return df


    def run(self):
        # self.test_connect()
        # self.get_tb_list()
        self.get_tb_describe(tb='user')
        # self.get_tb_df('car')
        # df = self.get_tb_df_limit10('car')
        # print(df)
        # df = self.get_tb_df(tb='user')
        # df.to_pickle('test.pickle')
        pass



if __name__=='__main__':
    MyImpalaConnect().run()