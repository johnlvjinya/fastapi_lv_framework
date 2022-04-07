
import sys
sys.path.append('../../..')
import os
import config
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse

import json
from typing import Optional
from fastapi import Cookie
from starlette.responses import RedirectResponse
from starlette.responses import FileResponse
from jinja2 import Environment, FileSystemLoader

templates = Jinja2Templates(directory='templates/')
router = APIRouter()

@router.get("/test")
def test(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return 'test'

# /echarts_pg/engine_html_list
@router.get("/engine_html_list")
def engine_html_list(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    j_list = os.listdir('templates/echarts_pg/engine_html')

    j_dict = {}
    for j in j_list:
        j_name = j.replace('.html', '')  # 文件的名称
        print(j_name)
        class_split_list = j_name.split('_')
        if len(class_split_list)>1:
            j_class = class_split_list[0]
        else:
            j_class = 'default'

        if j_class not in j_dict:
            j_dict[j_class] = []

        dict_x1 = {"name":j_name}
        j_dict[j_class].append(dict_x1)

    class_len = len(j_dict.keys())
    from colour import Color
    red = Color("#E066FF")
    color_list = [str(x) for x in  list(red.range_to(Color("limegreen"),class_len))]
    color_c_dict = {}
    for i,k1 in enumerate(list(j_dict.keys())):
        color_c_dict[k1] = color_list[i]
    return templates.TemplateResponse('echarts_pg/engine_html_list.html', context={'request': request,'j_dict':j_dict, 'color_c_dict':color_c_dict})

@router.get("/engine_html_open")
def engine_html_list(request: Request, hname:str,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    t_path = 'echarts_pg/engine_html/%s.html'%hname
    return templates.TemplateResponse(t_path, context={'request': request})

# 127.0.0.1:5004/echarts_pg/engine_json_list
@router.get("/engine_json_list")
def engine_json_list(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    j_list = os.listdir('templates/echarts_pg/engine_json')

    j_dict = {}
    for j in j_list:
        j_name = j.replace('.json', '')  # 文件的名称
        class_split_list = j_name.split('_')
        if len(class_split_list)>1:
            j_class = class_split_list[0]
        else:
            j_class = 'default'

        if j_class not in j_dict:
            j_dict[j_class] = []
        ### 构造当前的字典
        if os.path.exists('templates/echarts_pg/engine_js/%s.js'%j_name) is False:
            js_exists = 'no'
        else:
            js_exists= 'yes'
        dict_x1 = {"name":j_name, "js_exists":js_exists}
        j_dict[j_class].append(dict_x1)

    class_len = len(j_dict.keys())
    from colour import Color
    red = Color("#E066FF")
    color_list = [str(x) for x in  list(red.range_to(Color("limegreen"),class_len))]
    color_c_dict = {}
    for i,k1 in enumerate(list(j_dict.keys())):
        color_c_dict[k1] = color_list[i]
    return templates.TemplateResponse('echarts_pg/engine_json_list.html', context={'request': request,'j_dict':j_dict, 'color_c_dict':color_c_dict})


@router.get("/engine_json_run")
def engine_json_run(request: Request, jname:str,run_type:str,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    print(jname, run_type)
    j_path = 'templates/echarts_pg/engine_json/%s'%jname
    if run_type=='delete':
        if config.python =='python':
            try:os.rename(j_path, 'templates/echarts_pg/engine_json_history/%s'%jname)
            except:pass
        return RedirectResponse('/echarts_pg/engine_json_list')

    j_dict = json.load(open(j_path, "rb"))
    env = Environment(loader = FileSystemLoader("./"))
    js_t_path = 'templates/echarts_pg/ec_templates'
    html_path = 'templates/echarts_pg/engine_html/%s.html'%jname.replace('.json', '')  # 生成的js保存的路径 

    if run_type=='cover':
        js_path = 'static/js_ec_engine/%s.js'%jname.replace('.json', '')  # 生成的js保存的路径 
    if run_type=='copy':
        js_path = 'static/js_ec_engine/%s_copy.js'%jname.replace('.json', '')  # 生成的js保存的路径 

    with open(js_path, 'w', encoding='utf-8') as f2:
        for e_i in j_dict.get('e_list'):
            # print(exist_js_list)
            template_js = env.get_template('%s/%s.js'%(js_t_path,e_i['p_type']))
            content_js = template_js.render(js_data_url=e_i['d_url'], rd_id=e_i['c_name'], plt_type=e_i['p_type'])
            f2.write(content_js)

    with open(html_path, 'w', encoding='utf-8') as f3:
        template_html = env.get_template('templates/echarts_pg/basic_echarts_html_father.html')
        content_html = template_html.render(
            lp='{%',
            rp='%}',
            ll='{{',
            rr='}}',
            j_dict=j_dict,
            js_name=jname.replace('.json', '')
            )
        f3.write(content_html)

    return RedirectResponse('/echarts_pg/engine_html_open?hname=%s'%jname.replace('.json', ''))


































# http://127.0.0.1:5004/echarts_pg/ec_json_path?jpath=templates/echarts_pg/ec_json_test/bar.json
@router.get("/ec_json_path")
def ec_json_path(request: Request, jpath:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    mydict = json.loads(open(jpath, "rb").read())
    return mydict

# http://127.0.0.1:5004/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=bar.json
@router.get("/ecj")
def ec_json_path(request: Request, d:str,j, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')

    file_dict = config.f_path
    if d in file_dict:
        real_path = os.path.join(file_dict[d], j)
    else:
        real_path = os.path.join(d, j)

    mydict = json.loads(open(real_path, "rb").read())
    return mydict












































































# echarts_pg/echarts_code_engine
@router.get("/echarts_code_engine")
def echarts_code_engine(request: Request, js_data_url:str,container_id:str,plt_type:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    env = Environment(loader = FileSystemLoader("./"))
    ec_path = 'templates/echarts_pg/ec_templates'
    # print(exist_js_list)
    template_js = env.get_template('%s/%s.js'%(ec_path,plt_type))
    content_js = template_js.render(js_data_url=js_data_url, rd_id=container_id, plt_type=plt_type)
    f_path = os.path.join(config.f_path['data_excel'], 'ec_render.txt')
    with open(f_path, 'w', encoding='utf-8') as f2:
        # print(content_js, file=f2)
        f2.write(content_js)
    return FileResponse(f_path)

# echarts_pg/echarts_code_engine_list
@router.get("/echarts_code_engine_list")
def echarts_code_engine_list(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    exist_js_list = [x.replace('.js', '') for x in os.listdir('templates/echarts_pg/ec_templates')]

    jps_str = 'templates/echarts_pg/ec_json_test'
    json_test_list = os.listdir(jps_str)
    context={
            'exist_js_list':exist_js_list,
            'request': request,
            'json_test_list':json_test_list,
            'jp_path_str':'/echarts_pg/ecj?d=%s&j='%jps_str
            }    
    return templates.TemplateResponse('echarts_pg/echarts_code_engine.html', context=context)



