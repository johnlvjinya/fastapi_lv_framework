
import sys
sys.path.append('../../..')
import os
import json
import config
import myutils.login_hash as mlh
import pandas as pd
import myutils.myfile_tree as mmft
from fastapi import APIRouter, Request, Form
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse

from typing import Optional
from fastapi import Cookie
from starlette.responses import RedirectResponse

templates = Jinja2Templates(directory='templates/')
router = APIRouter()
file_dict = config.f_path

@router.get("/11")
def x11(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    return {"test": "test_html!"}

# http://127.0.0.1:5004/file_tree/file_str?eco_f_path=
@router.get('/file_str')                 # 检查数据不一致的问题
def file_str(request: Request, eco_f_path:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    fi_path = eco_f_path # 'log/装箱算法/01请求说明.txt'
    # print(fi_path, '<================||==')

    f_lines = []
    f_lines2 = []
    actag_list = 'txt,log,md'.split(',')
    if fi_path.split('.')[-1] in actag_list:
        f_lines = mmft.read_txt_py_text(fi_path)
        father_path,f11_name = os.path.split(fi_path)
        return templates.TemplateResponse('file_tree/file_str.html', 
                context={
                    'request': request,
                    'f_lines':f_lines,
                    'father_path':father_path,
                }
            )
    else:
        father_path,f11_name = os.path.split(fi_path)
        print('f11_name=======', f11_name)
        
        f_type = f11_name.split('.')[-1]
        d_show_types = ['.json','.jpg','.png']
        if f_type in d_show_types:
            return FileResponse(fi_path)
        else:
            return FileResponse(fi_path, filename=f11_name)

@router.get('/tree')                 # 参考log_check，展示任意一个文件夹
def tree(request: Request, eco_dir_path:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    # file_dict = {
    #     'log_daily_check':config.f_path['log_daily_check'],
    #     'log_daily_info':config.f_path['log_daily_info'],
    # }
    if eco_dir_path in file_dict:
        real_path = file_dict[eco_dir_path]
    else:
        real_path = eco_dir_path
    file_tree_dict = mmft.file_tree_dict(real_path)
    # print(file_tree_dict)

    father_tree,x = os.path.split(real_path)
    father_tree = father_tree.replace('\\', '/')
    if father_tree in config.f_stop_point_list:  # 再往上就不再递归
        father_tree = real_path

    fp_list = list(file_tree_dict.keys())
    if len(fp_list)==1:
        k0 = fp_list[0]
        v0_list = file_tree_dict[k0]  ####### 只取第一个键
        name_class_dict = {}

        from colour import Color
        red = Color("#F0FFF0")
        color_list = [str(x) for x in  list(red.range_to(Color("#FF83FA"),len(v0_list)))]

        for index,dict_j in enumerate(v0_list):
            final_name_split = dict_j['final_name'].split('_')
            dict_j['bg_color'] = color_list[index]
            if len(final_name_split)==1:
                if 'default' not in name_class_dict:
                    name_class_dict['default'] = []
                name_class_dict['default'].append(dict_j)
                continue
            if final_name_split[0] not in name_class_dict:
                name_class_dict[final_name_split[0]] = []
            name_class_dict[final_name_split[0]].append(dict_j)
        print(name_class_dict)

        return templates.TemplateResponse('file_tree/file_tree_one_dir.html', 
                context={
                    'request': request, 
                    'name_class_dict': name_class_dict,
                    'father_tree':father_tree,
                    'real_path':real_path
                }
            )


        # return 'test'

    # print(father_tree,x, '==========')
    # for k,v in file_tree_dict.items():
    #     print(k, '===>', v)
    return templates.TemplateResponse('file_tree/file_tree.html', 
            context={
                'request': request, 
                'file_tree_dict': file_tree_dict,
                'father_tree':father_tree,
            }
        )

# http://127.0.0.1:5004/file_tree/image_data_tree?eco_dir_path=data_analysis_res&echo2_str=坐标点测试
@router.get('/image_data_tree')   # 数据分析，将一个文件夹的图片和图片的介绍渲染到html
def image_data_tree(request: Request, eco_dir_path:str,echo2_str:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/') 
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    ####### 注意eco_dir_path是一阶目录，echo2_str是二阶目录。当eco_dir_path=''就表示再自己文件夹内，否则就是跳到电脑的其他目录下面
    if eco_dir_path in file_dict:
        real_path = file_dict[eco_dir_path]
    else:
        real_path = ''
    real_dir_path = os.path.join(real_path, echo2_str)  # 最终的dirpath
    dir_file_list = os.listdir(real_dir_path)
    dir_file_list.sort()
    ac_fig_types = 'png,jpg'.split(',')
    myfig_list = []  # 所有的图片
    if config.img_pretext in dir_file_list:
        pretext_lines = mmft.read_txt_py_text(os.path.join(real_dir_path, config.img_pretext))
    else:
        pretext_lines = []

    for i in dir_file_list:
        # print(i)
        if i.split('.')[-1] in ac_fig_types:
            dict_i = {}  # 新建字典
            dict_i['name'] = i.split('.')[0]  # 图片的名称
            dict_i['fig_path'] = os.path.join(real_dir_path, i)
            explain_txt_str = dict_i['name']+'.py'
            explain_excel_str = dict_i['name']+'.xlsx'

            if explain_txt_str in dir_file_list:  # 找到了解释的文件
                txt_f_path = os.path.join(real_dir_path, explain_txt_str)
                f_lines = mmft.read_txt_py_text(txt_f_path)
                dict_i['lines'] = f_lines    #### 解释的多行字符串
            else:  # 找到了文件
                dict_i['lines'] = []

            if explain_excel_str in dir_file_list:  # 找到了解释的文件
                excel_f_path = os.path.join(real_dir_path, explain_excel_str)
                df = pd.read_excel(excel_f_path).fillna('-')
                rows_N = min(15, df.shape[0])
                if df.shape[0]>rows_N:
                    dict_i['see_more'] = '查看更多...'
                else:
                    dict_i['see_more'] = ''
                df = df[:rows_N]
                # if df.shape[0]>df.shape[1] and df.shape[0]<20:
                #     cols_list = df.columns.tolist()
                #     df = df.T
                #     df.insert(0, '序号', cols_list)
                #     df['序号'] = cols_list
                cols_cn_list = df.columns.tolist()
                cols_en_list = ['c_'+str(x) for x in range(len(cols_cn_list))]
                en_cn_dict = dict(zip(cols_cn_list, cols_en_list))
                cn_en_dict = dict(zip(cols_en_list, cols_cn_list))

                df.columns = cols_en_list
                rows_dict_list = []
                for j,r in df.iterrows():
                    dict_ij = dict(zip(cols_en_list, r))
                    rows_dict_list.append(dict_ij)
                dict_i['rows_dict_list'] = rows_dict_list  # excel
                dict_i['cols_cn_list'] = cols_cn_list
                dict_i['download_excel_url'] = '/file_tree/file_str?eco_f_path=%s'%excel_f_path
            else:
                dict_i['rows_dict_list'] = []
                dict_i['cols_cn_list'] = []
                dict_i['download_excel_url'] = ''

            myfig_list.append(dict_i)
        else:
            print('没有接受图片...', i.split('.')[-1])
    # print(myfig_list)
    return templates.TemplateResponse('file_tree/image_data_tree.html', context={'request': request, 'myfig_list': myfig_list,'pretext_lines':pretext_lines})

@router.get('/image_data_file_list')    # 展示目前所有的分析的文件目录
def image_data_file_list(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/') 
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')

    ac_file_dict = {}
    for k,v in config.img_file_dict.items():       # 所有保存分析图片和结果的文件夹,第一类直接出现的文件夹
        ac_file_dict[k] = {}
        sub2_files= os.listdir(v)     # 所有子文件夹

        for sub2 in sub2_files:
            f_path = os.path.join(v, sub2)
            if os.path.isdir(f_path):
                
                dir_files1 = os.listdir(f_path)
                dir_files = []
                for sub3 in dir_files1:
                    sub3_path = os.path.join(f_path, sub3)
                    if os.path.isdir(sub3_path):
                        dir_files.append({'path':'%s/%s'%(sub2, sub3), 'name':sub3})
                        # print(sub2,'+++++++++++', sub3,'+++++++++++', sub3_path)
                dict_i = {}
                dict_i['f_path'] = k
                dict_i['name'] = sub2
                dict_i['files'] = dir_files
                ac_file_dict[k][sub2]= dict_i
                print('==sub2',sub2,  dict_i)
    return templates.TemplateResponse('file_tree/image_data_file_list.html', 
            context={
                'request': request, 
                'ac_file_dict':ac_file_dict,
                # 'ac_file_dict2':ac_file_dict2
            }
        )

# http://127.0.0.1:5004/file_tree/show_one_image?image_path=E:/SS_KUDU/data_analysis_res\坐标点测试\polygon_test_310000.png
@router.get('/show_one_image')   # 数据分析，将一个文件夹的图片和图片的介绍渲染到html
def show_one_image(request: Request, image_path:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/') 
    file_like = open(image_path, mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")

# http://127.0.0.1:5004/file_tree/show_one_image?image_path=E:/SS_KUDU/data_analysis_res\坐标点测试\polygon_test_310000.png
@router.get('/show_one_excel')   # 数据分析，将一个文件夹的图片和图片的介绍渲染到html
def show_one_excel(request: Request, path_str:str,excel_str:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/') 
    if path_str in config.f_path:
        path_str = config.f_path.get(path_str)
    excel_path_str = os.path.join(path_str, excel_str)
    df = pd.read_excel(excel_path_str).fillna('-')

    cols_cn_list = df.columns.tolist()
    cols_en_list = ['c_'+str(i) for i in range(len(cols_cn_list))]
    en_cn_dict = dict(zip(cols_cn_list, cols_en_list))
    cn_en_dict = dict(zip(cols_en_list, cols_cn_list))

    df.columns = cols_en_list
    rows_dict_list = []
    for i,r in df.iterrows():
        dict_i = dict(zip(cols_en_list, r))
        rows_dict_list.append(dict_i)

    from colour import Color
    red = Color("#E066FF")
    color_list = [str(x) for x in  list(red.range_to(Color("limegreen"),len(cols_cn_list)))]
    color_c_dict = {}
    for i,k1 in enumerate(cols_cn_list):
        color_c_dict[k1] = color_list[i]

    return templates.TemplateResponse('file_tree/excel_show.html', 
            context={
                'request': request,
                'excel_path_str':excel_path_str,
                'rows_dict_list':rows_dict_list,
                'cols_cn_list':cols_cn_list,
                'color_c_dict':color_c_dict,
            }
        )

