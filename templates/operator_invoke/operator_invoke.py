

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

templates = Jinja2Templates(directory='templates/')
router = APIRouter()

############# /operator_invoke/polygon_batch?dname=
@router.get("/analysis_list")
def analysis_list(request: Request,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    df = pd.read_excel(os.path.join(config.ROOT_PATH, 'data_analysis/说明.xlsx'))
    df =df[df['is_use']==1].reset_index(drop=True)
    operator_list_dict = {}
    res_folder_list = df['res_folder'].unique().tolist()
    for res_i in res_folder_list:
        df_i = df[df['res_folder']==res_i].reset_index(drop=True)
        operator_list_dict[res_i] = []
        for j,r in df_i.iterrows():
            res_path = '%s/%s'%(r['res_folder'], r['res_file'])
            end_p = os.path.join(config.f_path['data_analysis_res'],res_path)
            print(end_p)
            if os.path.exists(end_p) is False:
                font_color='red'
            else:
                font_color = 'purple'
            dict_ij = {
            'font_color':font_color,
            'name':r['res_file'],
            'pyname':r['code_name'],
            'bg_color':r['bg_color'],
            'url':'/operator_invoke/data_analysis_run_py_file?py_path_str=data_analysis/%s/%s'%(r['code_folder'], r['code_name'])
            }
            operator_list_dict[res_i].append(dict_ij)

    return templates.TemplateResponse('operator_invoke/operator_list_dict.html', 
                context={
                    'request': request,
                    'operator_list_dict':operator_list_dict
                }
            )

############# /operator_invoke/run_py_file?py_path_str=
@router.get("/data_analysis_run_py_file")
def data_analysis_run_py_file(request: Request,py_path_str: str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    df = pd.read_excel(os.path.join(config.ROOT_PATH, 'data_analysis/说明.xlsx'))
    df['py_path_str'] = 'data_analysis/'+df['code_folder']+'/'+df['code_name']
    df = df[df['py_path_str']==py_path_str].reset_index(drop=True)
    if df.shape[0]==0:
        return {'msg':'找不到py_path_str在data_analysis/说明.xlsx中对应的信息'}
    try:
        with open(py_path_str,'r', encoding='utf-8') as f:
            exec(f.read())
    except Exception as e:
        return {'mgs':str(e)}

    ##########  测试专用
    # with open(py_path_str,'r', encoding='utf-8') as f:
    #     exec(f.read())

    res_dict = dict(zip(df.columns, df.iloc[0]))
    redirect_str = '/file_tree/image_data_tree?eco_dir_path=data_analysis_res&echo2_str=%s/%s'%(res_dict['res_folder'], res_dict['res_file'])
    return RedirectResponse(redirect_str)

############# /operator_invoke/polygon_batch?dname=
@router.get("/operator_list")
def operator_list(request: Request,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    operator_list_dict = {
        "装箱算法":[
            {'name':'装箱算法json文件更新','pyname':'运行', 'url':'/operator_invoke/bin_data_refresh'},
            ],
        "路由推荐":[
            {'name':'路由数据全量清洗','pyname':'运行', 'url':'/operator_invoke/route_data_refresh_all'},
            ],  
        "电子栏杆分析":[
            {'name':'电子栏杆批量画图','pyname':'运行', 'url':'/operator_invoke/polygon_batch?dname='},
        ],
        "pickle更新":[
            {'name':'pickle补充下载','pyname':'运行', 'url':'/operator_invoke/data_refresh'},
            {'name':'pickle全量下载','pyname':'谨慎运行', 'url':'/operator_invoke/data_refresh_all'},
            ],            
    }
    return templates.TemplateResponse('operator_invoke/operator_list_dict.html', 
                context={
                    'request': request,
                    'operator_list_dict':operator_list_dict
                }
            )


@router.get("/route_data_refresh_all")
def route_data_refresh_all(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    try:
        import algorithms.algori_route.s21_route_clean_local_pickle as a
        A = a.CleanLocalPickle()
        A.run()

        import algorithms.algori_route.s22_route_region_df_route as b
        b.run() 

        import algorithms.algori_route.s30_get_node_connection as c
        c.run() 

        redirect_str = '/file_tree/tree?eco_dir_path=%s'%config.f_path['log_daily']
        return RedirectResponse(redirect_str)
    except Exception as e:
        return str(e)
        


############# /operator_invoke/polygon_batch?dname=
@router.get("/polygon_batch")
def polygon_batch(request: Request, dname:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    try:
        import algorithms.algori_polygon.s55_batch_test as aps55
        dname = '坐标点测试2'
        A =  aps55.BatchTest(dname+'.xlsx')
        A.run()
        return {"message":"success"}
    except Exception as e:
        return str(e)

############# /operator_invoke/polygon_batch?dname=
@router.get("/data_refresh")
def data_refresh(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    try:
        import data_analysis.data_offline.s02_get_data_from_kudu as adofs02
        adofs02.get_data_pickle(not_update_bool=True)
        redirect_str = '/file_tree/tree?eco_dir_path=%s'%config.f_path['log_daily']
        return RedirectResponse(redirect_str)
    except Exception as e:
        return str(e)

@router.get("/data_refresh_all")
def data_refresh_all(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    try:
        import data_analysis.data_offline.s02_get_data_from_kudu as adofs02
        adofs02.get_data_pickle(not_update_bool=False)
        redirect_str = '/file_tree/tree?eco_dir_path=%s'%config.f_path['log_daily']
        return RedirectResponse(redirect_str)
    except Exception as e:
        return str(e)

############# /operator_invoke/polygon_batch?dname=        装箱数据离线
@router.get("/bin_data_refresh")
def bin_data_refresh(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    try:
        import algorithms.algori_bin.s01_history_clean as a
        A = a.ContainerTemperature()
        A.run()

        import algorithms.algori_bin.s31_container_input_json as b
        B = b.CleanContainerExcel()
        B.run() 
        redirect_str = '/file_tree/tree?eco_dir_path=%s'%config.f_path['log_daily']
        return RedirectResponse(redirect_str)
    except Exception as e:
        return str(e)
        