import sys
sys.path.append('..')

import os
import json
import config
from myutils.func_decorated import log_func_time
from algori_bin.s32_one_container_one_item import one_goods_one_box_package

def select_best_container(goods_dict, temp_container_dict):
    res_list = select_able_containers(goods_dict, temp_container_dict)
    cost = 1000000000
    best_dict = {}
    able_container_list = []
    appear_list = []
    for k in res_list:

        if k['箱子'] not in appear_list:
            able_container_list.append({k['箱子']:k['每个箱子']})
            appear_list.append(k['箱子'])
        if k['成本']<cost:
            cost = k['成本']
            best_dict = k
    best_dict['货物'] = goods_dict['goods_str']
    best_dict['可选箱型'] = able_container_list

    print(best_dict)
    return best_dict

# @log_func_time
def select_able_containers(goods_dict={}, temp_container_dict={}):
    '''
    goods_dict={
        'temp_type':'-20',              # 温区
        'goods_str':'107==>12*8*2;'     # 货物字符串
        'can_reverse':1                 # 是否可以倒放
    }
    '''
    temp_type = goods_dict.get('temp_type')
    goods_str = goods_dict.get('goods_str')
    can_reverse = goods_dict.get('can_reverse')

    c_container_dict = temp_container_dict.get(temp_type) # 当前的温区的所有箱子的字典信息

    if goods_dict.get('must_accept_bins'):  # 如果存在箱型限制约束
        pass
    else:
        container_type_path = os.path.join(config.ROOT_PATH, 'data/bin/container_special_type.json')
        goods_dict['must_accept_bins'] = json.load(open(container_type_path, "rb")).get('常规') # 参考json中的数据结构        

    new_dict = {}
    for bin_i in goods_dict.get('must_accept_bins'):
        if bin_i in c_container_dict:
            new_dict[bin_i] = c_container_dict[bin_i]
    c_container_dict = new_dict   # 只保留接受的箱子

    one_order_str = goods_str.rstrip(';')
    goods_qty = int(one_order_str.split('==>')[0])
    goods_shape = one_order_str.split('==>')[1]
    [goods_l,goods_w,goods_h] = [10*int(i) for i in goods_shape.split('*')]  # 将厘米变成毫米
    # print('[goods_qty,goods_l,goods_w,goods_h]', [goods_qty,goods_l,goods_w,goods_h])
    goods_vol_L = round(goods_qty*goods_l*goods_w*goods_h/1000000,2)
    # print(goods_vol_L)
    ######## 查看哪些箱子能放得下
    # print('==================================备注，如果需要再优化，最后一个箱子可以换成一个单位成本最小，且能放下剩余数量的箱子，res_dict再循环一次就OK')
    res_list = []
    for k,v in c_container_dict.items():
        # print('最大容积_L, goods_vol_L', v['最大容积_L'], goods_vol_L)
            # print('\n考虑这个箱子==============',k)
            # v.pop('温度使用范围_C') 
            # print('可行的箱子：', k, '===>', v)
        c_l = v.get('长')
        c_w = v.get('宽')
        c_h = v.get('有效高')


        c_max_v = v.get('最大容积_L')
        list1,list2,list3 = one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)

        # print(k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)
        if list1[0]!=0:
            dict_x = {'箱子':k, '放法':'长长', '每个箱子':list1[0],'每层':list3[0],
                '箱子数(n+1)':goods_qty//list1[0]+1,
                'last箱':goods_qty%list1[0],
                '余量':list1[0]-goods_qty%list1[0],
                '箱子最大容积_L':v.get('最大容积_L'),
                'lwh余量':list2[0],
                '成本':round(v['成本']*(goods_qty//list1[0]+1),3),'单位成本':round(v['成本']/list1[0], 3)
                }
            res_list.append(dict_x)

        if list1[1]!=0:                
            dict_x = {'箱子':k, '放法':'长宽', '每个箱子':list1[1],'每层':list3[1], 
                '箱子数(n+1)':goods_qty//list1[1]+1,
                'last箱':goods_qty%list1[1],
                '余量':list1[1]-goods_qty%list1[1],
                '箱子最大容积_L':v.get('最大容积_L'),
                'lwh余量':list2[1],
                '成本':round(v['成本']*(goods_qty//list1[1]+1),3),'单位成本':round(v['成本']/list1[1], 3)
                }
            res_list.append(dict_x)

        if can_reverse==1:
            ########### 长高倒放，不考虑更复杂旋转
            a,b,c = goods_l,goods_w,goods_h
            goods_l = max(c, b)
            goods_w = min(c, b)
            goods_h = a
            list1,list2,list3 = one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
            # print('长高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2) 
            if list1[0]!=0:
                dict_x = {'箱子':k, '放法':'长高倒放-长长', '每个箱子':list1[0],'每层':list3[0], 
                    '箱子数(n+1)':goods_qty//list1[0]+1,
                    'last箱':goods_qty%list1[0],
                    '余量':list1[0]-goods_qty%list1[0],
                    '箱子最大容积_L':v.get('最大容积_L'),
                    '箱子lwh余量':list2[0],
                    '成本':round(v['成本']*(goods_qty//list1[0]+1),3),'单位成本':round(v['成本']/list1[0], 3)
                    }
                res_list.append(dict_x)
            if list1[1]!=0:
                dict_x = {'箱子':k, '放法':'长高倒放-长宽', '每个箱子':list1[1],'每层':list3[1], 
                    '箱子数(n+1)':goods_qty//list1[1]+1,
                    'last箱':goods_qty%list1[1],
                    '余量':list1[1]-goods_qty%list1[1],
                    '箱子最大容积_L':v.get('最大容积_L'),
                    'lwh余量':list2[1],
                    '成本':round(v['成本']*(goods_qty//list1[1]+1),3),
                    '单位成本':round(v['成本']/list1[1], 3)
                    }
                res_list.append(dict_x)

            ########### 宽高倒放，不考虑更复杂旋转
            a,b,c = goods_l,goods_w,goods_h
            goods_l = max(c, a)
            goods_w = min(c, a)
            goods_h = b
            list1,list2,list3 = one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
            # print('宽高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)    
            if list1[0]!=0:
                dict_x = {'箱子':k, '放法':'宽高倒放-长长', '每个箱子':list1[0],'每层':list3[0], 
                    '箱子数(n+1)':goods_qty//list1[0]+1,
                    'last箱':goods_qty%list1[0],
                    '余量':list1[0]-goods_qty%list1[0],
                    '箱子最大容积_L':v.get('最大容积_L'),
                    'lwh余量':list2[0],
                    '成本':round(v['成本']*(goods_qty//list1[0]+1),3),'单位成本':round(v['成本']/list1[0], 3)
                    }
                res_list.append(dict_x)
            if list1[1]!=0:
                dict_x = {'箱子':k, '放法':'宽高倒放-长宽', '每个箱子':list1[1],'每层':list3[1], 
                    '箱子数(n+1)':goods_qty//list1[1]+1,
                    'last箱':goods_qty%list1[1],
                    '余量':list1[1]-goods_qty%list1[1],
                    '箱子最大容积_L':v.get('最大容积_L'),
                    'lwh余量':list2[1],
                    '成本':round(v['成本']*(goods_qty//list1[1]+1),3),'单位成本':round(v['成本']/list1[1], 3)
                    }
                res_list.append(dict_x)

    # for k in res_list:
    #     print(k)
    if len(res_list)>0:
        # print('find solution, 货物数量和尺寸mm', goods_qty, [goods_l,goods_w,goods_h])
        return res_list
    else:
        print('no solution, 货物数量和货物尺寸mm', goods_qty, [goods_l,goods_w,goods_h])
        # print('=======>goods_dict\n', goods_dict,'=======>temp_container_dict\n',  temp_container_dict)
        return []



if __name__=='__main__':
    goods_dict={
        'temp_type':'B20',              # 温区
        'goods_str':'165==>6*7*11;',     # 货物字符串
        'can_reverse':1,                 # 1可以倒放
        'must_accept_bins':['PBX-EP46__EP46泡沫箱', 'PBX-EP133__EP133泡沫箱']      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    }
    goods_dict={
        'temp_type':'B20',              # 温区
        'goods_str':'107==>19*9*4;',     # 货物字符串
        'can_reverse':0,                 # 1可以倒放
        'must_accept_bins':['PBX-EP78__EP78泡沫箱']
    }

    f_path = os.path.join(config.ROOT_PATH, 'data/bin/container_info.json')
    temp_container_dict = json.load(open(f_path, "rb")) # 参考json中的数据结构
    # select_able_containers(goods_dict,temp_container_dict)
    res = select_best_container(goods_dict,temp_container_dict)
    print(res)
