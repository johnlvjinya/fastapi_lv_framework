
import sys
sys.path.append('../..')
import json
import requests
import myutils.dict_json_saver as mdjs

HOST = '127.0.0.1:5004'
# HOST = '101.133.238.216:5004'
# HOST = '101.132.107.216:5004'
########### http://101.132.107.216:5004/bin_recommend/bin_one_ver1


class MyTest():
    def __init__(self):
        pass

    def test_hello(self):
        url = "http://%s/bin_recommend/hello"%HOST
        res = requests.get(url=url)   # , data=json.dumps(data_post)
        json_res = json.loads(res.text)
        print('======================test1', type(json_res), json_res)        

    def test_test(self):
        url = "http://%s/bin_recommend/test"%HOST
        data_post = {
            'temp_type':'-20',              # 温区
            'goods_str':'1000==>14*6*5;',   # 货物字符串
            'can_reverse':0                 # 1可以倒放
        }
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "data":json.dumps(data_post)
        }
        res = requests.post(url=url, headers=headers)   # , data=json.dumps(data_post)
        json_res = json.loads(res.text)
        print('======================test2', type(json_res), json_res)

    def test_post_header(self):
        url = "http://%s/bin_recommend/bin_one_ver1_header"%HOST
        data_post = {
            ####### 判断是否是M+
            'start_region_id':140100,       # start, end region id用来找M+
            'end_region_id':140300,
            'omc_time':'2021-08-23',        # 开始结束日期找M+
            'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
            'specail_type_str':'',          # 用来判断，可行箱子肯定性条件，空就没有要求
            ####### 温度可行箱子判断
            'omc_tem_id':'32',              # 温度id
            ####### 货物和订单属性
            'can_reverse':1,                # 1可以倒放, 空则0
            'goods_str':'3==>13*30*10;100==>14*6*5;10==>14*6*5;2==>9*9*4;10==>120*7*2;10==>120*71*2;',    # 货物字符串,长度单位是里面（参考数据库）
        }

        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
            "data":json.dumps(data_post)
        }
        res = requests.post(url=url, headers=headers)   # , data=json.dumps(data_post)
        json_res = json.loads(res.text)
        print('======================test3', type(json_res), json_res)

    def test_post_body(self):
        url = "http://%s/bin_recommend/bin_one_ver1_body"%HOST
        data_post = {
            ####### 判断是否是M+
            'start_region_id':140100,      # start, end region id用来找M+
            'end_region_id':140300,
            'omc_time':'2021-08-23',        # 开始结束日期找M+
            'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
            'specail_type_str':'',         # 用来判断，可行箱子肯定性条件，空就没有要求
            ####### 温度可行箱子判断
            'omc_tem_id':'32',              # 温度id
            ####### 货物和订单属性
            'can_reverse':1,                # 1可以倒放, 空则0
            'goods_str':'3==>13*30*10;100==>14*6*5;10==>14*6*5;2==>9*9*4;10==>120*7*2;10==>120*71*2;',    # 货物字符串,长度单位是里面（参考数据库）
        }
        data_post = {

            ####### 判断是否是M+
            'start_region_id':140100,      # start, end region id用来找M+
            'end_region_id':140300,
            'omc_time':'2021-08-23',        # 开始结束日期找M+

            'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
            'specail_type_str':'',         # 用来判断，可行箱子肯定性条件，空就没有要求

            ####### 温度可行箱子判断
            'omc_tem_id':'25',              # 温度id

            ####### 货物和订单属性
            'can_reverse':0,                # 1可以倒放, 空则0
            'goods_str':'1==>15.0*15.0*15.0',    # 货物字符串,长度单位是里面（参考数据库）
        }
        mdjs.save_dict_to_json(data_post, file_path='test.json')
        res = requests.post(url=url, json=data_post)   # , data=json.dumps(data_post)
        print('======================test333', type(res), res.__dict__)

    def test_get(self):
        url = "http://%s/bin_recommend/bin_one_ver1??start_region_id=140100&end_region_id=140300&omc_time=2021-08-23&route_type=1&omc_tem_id=32&can_reverse=1&goods_str=3==>13*30*10;100==>14*6*5;10==>14*6*5;2==>9*9*4;10==>120*7*2;10==>120*71*2"%HOST
        res = requests.get(url=url)   # , data=json.dumps(data_post)
        json_res = json.loads(res.text)
        print('=====================test4', type(json_res), json_res)


        url = "http://%s/bin_recommend/bin_one_ver1??start_region_id=140100&end_region_id=140300&specail_type_str=&omc_time=2021-08-23&route_type=1&omc_tem_id=32&can_reverse=1&goods_str=3==>13*30*10;100==>14*6*5;10==>14*6*5;2==>9*9*4;10==>120*7*2;10==>120*71*2"%HOST
        res = requests.get(url=url)   # , data=json.dumps(data_post)
        json_res = json.loads(res.text)
        print('=====================test5', type(json_res), json_res)

    def run(self):
        # self.test_hello()
        # self.test_test()
        # self.test_post_header()
        self.test_post_body()
        # self.test_get()
        pass

if __name__=='__main__':
    MyTest().run()