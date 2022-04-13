# FastAPI server
import sys
sys.path.append('../../..')
import config
import uvicorn
import hmac
import hashlib
import base64
from typing import Optional
from fastapi import APIRouter, Form,Request
from fastapi.templating import Jinja2Templates

from fastapi import Cookie
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import myutils.login_hash as mlh

templates = Jinja2Templates(directory='templates/')
router = APIRouter()

SECRET_KEY = mlh.SECRET_KEY
PASSWORD_SALT = mlh.PASSWORD_SALT  # '497166f192bc8629d7449cf8ad8ea371331ebc2df53b1ee485cf03db9279c3d9'
users = config.users


def verify_password(username: str, password: str) -> bool:
    '''Checks whether hashes of the password entered and stored in the database match'''
    password_hash = hashlib.sha256( (password + PASSWORD_SALT).encode() ).hexdigest().lower()
    stored_password_hash = users[username]["password"].lower()
    print('password_hash,stored_password_hash', password_hash,stored_password_hash)
    return password_hash == stored_password_hash

# check cookie: yes - welcome, no - clean cookie and go to the home page
@router.get("/")  
def index_page(request: Request,username: Optional[str] = Cookie(default=None)):
    if not username:return templates.TemplateResponse('login_logout/login.html', context={'request': request,})
    valid_username = mlh.get_username_from_signed_string(username)  ######## 得到合法的用户名和密码
    return RedirectResponse('/home_pg')
    
# cookie saved or auto-identification passed - welcome, no - "I don’t know you!"
@router.post("/login")     
def process_login_page(request: Request, username : str = Form(...), password : str = Form(...)):
    user = users.get(username)
    print(user, 'user==========')
    if not user or not verify_password(username, password):return Response("I don’t know you!", media_type="text/html")
    response = templates.TemplateResponse('login_logout/login_success.html', context={'request': request,})
    username_signed = base64.b64encode(username.encode()).decode() + "." + mlh.sign_data(username)
    response.set_cookie(key="username", value=username_signed)
    return response

@router.get("/login")     
def login_get(request: Request,username: Optional[str] = Cookie(default=None)):
    response = templates.TemplateResponse('login_logout/login_success.html', context={'request': request,})
    return response

@router.get("/logout")
def logout(request: Request,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    valid_username = mlh.get_username_from_signed_string(username)
    response = templates.TemplateResponse('login_logout/logout.html', context={'request': request,})
    response.delete_cookie(key="username")
    return response

@router.get("/no_permission")     
def no_permission(request: Request):
    return templates.TemplateResponse('login_logout/no_permission.html', context={'request': request,})

@router.get("/user_info")     
def user_info(request: Request, username: Optional[str] = Cookie(default=None)):
    my_name = mlh.get_username_from_signed_string(username)
    myrole = str(config.users[my_name]['stop_list'])
    return templates.TemplateResponse('login_logout/user_info.html', context=
        {'request': request,
        'my_name':my_name,
        'myrole':myrole,
        })

@router.get("/error_page")     
def error_page(request: Request, error_info: str):
    return templates.TemplateResponse('login_logout/user_info.html', context={'request': request,'error_info':error_info,})