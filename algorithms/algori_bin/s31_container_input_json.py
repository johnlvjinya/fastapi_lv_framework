
import sys
sys.path.append('../..')
import os
import json
import config
import pandas as pd
# from copy import deepcopy
import myutils.dict_json_saver as mdjs
from myutils.func_decorated import log_func_time
################################ 记录log
class CleanContainerExcel():
    def __init__(self):

        fp = os.path.join(config.ROOT_PATH, 'data/bin/箱子算法数据维护.xlsx')
        df = pd.read_excel(fp, sheet_name='箱子信息') 
        df['类型'] = df['类型'].fillna('-99999')
        df['名称'] = df['名称'].fillna('-99999')
        df = df[(df['类型']!='-99999')&df['是否使用']==1].reset_index(drop=True)
        df['箱子名称'] = df['名称']## df['型号']+'__'+df['名称']   ######## 注意如果名字完善后可以直接用名字，现在有重复的情况


        self.df1 = df
        self.df2 = pd.read_excel(fp, sheet_name='温区分类字典')
        self.df3 = pd.read_excel(fp, sheet_name='配置参数')

        ########### 从excel导入特殊规则
        # self.df4 = pd.read_excel(fp, sheet_name='特殊规则')

        ########### 从seatable导入规则
        from seatable_api import Base, context
        st_app_name = 'ss-test1'
        st_api_token = '83d54f7aeda33c6b172c2e4535c1eb049fc14acb'
        server_url='https://cloud.seatable.cn'
        base = Base(st_api_token, server_url)
        base.auth()
        # res = base.get_metadata()
        ###################### 得到当前已经填写的所有的运单
        rows = base.list_rows('特殊规则')
        self.df4 = pd.DataFrame(rows)  # 得到seatable的数据    
        # print(self.df4, self.df4)    
        try:
            df['长*宽*高'] = df['内径长_mm'].astype(int).astype(str)+'*'+df['内径宽_mm'].astype(int).astype(str)+'*'+df['内径高_mm'].astype(int).astype(str)
            bin_col_list = '序号,存货序号,名称,接受温度类别,长*宽*高,路由限制条件'.split(',')
            self.df1[bin_col_list].to_excel(os.path.join(config.f_path['data_excel'], 'bin_箱子信息.xlsx'), index=False)
        except:pass
        self.df2.to_excel(os.path.join(config.f_path['data_excel'], 'bin_温区信息.xlsx'), index=False)


    def get_special_rule_dict(self):
        df = self.df4
        df = df.fillna('-1')

        df['cu_id'] = df['cu_id'].astype(int).astype(str)
        df['cp_id'] = df['cp_id'].astype(int).astype(str)
        col_list = df.columns.tolist()
        rule_list = []
        for i,r in df.iterrows():
            dict_i = dict(zip(col_list, r))
            rule_list.append(dict_i)
        special_rule_dict = {"rule_list":rule_list}
        f_path = os.path.join(config.f_path['data_json'], 'bin_special_rule_dict.json')
        mdjs.save_dict_to_json(special_rule_dict, file_path=f_path)   


        # print(df.shape[0])
    def get_bin_para_settings(self):
        df = self.df3
        res_dict = dict(zip(df['name'], df['value']))
        # print(res_dict)
        f_path = os.path.join(config.f_path['data_json'], 'bin_para_settings.json')
        mdjs.save_dict_to_json(res_dict, file_path=f_path)   

    def get_container_temperature_dict(self):            # 转换excel中的数据
        # df = deepcopy(self.df)
        df = self.df1
        df2 = self.df2

        df['长'] = [int(x) for x in df['内径长_mm']]
        df['宽'] = [int(x) for x in df['内径宽_mm']]
        df['高'] = [int(x) for x in df['内径高_mm']]
        df['有效高'] = df['高'].astype(int) - df['头部最小干冰深度_mm'].astype(int)-df['底部最小干冰深度_mm'].astype(int)
        df['成本'] = df['成本']*df['惩罚因子'].fillna(1)  #  太大的箱子需要加入惩罚

        df['长宽高'] = df['长'].astype(str)+'*'+df['宽'].astype(str)+'*'+df['高'].astype(str)
        # max_space_list = []  # 最大容积
        # for i in range(df.shape[0]):
        #     max_i = min(df['长'][i]*df['宽'][i]*df['有效高'][i], df['长'][i]*df['宽'][i]*df['高'][i]*(1-df['最小干冰容积_%'][i]/100))
        #     max_space_list.append(round(max_i/1000000, 2))
        # df['最大容积_L'] = max_space_list
        df = df['名称,长,宽,高,有效高,接受温度类别,成本,长宽高'.split(',')]

        container_dict = {}
        container_dict['bin_成本'] = dict(zip(df['名称'], df['成本'].round(3)))
        container_dict['bin_shape'] = dict(zip(df['名称'], df['长宽高']))


        for i,r in df.iterrows():
            max_vol_dict = {}
            vol1 = r['长']*r['宽']*r['高']/1000000
            vol2 = r['长']*r['宽']*r['有效高']/1000000

            accept_t_type_list = r['接受温度类别'].split(',')
            # print(accept_t_type_list)

            for t_type_j in accept_t_type_list:
                if t_type_j not in container_dict:  # 这个温度类型还没有加入
                    container_dict[t_type_j] = {}

                container_dict[t_type_j][r['名称']] = {
                    '长':r['长'],
                    '宽':r['宽'],
                    '高':r['高'],
                    '有效高':r['有效高'],
                    '容积':vol1,
                    '有效高容积':vol2,
                    '最大容积_L':'min(容积*非干冰比例, 有效高容积)',      # 最大容积_L
                    '成本':round(float(r['成本']), 4),
                }
        f_path = os.path.join(config.f_path['data_json'], 'bin_info.json')
        mdjs.save_dict_to_json(container_dict, file_path=f_path)

    def get_special_type_dict(self):
        df = self.df1
        print(df.shape[0])
        res_dict = {}
        df['特殊类型'] = df['特殊类型'].fillna('常规')
        group_df = df.groupby('特殊类型')
        for i in group_df:
            # print(i[0], '===================\n', i[1])
            res_dict[i[0]] = i[1]['箱子名称'].tolist()

        f_path = os.path.join(config.f_path['data_json'], 'bin_special_type.json')
        mdjs.save_dict_to_json(res_dict, file_path=f_path)        

        f_path = os.path.join(config.f_path['data_json'], 'bin_sto_id.json')
        container_sto_id = dict(zip(df['名称'], df['存货序号'].astype(int)))
        mdjs.save_dict_to_json(container_sto_id, file_path=f_path)

    def get_route_constraint(self):
        df = self.df1
        df['路由限制条件'] = df['路由限制条件'].fillna('').astype(str)

        res_dict = {}
        route_type_list = '航空*中铁*大巴*快递*生生专人*高铁*德邦*生生专车*专线*物流*京沪专线*沪皖专线*沪鄂专线'.split('*')
        split_v = [[j for j in i.split('*') if j] for i in df['路由限制条件']]
        container_route_dict = dict(zip(df['箱子名称'],split_v))
        # print(container_route_dict)

        res_dict = {}
        for r_j in route_type_list:
            res_dict[r_j] = []
            for k,v in container_route_dict.items():
                if r_j in v:
                    res_dict[r_j].append(k)
        f_path = os.path.join(config.f_path['data_json'], 'bin_route_constraint.json')
        mdjs.save_dict_to_json(res_dict, file_path=f_path)        

    def get_config_temperature_vol_percent(self):
        df = self.df2.fillna(0)
        df['EP_vol_p'] = (1-df['EP最小干冰体积比']/100).round(3)

        dict1 = dict(zip(df['config配置对应键'].astype(int), df['EP_vol_p']))
        dict2 = dict(zip(df['config配置对应键'].astype(int), df['温度类别']))
        f_path = os.path.join(config.f_path['data_json'], 'bin_config_temperature_vol.json')
        mdjs.save_dict_to_json({'temp_vol':dict1, 'temp_type':dict2}, file_path=f_path)    



    def run(self):
        self.get_special_rule_dict()
        self.get_container_temperature_dict()
        self.get_special_type_dict()
        self.get_route_constraint()
        self.get_config_temperature_vol_percent()
        self.get_bin_para_settings()

if __name__=='__main__':
    CleanContainerExcel().run()