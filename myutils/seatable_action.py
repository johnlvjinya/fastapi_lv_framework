
import os
import pandas as pd
from seatable_api import Base, context

if __name__=='__main__':
    import dict_json_saver as mdjs  ### 当前文件测试
else:
    import myutils.dict_json_saver as mdjs
    import config

class MyseaTable():
    def __init__(self,st_api_token, server_url='https://cloud.seatable.cn'):
        self.base = Base(st_api_token, server_url='https://cloud.seatable.cn')
        self.base.auth()        

    def get_sub_tb_list(self):
        res = self.base.get_metadata()
        # print(res)
        tb_list = [x.get('name') for x in res['tables']]

        st_tb_dict = {}
        for x in res['tables']:
            st_tb_dict[x['name']] = x['_id']

        if __name__!='__main__':
            f_path = os.path.join(config.f_path['data_json'], 'st_tb_dict.json')
            mdjs.save_dict_to_json(st_tb_dict, file_path=f_path)
        else:
            print(st_tb_dict)
        return tb_list

    def get_tb_df(self, tb):
        rows = self.base.list_rows(tb, view_name=None, order_by=None, desc=False, start=None, limit=None)
        df = pd.DataFrame(rows)
        return df



if __name__=='__main__':
    st_api_token = '0bfd623fc845592c776d8c35e2f24ae69cf3eb53'
    mt = MyseaTable(st_api_token)
    tb_list = mt.get_sub_tb_list()

    df = mt.get_tb_df('AI')
    df.to_excel('test.xlsx', index=False)
