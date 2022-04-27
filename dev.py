
import os
import config
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from templates.home_pg import home_pg
from templates.echarts_pg import echarts_pg
from templates.login_logout import login_logout
from templates.file_tree import file_tree
from templates.file_upload import file_upload
from templates.cs_js_pages import cs_js_pages
from templates.python_study import python_study

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login_logout.router)
app.include_router(home_pg.router, prefix="/home_pg", tags=["home_pg"])
app.include_router(login_logout.router, prefix="/login_logout", tags=["login_logout"])
app.include_router(echarts_pg.router, prefix="/echarts_pg", tags=["echarts_pg"])
app.include_router(file_tree.router, prefix="/file_tree", tags=["file_tree"])
app.include_router(file_upload.router, prefix="/file_upload", tags=["file_upload"])
app.include_router(cs_js_pages.router, prefix="/cs_js_pages", tags=["cs_js_pages"])
app.include_router(python_study.router, prefix="/python_study", tags=["python_study"])


if __name__ == '__main__':
    uvicorn.run(app='dev:app', host="0.0.0.0",port=5000, debug=True,workers=4) # ,debug=True
    