import sys
sys.path.append('../..')

import os
import json
import config
import pandas as pd
from fastapi import APIRouter, Request, Body
from fastapi.responses import JSONResponse
import algorithms.algori_bin.s41_one_container_one_item as as41coi
import algorithms.algori_bin.s42_algori_bin_ver3 as as42ver
router = APIRouter()


def get_q_dict(q_str):
    # q_str = '?start_region_id=140100&end_region_id=140300&omc_time=2021-08-23&route_type=1&omc_tem_id=32&can_reverse=1&goods_str=3==%3E13*30*10;100==%3E14*6*5;10==%3E14*6*5;2==%3E9*9*4;10==%3E120*7*2;10==%3E120*71*2'
    q_str = str(q_str)
    q_str = q_str.lstrip('?')
    q_list = q_str.split('&')

    l1 = []
    l2 = []
    for q in q_list:
        q2 = q.replace('==%3E', '-->')
        # print(q2)
        l1.append(q2.split('=')[0])
        l2.append(q2.split('=')[1])
    l2 = [i.replace('-->', '==>') for i in l2]
    q_dict = dict(zip(l1, l2))
    print(q_dict)
    int_type_k = 'start_region_id,end_region_id,route_type,can_reverse'.split(',')
    for k in int_type_k:
        if k in q_dict:
            q_dict[k] = int(q_dict[k])
    return q_dict 


######### http://127.0.0.1:5004/route_recommend/hello
@router.get("/hello")
def hello():
    return {"Hello": "World"}


############  http://127.0.0.1:5004/bin_recommend/test
@router.post("/test")
def test(request: Request):   # 计算两个数的和
    try:
        response = {'code': 200, 'message': '成功'}
        data = json.loads(request.headers.get("data"))
        print(data)
        response['res_list'] = 'test'

    except Exception as e:
        response = {'code': 201, 'message': '失败', 'error':str(e)}
    return response

############  http://127.0.0.1:5004/bin_recommend/bin_one_ver1_header
@router.post("/bin_one_ver1_header")
def bin_one_ver1_header(request: Request):
    # response = {'code': 200, 'message': '成功'}
    # goods_dict = json.loads(request.headers.get("data"))
    # print(goods_dict)
    # A = as41coi.OneContainerOneItemSolution(goods_dict)
    # res = A.multi_container_multi_item()
    # response['request.body'] =  request.body
    # response['res_dict'] = res
    try:
        response = {'code': 200, 'message': '成功'}
        goods_dict = json.loads(request.headers.get("data"))
        print(goods_dict)
        A = as41coi.OneContainerOneItemSolution(goods_dict)
        res = A.multi_container_multi_item()
        response['request.body'] =  request.body
        response['res_dict'] = res
    except Exception as e:
        print('error.......', e)
        response = {'code': 201, 'message': '失败', 'error':str(e)}
    return response



############  http://127.0.0.1:5004/bin_recommend/bin_one_ver1_header
@router.post("/bin_one_ver1_body")
def bin_one_ver1_body(
    request: Request,

    ######## 增加特殊规则条件
    thermometer_num: int = Body(1, title='温度计数量，默认为1', embed=True),         # 温度计数量，默认为1
    cu_id: str = Body('-1', title='客户编号，没有就填"-1"', embed=True),             # 客户编号，没有就填"-1",或者不要这个字段
    cp_id: str = Body('-1', title='项目编号，没有就填"-1"', embed=True),             # 项目编号,没有就填"-1",或者不要这个字段
    goods_name: str = Body('-1', title='货物名称，没有就填"-1"', embed=True),        # 货物名称

    ####### 判断是否是M+
    start_region_id: int = Body(140100, title='start_region_id,找M+', embed=True),   # start, end region id用来找M+
    end_region_id: int = Body(140300, title='start_region_id,找M+', embed=True),     # start, end region id用来找M+
    omc_time: str = Body('2021-08-23', title='开始结束日期,找M+', embed=True),         # start, end region id用来找M+
    route_type:int = Body(-1, title='路由方式,没有的话就是-1', embed=True),               
    specail_type_str: str = Body('', title='可行箱子类别,空就没有要求', embed=True),  # 用来判断，可行箱子肯定性条件，空就没有要求
    ####### 温度可行箱子判断
    omc_tem_id:str = Body('32', title='温度类别', embed=True),               # 温度id
    ####### 货物和订单属性
    can_reverse:int = Body(0, title='0不可以倒放,1可以倒放, 空则0', embed=True),                # 1可以倒放, 空则0
    goods_str:str = Body('2==>11*11*11;5==>10*10*10;', title='货物字符串', embed=True),   # 货物字符串,长度单位是里面（参考数据库）
    ):

    goods_dict = {
        ######## 增加特殊规则条件
        'thermometer_num':thermometer_num,      # 温度计数量，默认为1
        'cu_id':cu_id,                          # 客户编号，没有就填"-1",或者不要这个字段
        'cp_id':cp_id,                          # 项目编号,没有就填"-1",或者不要这个字段
        'goods_name':goods_name,                # 货物名称
        
        ####### 判断是否是M+
        'start_region_id':start_region_id,      # start, end region id用来找M+
        'end_region_id':end_region_id,
        'omc_time':omc_time,                    # 开始结束日期找M+
        'route_type':route_type,                # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
        'specail_type_str':specail_type_str,    # 用来判断，可行箱子肯定性条件，空就没有要求
        
        ####### 温度可行箱子判断
        'omc_tem_id':omc_tem_id,                # 温度id
        ####### 货物和订单属性
        'can_reverse':can_reverse,                # 1可以倒放, 空则0
        'goods_str':goods_str,    # 货物字符串,长度单位是里面（参考数据库）
    }    
    try:
        response = {'code': 200, 'message': '成功'}
        # goods_dict = json.loads(request.headers.get("data"))
        # print(goods_dict)
        # A = as41coi.OneContainerOneItemSolution(goods_dict)
        # res = A.multi_container_multi_item()
        A = as42ver.OneContainerOneItemSolution(goods_dict)
        res = A.run()
        response['res_dict'] = res
    except Exception as e:
        # print('error.......', e)
        response = {'code': 201, 'message': '失败', 'error':str(e)}    

    return response
