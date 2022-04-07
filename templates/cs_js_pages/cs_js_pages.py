
import sys
sys.path.append('../../..')
import os
import config
import myutils.mylogger as mml
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

# 127.0.0.1:5004/cs_js_pages/x11
@router.get("/x11")
def x11(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return {"test": "test_html_cs_js_pages!"}
    
@router.get("/test_eco")
def test_eco(request: Request, test1:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    eco = test1
    return templates.TemplateResponse('cs_js_pages/test_eco.html', context={'request': request,'eco':eco})

@router.get("/static_page")
def static_page(request: Request, page_name:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    # page_name = 'button_hover.html'
    return templates.TemplateResponse('cs_js_pages/static_pages/%s'%page_name, context={'request': request})

@router.get("/static_page_list")
def static_page_list(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    page_list = os.listdir('templates/cs_js_pages/static_pages')
    page_dict_list = []
    for p in page_list:
        page_dict_list.append({"name":p.rstrip('.html'),"html_name":p})
    return templates.TemplateResponse('cs_js_pages/static_page_list.html', context={
        'request': request, 
        "page_dict_list":page_dict_list
        })

# 127.0.0.1:5004/cs_js_pages/icon_list?first_char=a
@router.get("/icon_list")
def icon_list(request: Request, first_char:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    icon_list = os.listdir('static/icons')
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    icon_char_dict = {"others":[]}
    for c in chars:
        icon_char_dict[c] = []

    for icon_i in icon_list:
        c = icon_i[0]
        if c in chars:
           icon_char_dict[c].append(icon_i)
        else:
            icon_char_dict['others'].append(icon_i)

    # 展示的图标
    show_chars_list = icon_char_dict.get(first_char)
    chars_type_list = chars +['others']
    # print(show_chars_list)

    return templates.TemplateResponse('cs_js_pages/icon_list.html', context={
        'request': request,
        'show_chars_list':show_chars_list,
        'chars_type_list':chars_type_list
        }, 
        )

# 127.0.0.1:5004/cs_js_pages/test_form
@router.get("/test_form_one")
def test_form_one(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    return templates.TemplateResponse('cs_js_pages/test_form_one.html', context={
        'request': request,
        }, 
        )

@router.get("/test_form_loop")
def test_form_one(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    form_id_list = [str(i) for i in range(5)]
    return templates.TemplateResponse('cs_js_pages/test_form_loop.html', context={
        'request': request,
        'form_id_list':form_id_list,
        }, 
        )

# cs_js_pages/test_form_deal
@router.get("/test_form_deal")
def test_form_deal(request: Request, data:str, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')
    
    msg = {
    'data':json.loads(data),
    }
    print(msg)
    headers = {}
    return JSONResponse(content=msg, headers=headers)
