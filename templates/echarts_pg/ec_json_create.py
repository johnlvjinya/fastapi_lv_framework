
import sys
sys.path.append('../..')
import os
import config
import myutils.dict_json_saver as mdjs


e_list = [
    {
        'c_name':'c1',  # 容器名称
        'd_url':'/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=bar.json',
        'p_type':'bar',  # 图表类型
        'title':'柱状图'

    },
    {
        'c_name':'c2',  # 容器名称
        'd_url':'/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=area_stack.json',
        'p_type':'area_stack',  # 图表类型
        'title':'堆积图'
    },
    {
        'c_name':'c3',  # 容器名称
        'd_url':'/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=pie.json',
        'p_type':'pie',  # 图表类型
        'title':'饼图'
    },
]

json_list = [x.replace('.json', '') for x in os.listdir('ec_json_test')]
js_list = [x.replace('.js', '') for x in os.listdir('ec_templates')]
inter_list = []
for i in json_list:
    if i in js_list:
        inter_list.append(i)

e_list2 = []
for i,inter_i in enumerate(inter_list):
    dict_i =  {
        'c_name':'c_'+str(i),
        'd_url':'/echarts_pg/ecj?d=templates/echarts_pg/ec_json_test&j=%s.json'%inter_i,
        'p_type':inter_i,
        'title':inter_i+'图'
        }
    e_list2.append(dict_i)



if __name__=='__main__':
    mdjs.save_dict_to_json({'e_list':e_list}, file_path='engine_json/test001.json')
    mdjs.save_dict_to_json({'e_list':e_list2}, file_path='engine_json/ec_模板.json')












