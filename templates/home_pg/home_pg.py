

import sys
sys.path.append('../../..')
import os
import config
import pandas as pd
import myutils.login_hash as mlh
import myutils.tencent_cos_action as mtca
import myutils.seatable_action as msa
import myutils.dict_json_saver as mdjs

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form

from typing import Optional
from fastapi import Cookie
from starlette.responses import RedirectResponse
from seatable_api.constants import ColumnTypes

templates = Jinja2Templates(directory='templates/')
router = APIRouter()

def refresh_seatable(fname):
    f_list = mtca.get_prefix_file_list(fname)
    cos_exists_tag_list = [x['ETag'] for x in f_list]

    mt = msa.MyseaTable(config.st_api_token)
    seatable_df = mt.get_tb_df(fname)

    seatable_df.to_pickle(os.path.join(config.f_path['data_excel'], '%s.pickle'%fname))
    print(seatable_df.columns)
    if 'ETag' not in seatable_df.columns:
        tag_list = []
        tag_dict = {}
        seatable_df['ETag'] = ''
    else:
        tag_list = seatable_df['ETag'].tolist()
        tag_dict = dict(zip(seatable_df['ETag'], seatable_df['_id']))

    new_rows = []           # 新增加的列
    update_rows = []        # 更新的列
    no_cos_rows = []        # cos中没有的行
    for i,r in seatable_df.iterrows():
        if r['ETag'] not in cos_exists_tag_list:
            dict_i = {
                "row_id": r['_id'],
                "row": {'cos_state':'false'}                
            }
            no_cos_rows.append(dict_i)
    mt.base.batch_update_rows(fname, no_cos_rows)

    for dict_f in f_list:
        if dict_f['ETag'] in tag_list:  # 更新
            dict_i = {
                "row_id": tag_dict[dict_f['ETag']],
                "row": dict_f
            }
            update_rows.append(dict_i)
            pass
        else:
            dict_f['cos_state'] = 'true'
            new_rows.append(dict_f)
            pass
    mt.base.batch_update_rows(fname, update_rows)
    mt.base.batch_append_rows(fname, new_rows)    

@router.get("/11")
def x11(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return {"test": "test_html!"}

@router.get("/")       ############# 默认模板，ec_模板.html等完成后替换
def home(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return RedirectResponse('/home_pg/seatable_cos_compare?c_tb=')

@router.get("/seatable_cos_compare")
def seatable_cos_compare(request: Request,c_tb:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    bucket_file_list = mtca.get_contained_file_list()

    if c_tb=='yes':   # 创建新的表格
        add_dict = {
            '名称':[ColumnTypes.TEXT,300],  # 列属性和宽度
            'url':[ColumnTypes.URL,20],
            'cos更新时间':[ColumnTypes.DATE,100],
            'ETag':[ColumnTypes.TEXT,20],
            'Size':[ColumnTypes.NUMBER,20],
            'cos_state':[ColumnTypes.SINGLE_SELECT,60],
            '类别':[ColumnTypes.SINGLE_SELECT,150],
            '详细说明':[ColumnTypes.LONG_TEXT,100],
            '说明文件':[ColumnTypes.FILE,100],
        }# '文件名,url,cos更新时间,ETag,Size'.split(',')

        mt = msa.MyseaTable(config.st_api_token)
        st_tb_list = mt.get_sub_tb_list()
        for f in bucket_file_list:
            if f not in st_tb_list:
                mt.base.add_table(f, lang='zh-cn')

            cols_list = [x.get('name')for x in mt.base.list_columns(f)]
            for k,v in add_dict.items():
                if k not in cols_list:
                    mt.base.insert_column(table_name=f, column_name=k, column_type=v[0], column_key=None, column_data=None)

                mt.base.resize_column(table_name=f, column_key=k, new_column_width=v[1])

                if k=='cos_state':
                    mt.base.add_column_options(f, k, [
                            {"name": "true", "color": "#C1FFC1", "textColor": "#000000"},
                            {"name": "false", "color": "#EE30A7", "textColor": "#000000"},
                    ])
    return templates.TemplateResponse('home_pg/seatable_cos_compare.html', 
        context={
            'bucket_file_list': bucket_file_list,
            'request': request,
        })

@router.get("/add_cos_file_to_seatable")
def add_cos_file_to_seatable(request: Request,fname:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    refresh_seatable(fname)
    return 'add_cos_file_to_seatable::::%s'%fname

@router.get("/refresh_all_tb")
def refresh_all_tb(request: Request,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    bucket_file_list = mtca.get_contained_file_list()
    mdjs.save_dict_to_json({'bucket_file_list':bucket_file_list}, os.path.join(config.f_path['data_json'], 'bucket_file_list.json'))
    try:
        for f in bucket_file_list:
            refresh_seatable(f)
        return RedirectResponse('/home_pg/seatable_cos_compare?c_tb=')
    except Exception as e:
        return str(e)

@router.get("/cos_one_file")
def cos_one_file(request: Request,fname:str,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    df = pd.read_pickle(os.path.join(config.f_path['data_excel'], '%s.pickle'%fname))
    print(df)
    return fname

@router.get("/home")
def home11(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return templates.TemplateResponse('home_pg/ec_模板.html', context={'request': request,})

@router.get("/echarts_test")
def echarts_test(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return templates.TemplateResponse('home_pg/echarts_test.html', context={'request': request,})

# http://127.0.0.1:5004/seatable_iframe
@router.get("/seatable_iframe")
def seatable_iframe(request: Request,fn:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return templates.TemplateResponse('home_pg/%s'%fn, 
        context={
        'request': request, 
        })

