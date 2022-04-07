
import sys
sys.path.append('../..')

import os
import json
import config
import pandas as pd
import myutils.dict_json_saver as mdjs


class ContainerTemperature():
    def __init__(self):
        pass

    def check_box_stock_id_name(self):
        f_path = os.path.join(config.f_path['kudu_table_pickle'], 'stock.pickle')
        df1 = pd.read_pickle(f_path)
        df1 = df1[['sto_id','stt_id','sto_no', 'sto_name']]
        m_type_dict = {}
        for k in [5,6,51,52,9]:m_type_dict[k]='箱子'
        for k in [4,36]:m_type_dict[k]='温度计'
        for k in [50]:m_type_dict[k]='鼎为定位器'

        df1['stt_id']=df1['stt_id'].map(m_type_dict)  # 保存所有箱子的信息
        print(df1.columns)
        df1 = df1[df1['stt_id']=='箱子']

        f_path = os.path.join(config.ROOT_PATH, 'data/bin/箱子算法数据维护.xlsx')
        df2 = pd.read_excel(f_path)

        df = pd.merge(df2, df1, left_on='名称', right_on='sto_name', how='left')
        f_path = os.path.join(config.f_path['data_excel'], 'bin_箱子存货类型检查.xlsx')
        df.to_excel(f_path, index=False)

    def m_plus_case_list(self):
        f_path1 = os.path.join(config.f_path['kudu_table_pickle'], 'tms_material_plan_config.pickle')
        df1 = pd.read_pickle(f_path1)
        df1.columns = ['c_'+x for x in df1.columns]
        # print(df1)
        # print('df1.columns', df1.columns)

        f_path2 = os.path.join(config.f_path['kudu_table_pickle'], 'tms_material_plan_config_detail.pickle')
        df2 = pd.read_pickle(f_path2)   
        c_list = df2.columns.tolist()
        for i,col in enumerate(c_list):
            if not col:
                c_list[i] = 'col_'+str(i)
        c_list = ['d_'+i for i in c_list]
        df2.columns = c_list
        # print(df2)
        # print('df2.columns', df2.columns)
        # print(df2)
        # print('箱子数量...', len(df2['d_存货名称'].unique().tolist()))
        df = pd.merge(df1, df2, left_on='c_omc_id', right_on='d_omc_id', how='left')
        df = df[df['d_omcd_visible']==1]  # omcd_visible:状态 1正常 2删除
        # print(df)
        # print('df.columns', df.columns)


        df = df[df['c_omc_type']==2]  # omc_type:类型 1普通配置 2特殊配置

        ############# 测试箱型可以匹配的所有的温度
        '''
        'c_温度区间',c_omc_tem_name
        'c_温度id',c_omc_tem_id
        'c_温度区间',c_omc_tem_name
        'c_城市列表',c_omc_regionname_list
        'c_城市列表id',c_omc_regionid_list
         'c_开始时间', c_omc_start_time
         'c_结束时间',c_omc_stop_time
         'c_类型 1普通配置 2特殊配置',c_omc_type
         'd_存货id'd_omcd_sto_id
        '''
        s_list = ['c_omc_tem_name','c_omc_tem_id','c_omc_tem_name','c_omc_regionname_list','c_omc_regionid_list', 
        'c_omc_start_time', 'c_omc_stop_time','c_omc_type','d_omcd_sto_id']
        df = df[s_list]
        df['c_omc_start_time']=pd.to_datetime(df['c_omc_start_time'].values, unit='s', utc=True).tz_convert('Asia/Shanghai').strftime("%Y-%m-%d")
        df['c_omc_stop_time']=pd.to_datetime(df['c_omc_stop_time'].values, unit='s', utc=True).tz_convert('Asia/Shanghai').strftime("%Y-%m-%d")
        # print(df['c_开始时间'])

        stock_df = pd.read_pickle(os.path.join(config.f_path['kudu_table_pickle'], 'stock.pickle'))
        s_list = ['sto_id','sto_name'] # 'sto_id: 存货序号','sto_name:存货名称'
        stock_df = stock_df[s_list]
        stock_df.columns = ['stock_'+i for i in s_list]
        df = pd.merge(df, stock_df, left_on='d_omcd_sto_id', right_on='stock_sto_id', how='left')  # omcd_sto_id:存货id, 
        test_container_list = df['stock_sto_name'].unique().tolist()  ########## 数据库中的箱子

        box_hand_df = pd.read_excel(os.path.join(config.ROOT_PATH, 'data/bin/箱子算法数据维护.xlsx'))  ######## 算法维护的箱子
        container_list2 = box_hand_df['名称'].tolist()
        not_hand_c_list = []
        for c_i in test_container_list:
            if c_i not in container_list2:
                not_hand_c_list.append(c_i)

        ################################

        # fp = os.path.join(config.ROOT_PATH, 'test.xlsx')
        # df.to_excel(fp, index=False)

        df1 = df[df['c_omc_type']==2].astype(str)
        df1['相同类型拼凑'] = df1['c_omc_tem_id']+'&@&'+df1['c_omc_regionid_list']+'&@&'+df1['c_omc_start_time']+'&@&'+df1['c_omc_stop_time']
        # print(df1)
        condition_list = df1['相同类型拼凑'].unique().tolist()
        spectial_list = {}
        for c in condition_list:
            c_split_list = c.split('&@&')
            dict_i = {}
            # dict_i['temp_id'] = int(c_split_list[0])
            dict_i['region_list'] = [int(x) for x in c_split_list[1].split(',')]
            dict_i['start_time'] = c_split_list[2]
            dict_i['end_time'] = c_split_list[3]

            df_c_i = df1[df1['相同类型拼凑']==c]

            m_p_List = []
            for bin_x in df_c_i['stock_sto_name'].tolist():
                if 'M+' in bin_x:
                    m_p_List.append(bin_x)
            dict_i['accept_bins'] = m_p_List
            spectial_list[int(c_split_list[0])] = dict_i
        # print(len(condition_list))
        # print(spectial_list)

        # df2 = df[df['c_类型 1普通配置 2特殊配置']==1]
        # normal_dict = {}
        # group_df = df2.groupby('c_温度id')

        # for g in group_df:
        #     normal_dict[g[0]] = g[1]['stock_存货名称'].tolist()
        # res = {
        #     'm_plus_case_list':spectial_list,  # 特殊情况的箱子
        #     # 'normal_temp_dict':{},      # 正常情况的箱子
        #     # '零度以下平均温度':{}  # 箱子最低温度的字典
        #     }

        f_path = os.path.join(config.f_path['data_json'], 'bin_m_plus_case_list.json')
        mdjs.save_dict_to_json(spectial_list, file_path=f_path)

    def get_route_dict(self):
        df = pd.read_pickle(os.path.join(config.f_path['kudu_table_pickle'], 'route_type.pickle')).astype(str)
        mydict = {}
        mydict['cn_en_dict'] = dict(zip(df['rt_name'], df['rt_id']))
        mydict['en_cn_dict'] = dict(zip(df['rt_id'], df['rt_name']))
        mdjs.save_dict_to_json(mydict, os.path.join(config.f_path['data_json'], 'bin_route_type_dict.json'))
        return mydict


    def run(self):
        self.m_plus_case_list()
        self.get_route_dict()
        self.check_box_stock_id_name()



if __name__=='__main__':
    ContainerTemperature().run()





