
import sys
sys.path.append('../../..')
import os
import json
import config
import myutils.login_hash as mlh
import myutils.myfile_tree as mmft
from fastapi import APIRouter, Request, Form,File, UploadFile
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from typing import List
from typing import Optional
from fastapi import Cookie
from starlette.responses import RedirectResponse

templates = Jinja2Templates(directory='templates/')
router = APIRouter()

# http://127.0.0.1:5004/file_upload/file_upload_dir_list
@router.get('/file_upload_dir_list')                 # 接受上传的所有文件目录
def file_upload_dir_list(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    res_dict = {}
    for k,v in config.ac_dir_dict.items():
        dict_k = mmft.file_dir_dict(v)
        new_dict = {'f_dir':v}
        for k1,v1 in dict_k.items():
            if k1!='' and k1 not in config.f_stop_point_list:
                new_dict[k1]=v1
        res_dict[k] = new_dict
        print(k, v, '=======>',res_dict[k])
    return templates.TemplateResponse('file_upload/file_upload_dir_list.html', context={'request': request, 'res_dict': res_dict,})

# http://127.0.0.1:5004/file_upload/file_upload_dir_one_dir?dir_name=E:/SS_KUDU/data_json
@router.get('/file_upload_dir_one_dir')                 # 接受上传的所有文件目录
def file_upload_dir_one_dir(request: Request,dir_name:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    file_list1 = os.listdir(dir_name)
    file_list = []
    father_dir = os.path.split(dir_name)[0]

    # file_list = [{"name":x, "eco_f_path":os.path.join(dir_name, x)} for x in file_list1] 
    if dir_name not in config.f_stop_point_list:
        for index,i in enumerate(file_list1):

            dict_i = {}
            dict_i['name'] = i
            dict_i['index'] = str(index)
            dict_i['eco_f_path'] ='%s/%s'%(dir_name, i) #os.path.join(dir_name, i).replace('\\', '/')

            if os.path.isdir(dict_i['eco_f_path']):
                dict_i['type'] = 'dir'
            else:
                dict_i['type'] = 'file'
            file_list.append(dict_i)  

        return templates.TemplateResponse('file_upload/file_upload_dir_one_dir.html', 
            context={'request': request, 'file_list': file_list,'dir_name':dir_name, 'father_dir':father_dir})
    else:
        return RedirectResponse('/file_upload/file_upload_dir_list')


@router.post('/file')                 # 接受上传的所有文件目录
async def file(request: Request, dir_name:str, username: Optional[str] = Cookie(default=None), file: UploadFile = File(...)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    # rq_dict = {}
    # for x in request.__dict__['_headers'].__dict__['_list']:
    #     try:
    #         k = str(x[0], encoding='utf-8')
    #         v = str(x[1], encoding='utf-8')
    #         rq_dict[k] = v
    #     except:
    #         pass
    # for k,v in rq_dict.items():
    #     print(k,'=======>',v)
    # redirect_str = rq_dict['referer'].replace(rq_dict['origin'], '')
    # print(redirect_str)

    try:
        res = await file.read()
        with open(os.path.join(dir_name, file.filename), "wb") as f:
            f.write(res)
        return {"message": '成功',  'filename': file.filename}
    except Exception as e:
        return {"message": str(e),  'filename': file.filename}

    # return RedirectResponse('/file_upload/file_upload_dir_one_dir?dir_name=%s'%dir_name)

@router.post('/files')                 # 接受上传的所有文件目录
async def files(request: Request, dir_name:str, username: Optional[str] = Cookie(default=None), files: List[UploadFile] = File(...)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    try:
        for file in files:
            res = await file.read()
            with open(os.path.join(dir_name, file.filename), "wb") as f:
                f.write(res)
        return {"message": 'success'}
    except Exception as e:
        return {"message": str(e)}

@router.post('/dir_create')                 # 接受上传的所有文件目录
def dir_create(request: Request, dir_name:str, username: Optional[str] = Cookie(default=None), file_dir_name: str = Form(...)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    try:
        new_path = os.path.join(dir_name, file_dir_name)
        if os.path.exists(new_path) is False:os.makedirs(new_path)        
        return {"message": 'success'}
    except Exception as e:
        return {"message": str(e)}

# http://127.0.0.1:5004/
@router.post('/file_delete')                 # 检查数据不一致的问题
def file_delete(request: Request, eco_f_path:str, dir_name:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[mlh.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')

    t_path = os.path.join(dir_name, eco_f_path)
    print('eco_f_path.......', eco_f_path, 't_path...', t_path)

    if os.path.isdir(eco_f_path):
        import shutil
        shutil.rmtree(eco_f_path)
    else:
        os.remove(eco_f_path)
    return {"message": 'success'}
