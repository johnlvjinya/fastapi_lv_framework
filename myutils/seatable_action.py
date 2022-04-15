
import pandas as pd
from seatable_api import Base, context

class MyseaTable():
    def __init__(self,st_api_token, server_url='https://cloud.seatable.cn'):
        self.base = Base(st_api_token, server_url='https://cloud.seatable.cn')
        self.base.auth()        

    def get_sub_tb_list(self):
        res = self.base.get_metadata()
        tb_list = [x.get('name') for x in res['tables']]
        return tb_list

    def get_tb_df(self, tb):
        rows = self.base.list_rows(tb, view_name=None, order_by=None, desc=False, start=None, limit=None)
        df = pd.DataFrame(rows)
        return df



if __name__=='__main__':
    st_api_token = '0bfd623fc845592c776d8c35e2f24ae69cf3eb53'
    mt = MyseaTable(st_api_token)
    tb_list = mt.get_sub_tb_list()

    df = mt.get_tb_df('guitar')
    df.to_excel('test.xlsx', index=False)


    


# # rows = base.list_rows('箱子不一致分析')
# # print(len(rows), '测试seatable.........................')
# sql = '''  select _id from 箱子不一致分析 where 运单号='%s' '''%str(data.get('dialog_id'))
# res = base.query(sql)

# # print(res)
# if len(res)>0:
#     s_id = res[0].get('_id')
#     row_data = {}
#     s1 = nv_dict.get('commentField').replace(' ','')
#     s2 = nv_dict.get('ageRangeField').replace(' ', '')
#     if s1!='':
#         row_data['不一致原因'] = nv_dict.get('commentField')
#     if s2!='':
#         row_data['算法是否需要修正'] = nv_dict.get('ageRangeField')
#     print('row_data...........', row_data)
#     base.update_row('箱子不一致分析', s_id, row_data)    

# return {'dialog_id':data.get('dialog_id'), 's1':s1}


