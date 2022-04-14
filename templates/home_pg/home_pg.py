

import sys
sys.path.append('../../..')
import os
import config
import myutils.login_hash as mlh
import myutils.tencent_cos_action as mtca
import myutils.seatable_action as msa
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form

from typing import Optional
from fastapi import Cookie
from starlette.responses import RedirectResponse
from seatable_api.constants import ColumnTypes

templates = Jinja2Templates(directory='templates/')
router = APIRouter()


@router.get("/11")
def x11(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return {"test": "test_html!"}

@router.get("/")       ############# 默认模板，ec_模板.html等完成后替换
def home(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return RedirectResponse('/home_pg/seatable_cos_compare')

@router.get("/seatable_cos_compare")
def seatable_cos_compare(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    bucket_file_list = mtca.get_contained_file_list()

    mt = msa.MyseaTable(config.st_api_token)
    st_tb_list = mt.get_sub_tb_list()

    for f in bucket_file_list:
        if f not in st_tb_list:
            mt.base.add_table(f, lang='zh-cn')
        cols_list = [x.get('name')for x in mt.base.list_columns(f)]
        if 'cos_f_name' not in cols_list:
            mt.base.insert_column(table_name=f, column_name='cos_f_name', column_type=ColumnTypes.TEXT, column_key=None, column_data=None)

    return templates.TemplateResponse('home_pg/seatable_cos_compare.html', 
        context={
            'bucket_file_list': bucket_file_list,
            'request': request,
        })

@router.get("/add_cos_file_to_seatable")
def add_cos_file_to_seatable(request: Request,fname:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')

    f_list = mtca.get_prefix_file_list(fname)
    # print(f_list)
    return 'add_cos_file_to_seatable::::%s'%fname

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

