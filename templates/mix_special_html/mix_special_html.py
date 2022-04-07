

import sys
sys.path.append('../../..')
import os
import json
import config
import subprocess
import pandas as pd
from fastapi import APIRouter, Request, Form
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from typing import Optional
from fastapi import Cookie
from starlette.responses import RedirectResponse
from myutils.myrds import rds_sql_res
import pymysql.cursors
import numpy as np
import myutils.get_route_report as mgrr
templates = Jinja2Templates(directory='templates/')
router = APIRouter()

############# /mix_special_html/bin_results_daily_print?day_str=
@router.get("/bin_results_daily_print")
def bin_results_daily_print(request: Request, day_str:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    

    from seatable_api import Base, context
    st_app_name = 'ss-test1'
    st_api_token = '83d54f7aeda33c6b172c2e4535c1eb049fc14acb'
    server_url='https://cloud.seatable.cn'
    base = Base(st_api_token, server_url)
    base.auth()
    # res = base.get_metadata()

    ###################### 得到当前已经填写的所有的运单
    rows = base.list_rows('箱子不一致分析')
    df_stb = pd.DataFrame(rows)  # 得到seatable的数据
    print(df_stb.columns)
    if '运单号' not in df_stb.columns:
        df_stb = pd.DataFrame([], columns='运单号'.split(','))

    if '不一致原因' not in df_stb.columns:
        df_stb['不一致原因'] = ''
    df_stb = df_stb['运单号,不一致原因'.split(',')]
    df_stb.columns = 'c1,不一致原因'.split(',')
    df_stb['c1'] = df_stb['c1'].replace(np.nan, 0)
    df_stb['c1'] = df_stb['c1'].astype(int)
    df_stb['不一致原因'] = df_stb['不一致原因'].replace(np.nan, '')
    df_stb['不一致原因'] = df_stb['不一致原因'].astype(str)
    


    df_stb['不一致原因'] = df_stb['不一致原因'].fillna('')

    df = pd.read_excel(os.path.join(config.f_path['data_analysis_res'], '装箱算法/03箱型计算对比-2022/01箱型计算结果.xlsx'))

    df = pd.merge(df, df_stb, left_on='纸质运单编号', right_on='c1', how='left')

    # print(df['纸质运单编号'].tolist())
    date_list = df['创建时间'].unique().tolist()
    date_list.sort(reverse=True)
    date_list = date_list[:10]

    if day_str is None or day_str=='':
        day_str = df['创建时间'].unique().tolist()[0]
        # print('day_str........day_str', day_str)
        df = df[df['创建时间']==day_str].reset_index(drop=True)        
    else:
        df = df[df['创建时间']==day_str].reset_index(drop=True)
        # print('day_str........day_str', day_str, df.shape, df)

    ############################################################################ 从业务库查询
    # host='rm-uf607qm8l57p67nl2uo.mysql.rds.aliyuncs.com'
    # port=52319
    # user='bigdata'
    # password='j0^&WkpZbub#7tge'
    # db = 'oms'

    # if len(df['运单号'].tolist())>0:
    #     to_id_str = str(tuple(df['运单号'].tolist())).replace(',)', ')')
    #     sql=''' SELECT to_id,ow_create_username FROM `order_worksheet` where to_id in %s and ow_type in (1,6,8,11) '''%to_id_str
    #     print('sql....................................\n', sql)
    #     conn=pymysql.connect(host=host,port=port,user=user,password=password,db=db) # ,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor
    #     cur = conn.cursor()
    #     cur.execute(sql)
    #     res = list(cur.fetchall())
    #     df_creater = pd.DataFrame(res, columns='to_id,creater'.split(','))
    # else:
    #     df_creater = pd.DataFrame([], columns='to_id,creater'.split(','))

    ############################################################################ 从大数据查询
    if len(df['运单号'].tolist())>0:
        to_id_str = str(tuple(df['运单号'].tolist())).replace(',)', ')')
        
        sql=''' SELECT to_id,ow_create_username FROM `order_worksheet` where to_id in %s and ow_type in (1,6,8,11) '''%to_id_str
        print('sql....................................\n', sql)
        from impala.dbapi import connect
        conn = connect(host='101.132.107.216', port=21050)
        cur = conn.cursor()
        cur.execute('use kudu_pro;')
        cur.execute(sql)
        res = list(cur.fetchall())

        df_creater = pd.DataFrame(res, columns='to_id,creater'.split(','))
        print('####### 从大数据查询')
    else:
        df_creater = pd.DataFrame([], columns='to_id,creater'.split(','))


    # print(df_creater)
    df = pd.merge(df, df_creater, left_on='运单号', right_on='to_id', how='left')
    df = df.sort_values('creater').reset_index(drop=True)

    bin_list = []
    df['计算箱型'] = df['计算箱型'].fillna('0*0')
    df['纸质运单编号'] = df['纸质运单编号'].fillna(0)
    df['纸质运单编号'] = df['纸质运单编号'].astype(int)
    df['纸质运单编号'] = df['纸质运单编号'].astype(str)
    for i in df['计算箱型'].tolist():
        first_bin = i.split(';')[0]
        bin_name = first_bin.split('*')[1]
        bin_list.append(bin_name)
    df['主箱型'] = bin_list

    bin_list2 = []
    df['实际箱型'] = df['实际箱型'].fillna('0*0')
    for i in df['实际箱型'].tolist():
        first_bin = i.split(';')[0]
        bin_name = first_bin.split('*')[1]
        bin_list2.append(bin_name)

    df['real主箱型'] = bin_list2
    # print(df['real主箱型'][:5])

    df_bin_info = pd.read_excel(os.path.join(config.ROOT_PATH, 'data/bin/箱子算法数据维护.xlsx'), sheet_name='箱子信息')

    df_bin_info['y内径长_mm'] = df_bin_info['y内径长_mm'].fillna(0).astype(int)
    df_bin_info['y内径宽_mm'] = df_bin_info['y内径宽_mm'].fillna(0).astype(int)
    df_bin_info['y内径高_mm'] = df_bin_info['y内径高_mm'].fillna(0).astype(int)

    df_bin_info['箱子内径尺寸lwh'] = df_bin_info['y内径长_mm'].astype(str)+'*'+df_bin_info['y内径宽_mm'].astype(str)+'*'+df_bin_info['y内径高_mm'].astype(str)
    df_bin_info = df_bin_info['名称,箱子内径尺寸lwh'.split(',')]
    df = pd.merge(df, df_bin_info, left_on='主箱型', right_on='名称', how='left')
    df_bin_info.columns = '名称,实际箱子尺寸lwh'.split(',')
    df = pd.merge(df, df_bin_info, left_on='real主箱型', right_on='名称', how='left')


    # print(df.columns.tolist())

    en_cn_dict = {
        'sto_id':'运单号',
        'cp_id':'项目序号',
        'cu_id':'客户序号',
        'creater':'creater',
        'co_no':'纸质运单编号',
        'to_temperature':'运输温度',
        'shape_str':'货物尺寸',
        'name':'货物名称',
        'cal':'计算箱型',
        'real':'实际箱型',
        's_plan':'求解方案',
        '_ctime':'创建时间',
        'plan':'计划箱型',
        'bin_lwh':'箱子内径尺寸lwh',
        'real_bin_lwh':'实际箱子尺寸lwh',
        'alreason':'不一致原因',

    }

    df['货物尺寸'] = df['货物尺寸'].str.replace('==>', '|')
    df['货物尺寸'] = df['货物尺寸'].str.replace(';', '____ ') 
    df = df.drop_duplicates(subset=['运单号'])

    df0 = pd.DataFrame([], columns=df.columns)

    df1 = df[
    (df['实际箱型']!='0*0')
    &(df['计算VS实际']=='否')
    &(df['计划VS实际']=='是')
    &(df['货物类别数']==1)
    ].reset_index(drop=True)

    res_list = []
    for i,r in df1.iterrows():
        dict_i = {}
        for k,v in en_cn_dict.items():
            dict_i[k] = r[v]
            # dict_i['sto_id'] = r['运单号']
        res_list.append(dict_i)

    df2 = df[
    (df['实际箱型']!='0*0')
    &(df['计算VS实际']=='否')
    &(df['货物类别数']!=1)
    ].reset_index(drop=True)
    # print(df2.shape[0])

    res_list2 = []
    for i,r in df2.iterrows():
        dict_i = {}
        for k,v in en_cn_dict.items():
            dict_i[k] = r[v]
            # dict_i['sto_id'] = r['运单号']
        res_list2.append(dict_i)


    df3 = df[
    (df['实际箱型']!='0*0')
    &(df['计划VS实际']=='否')
    &(df['计算VS实际']=='否')
    &(df['货物类别数']==1)
    ].reset_index(drop=True)
    # print(df2.shape[0])

    res_list3 = []
    for i,r in df3.iterrows():
        dict_i = {}
        for k,v in en_cn_dict.items():
            dict_i[k] = r[v]
            # dict_i['sto_id'] = r['运单号']
        res_list3.append(dict_i)
    # print(date_list)

    df0 = df0.append(df1).append(df2).append(df3)
    try:
        df0.to_excel(os.path.join(config.ROOT_PATH, 'test.xlsx'), index=False)
    except:
        pass

    #### https://seatable.github.io/seatable-scripts-cn/
    # pip3 install seatable-api

    current_co_no_list = []
    rows = base.list_rows('箱子不一致分析')
    for r in rows:
        if '运单号' in r:
            current_co_no_list.append(str(r['运单号']))
    # print(current_co_no_list)

    ######### 获得需要更新的运单
    rows_data = []
    for i,r in df0.iterrows():
        if str(r['纸质运单编号']) not in current_co_no_list:
            print(r['纸质运单编号'], type(r['纸质运单编号']), '===', current_co_no_list)
            dict_i = {
                "运单号":str(r['纸质运单编号']),
                "处理人":r['creater'],
                "日期":r['创建时间'],
                "货物类别":str(r['货物类别数']),
                "计划VS实际":r['计划VS实际'],
            }
            rows_data.append(dict_i)
    if len(rows_data)>1:
        base.batch_append_rows('箱子不一致分析', rows_data)

    '''
    更新实例
    row_data = {
        "dcXS": "123"
    }
    base.update_row('Table1', 'U_eTV7mDSmSd-K2P535Wzw', row_data)
    '''
    return templates.TemplateResponse('mix_special_html/bin_results_daily_print.html', 
                context={
                    'request': request,
                    'res_list':res_list,
                    'res_list2':res_list2,
                    'res_list3':res_list3,
                    'date_list':date_list,
                }
            )


# /mix_special_html/test_form_deal
@router.get("/test_form_deal")
def test_form_deal(request: Request, data:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    

    data=json.loads(data)
    print(data, type(data))
    name_list = [x.get('name') for x in data['form_data']]
    value_list = [x.get('value') for x in data['form_data']]
    nv_dict = dict(zip(name_list, value_list))

    from seatable_api import Base, context
    st_app_name = 'ss-test1'
    st_api_token = '83d54f7aeda33c6b172c2e4535c1eb049fc14acb'
    server_url='https://cloud.seatable.cn'
    base = Base(st_api_token, server_url)
    base.auth()

    # rows = base.list_rows('箱子不一致分析')
    # print(len(rows), '测试seatable.........................')
    sql = '''  select _id from 箱子不一致分析 where 运单号='%s' '''%str(data.get('dialog_id'))
    res = base.query(sql)

    # print(res)
    if len(res)>0:
        s_id = res[0].get('_id')
        row_data = {}
        s1 = nv_dict.get('commentField').replace(' ','')
        s2 = nv_dict.get('ageRangeField').replace(' ', '')
        if s1!='':
            row_data['不一致原因'] = nv_dict.get('commentField')
        if s2!='':
            row_data['算法是否需要修正'] = nv_dict.get('ageRangeField')
        print('row_data...........', row_data)
        base.update_row('箱子不一致分析', s_id, row_data)    

    return {'dialog_id':data.get('dialog_id'), 's1':s1}


# /mix_special_html/download_seatable_reason
@router.get("/download_seatable_reason")
def download_seatable_reason(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    

    from seatable_api import Base, context
    st_app_name = 'ss-test1'
    st_api_token = '83d54f7aeda33c6b172c2e4535c1eb049fc14acb'
    server_url='https://cloud.seatable.cn'
    base = Base(st_api_token, server_url)
    base.auth()

    rows = base.list_rows('箱子不一致分析')

    df = pd.DataFrame(rows)
    s_cols = '运单号,不一致原因,算法是否需要修正,处理人,日期,货物类别,计划VS实际'.split(',')
    df = df[s_cols]
    f_path = os.path.join(config.f_path['data_excel'], 'bin_seatable_装箱不一致原因分析.xlsx')

    df.to_excel(f_path, index=False)
    # http://127.0.0.1:5004/file_tree/file_str?eco_f_path=data/bin/%E7%AE%B1%E5%AD%90%E7%AE%97%E6%B3%95%E6%95%B0%E6%8D%AE%E7%BB%B4%E6%8A%A4.xlsx
    # eco_f_path = os.path.join(config.f_path[''])
    return RedirectResponse('/file_tree/file_str?eco_f_path=%s'%f_path)
    # return {'test':1}


# /mix_special_html/route_exists_real_rout_list
@router.get("/route_exists_real_rout_list")
def route_exists_real_rout_list(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    

    f_path = os.path.join(config.f_path['data_json'], 'route_exists_real_route_list.json')             # 箱子的基本信息字典
    r_route_dict = json.load(open(f_path, "rb"))

    new_list = []
    for k,v in r_route_dict.items():
        v['from_to_en'] = k
        new_list.append(v)

    new_list = sorted(new_list, key = lambda i: i['order_num'], reverse=True)

    # r_k_list = list(r_route_dict.keys())
    # print(r_k_list[:10])
    return templates.TemplateResponse('mix_special_html/route_exists_real_rout_list.html', 
                context={
                    'request': request,
                    'new_list':new_list,
                }
            )

@router.get("/download_region_pickle_excel")
def download_region_pickle_excel(request: Request,region_pickle:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    f_path = os.path.join(config.f_path['route_region_df'], region_pickle)
    df = pd.read_pickle(f_path)

    f_path = os.path.join(config.f_path['temp'], 'route_region_df.xlsx')
    df.to_excel(f_path, index=False)
    return FileResponse(f_path, filename=region_pickle.replace('.pickle', '.xlsx'))
    
# /mix_special_html/route_report
@router.get("/route_report")
def route_report(request: Request,se_str:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    c1 = se_str.split('-->')[0]
    c2 = se_str.split('-->')[1]

    mgrr.get_report(c1=c1,c2=c2)
    report_path = os.path.join(config.f_path['temp'], 'route_report/路由报告.docx')
    return FileResponse(report_path, filename='%s-%s路由报告.docx'%(str(c1), str(c2)))



# /mix_special_html/duplicate_table_col_page
@router.get("/duplicate_table_col_page")
def duplicate_table_col_page(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    return templates.TemplateResponse('mix_special_html/duplicate_table_col_page.html', 
                context={
                    'request': request,
                }
            )

# /mix_special_html/route_report
@router.get("/duplicate_table_col_search")
def duplicate_table_col_search(request: Request,tb_name : str, col_name : str,where_str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    ############################################################################ 从业务库查询
    host=config.host
    port=config.port
    user=config.user
    password=config.password
    db = config.db

    
    try:
        sql = 'SELECT %s from %s %s'%(col_name, tb_name, where_str)
        print('sql....................................\n', sql)
        conn=pymysql.connect(host=host,port=port,user=user,password=password,db=db) # ,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor
        cur = conn.cursor()
        cur.execute(sql)
        res = list(cur.fetchall())
        df = pd.DataFrame(res, columns='col1'.split(','))


        # df = pd.read_excel('duplicate_table_col_search.xlsx')
        vc = df['col1'].value_counts()
        df = pd.DataFrame(vc)
        df.insert(0, '名称', df.index)
        df.rename(columns={'col1':'重复次数'}, inplace=True)
        df = df[df['重复次数']>1].reset_index(drop=True)

        res_path = os.path.join(config.f_path['temp'], '%s_%s_重复名称.xlsx'%(tb_name, col_name))
        print(res_path)
        df.to_excel(res_path, index=False)
        return FileResponse(res_path)

    except Exception as e:
        return str(e)







