
import sys
sys.path.append('../../..')
import os
import config
import myutils.mylogger as mml
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Form

from typing import Optional
from fastapi import Cookie
from starlette.responses import RedirectResponse


templates = Jinja2Templates(directory='templates/')
router = APIRouter()


@router.get("/11")
def x11(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return {"test": "test_html!"}

@router.get("/")       ############# 默认模板，ec_模板.html等完成后替换
def home(request: Request, username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    return RedirectResponse('/home_pg/echarts_test')

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

