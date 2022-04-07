
import os
import config
import uvicorn
import myutils.mylogger as mml
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from algorithms_api.bin_recommend import bin_recommend  # 装箱

from templates.home_pg import home_pg
from templates.echarts_pg import echarts_pg
from templates.file_tree import file_tree
from templates.login_logout import login_logout
from templates.operator_invoke import operator_invoke
from templates.file_upload import file_upload
from templates.mix_special_html import mix_special_html

from templates.cs_js_pages import cs_js_pages

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login_logout.router)
app.include_router(home_pg.router, prefix="/home_pg", tags=["home_pg"])
app.include_router(echarts_pg.router, prefix="/echarts_pg", tags=["echarts_pg"])
app.include_router(file_tree.router, prefix="/file_tree", tags=["log_html"])
app.include_router(operator_invoke.router, prefix="/operator_invoke", tags=["operator_invoke"])
app.include_router(file_upload.router, prefix="/file_upload", tags=["file_upload"])
app.include_router(mix_special_html.router, prefix="/mix_special_html", tags=["mix_special_html"])
app.include_router(cs_js_pages.router, prefix="/cs_js_pages", tags=["cs_js_pages"])

app.include_router(bin_recommend.router, prefix="/bin_recommend", tags=["bin_recommend"])





if __name__ == '__main__':
    uvicorn.run(app='dev:app', host="0.0.0.0",port=5004, debug=True,workers=4) # ,debug=True
    