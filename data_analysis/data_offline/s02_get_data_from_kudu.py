
import sys
sys.path.append('../..')

import os
import config
import pandas as pd
import myutils.kudu_api as mka
from myutils.func_decorated import log_func_time
import data_analysis.data_offline.s01_bussiness_tb_info as dksb
import myutils.mylogger as mml


########## 引用多进程
# from multiprocessing import Pool
# def get_impala_db_tb(tb):
#     df2 = MIC.get_tb_df(tb)
#     df2.to_pickle(os.path.join(config.f_path['kudu_table_pickle'], '%s.pickle'%tb))
#     return 1


def get_data_pickle(not_update_bool=config.NOT_UPDATE_BOOL):
    # n = os.cpu_count()
    # pool = Pool(processes=max(2,n-2))  # 默认cpu_count()
    MIC = mka.MyImpalaConnect(host=config.kudu_host, port=config.kudu_port)

    ############ 连接kudu数据库
    kdu_tb_list = MIC.get_tb_list() 

    ########### 查看与算法相关的表
    df = pd.read_excel(os.path.join(config.ROOT_PATH,'data/业务表算法相关离线.xlsx'))
    df = df[df['算法相关']=='YES'].reset_index(drop=True)
    df['q_str'] = df['q_str'].fillna('')

    ############ 目前已经下载的Pickle
    existed_file_list = os.listdir(config.f_path['kudu_table_pickle'])

    ########### 表结构生成
    f2_path = os.path.join(config.f_path['data_excel'], 'dev_表结构字段对应.xlsx')
    writer=pd.ExcelWriter(f2_path)

    ############# 更新表
    for tb in df['表'].tolist():
        if tb in kdu_tb_list:
            # print('test1')
            df_tb = MIC.get_tb_describe(tb)
            tb_col_s = 'col_en,col_cn,col_type'.split(',')
            df_tb[tb_col_s].to_excel(writer,sheet_name=tb,index=False)
        else:
            print('test2............没有表')
    writer.save()

    for i,r in df.iterrows():
        tb = r['表']
        if 'where' in r['q_str']:
            q_str = '%s %d'%(r['q_str'], r['时间戳'])
        else:
            q_str = ''

        if tb in kdu_tb_list:
            if not_update_bool and '%s.pickle'%tb in existed_file_list:  # 不用覆盖
                print('no need to refresh data.............%s'%tb) 
            else:
                df1 = MIC.get_tb_df_limit10(tb)
                df2 = MIC.get_tb_df(tb, q_str)
                print('download.............%s'%tb, '一共有%s行数据'%str(df2.shape[0]))
                df1.to_excel(os.path.join(config.f_path['kudu_table_pickle'], '%s.xlsx'%tb), index=False)
                df2.to_pickle(os.path.join(config.f_path['kudu_table_pickle'], '%s.pickle'%tb))
                # df2.to_csv(os.path.join(config.f_path['kudu_table_pickle'], '%s.csv'%tb), index=False)
                
        else:
            print('!!!!表不存在.............%s'%tb)

    # from_bussiness_tb_list = ['temperature','tms_material_plan_config', 'tms_material_plan_config_detail']  # 'tms_material_plan_config', 'tms_material_plan_config_detail'
    
    # lg.info('from_bussiness_tb_list:%s'%(str(from_bussiness_tb_list)))
    # print('===========================业务补充表,注意不要删，否则字段可能报错')
    # for tb in from_bussiness_tb_list:
    #     if config.NOT_UPDATE_BOOL and '%s.pickle'%tb in existed_file_list:  # 不用覆盖
    #         print('no need to refresh data.............%s'%tb) 
    #     else:
    #         GTE = dksb.GetTableToExcel()
    #         print('download.............%s'%tb)
    #         df1,N = GTE.get_one_tb(tb)
    #         df1[:min(10, N)].to_excel(os.path.join(config.f_path['kudu_table_pickle'], '%s.xlsx'%tb), index=False)
            
    #         df1.to_pickle(os.path.join(config.f_path['kudu_table_pickle'], '%s.pickle'%tb))

if __name__=='__main__':
    # get_data_pickle(not_update_bool=True)
    get_data_pickle(not_update_bool=False)

