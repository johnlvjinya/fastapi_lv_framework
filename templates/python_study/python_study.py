

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
@router.get("/hello_python")
def hello_python(request: Request,username: Optional[str] = Cookie(default=None)):
    if not username:return RedirectResponse('/')
    if str(__name__).split('.')[-1] in config.users[config.get_username_from_signed_string(username)]['stop_list']:return RedirectResponse('/no_permission')

    return {'test':'hello python'}

