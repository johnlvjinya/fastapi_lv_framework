
import sys
sys.path.append('..')

import os
import json
import config
from myutils.func_decorated import log_func_time


def select_best_container(goods_dict, temp_container_dict):
    res_list = select_able_containers(goods_dict, temp_container_dict)
    cost = 1000000000
    best_dict = {}
    for k in res_list:
        # print(k) 
        if k['成本']<cost:
            cost = k['成本']
            best_dict = k
    # print(best_dict)
    return best_dict


def get_goods_c_container_dict(goods_dict):
    f_path = os.path.join(config.ROOT_PATH, 'data/bin/config_temperature_vol.json')
    config_temperature_vol = json.load(open(f_path, "rb")) # 参考json中的数据结构 

    f_path = os.path.join(config.ROOT_PATH, 'data/bin/container_info.json')
    container_info = json.load(open(f_path, "rb")) # 参考json中的数据结构     

    f_path = os.path.join(config.ROOT_PATH, 'data/bin/container_route_constraint.json')
    container_route_constraint = json.load(open(f_path, "rb")) # 参考json中的数据结构     

    f_path = os.path.join(config.ROOT_PATH, 'data/bin/container_special_type.json')
    container_special_type = json.load(open(f_path, "rb")) # 参考json中的数据结构     

    f_path = os.path.join(config.ROOT_PATH, 'data/bin/m_plus_case_list.json')
    m_plus_case_list = json.load(open(f_path, "rb")) # 参考json中的数据结构 


    ########## 首先判断是不是M+类型的箱子
    '''
    goods_dict = {

        ####### 判断是否是M+
        'start_region_id':1234566,      # start, end region id用来找M+
        'end_region_id':1234567,
        'omc_time':'2022-12-25',        # 开始结束日期找M+

        ####### 温度可行箱子判断
        'omc_tem_id':'62',              # 温度id

        ####### 货物和订单属性
        'can_reverse':1,                # 1可以倒放, 空则0
        'goods_str':'107==>12*8*2;',    # 货物字符串,长度单位是里面（参考数据库）
        'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
        'specail_type_str':'B',         # 用来判断，可行箱子肯定性条件，空就没有要求

        #'must_accept_bins':['PBX-EP46__EP46泡沫箱', 'PBX-EP133__EP133泡沫箱']      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    }
    '''








def select_able_containers(goods_dict, temp_container_dict):
    '''
    goods_dict = {

        ####### 判断是否是M+
        'start_region_id':1234566,      # start, end region id用来找M+
        'end_region_id':1234567,
        'omc_time':'2022-12-25',        # 开始结束日期找M+

        ####### 温度可行箱子判断
        'omc_tem_id':'62',              # 温度id

        ####### 货物和订单属性
        'can_reverse':1,                # 1可以倒放, 空则0
        'goods_str':'107==>12*8*2;',    # 货物字符串,长度单位是里面（参考数据库）
        'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
        'specail_type_str':'B',         # 用来判断，可行箱子肯定性条件，空就没有要求

        #'must_accept_bins':['PBX-EP46__EP46泡沫箱', 'PBX-EP133__EP133泡沫箱']      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    }
    '''
    # print(goods_dict)
    temp_type = goods_dict.get('temp_type')
    goods_str = goods_dict.get('goods_str')
    can_reverse = goods_dict.get('can_reverse')

    ########## 计算货物的信息
    one_order_str = goods_str.rstrip(';')
    goods_qty = int(one_order_str.split('==>')[0])
    goods_shape = one_order_str.split('==>')[1]
    [goods_l,goods_w,goods_h] = [10*int(i) for i in goods_shape.split('*')]  # 将厘米变成毫米
    # print('[goods_qty,goods_l,goods_w,goods_h]', [goods_qty,goods_l,goods_w,goods_h])
    goods_vol_L = round(goods_qty*goods_l*goods_w*goods_h/1000000,2)


    # print(goods_vol_L)
    ######## 查看哪些箱子能放得下
    res_list = []
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


    '''
    c_container_dict字典中的基本元素如下：
    "EP15": {
      "保温箱内径_mm": "265*265*270",
      "长": 265,
      "宽": 265,
      "高": 270,
      "有效高": 120,
      "温区类别_C": "-20,-60",
      "成本": 4.85,
      "最大容积_L": 9.48
    },

    '''



    # print(c_container_dict)

    for k,v in c_container_dict.items():
        # print('最大容积_L, goods_vol_L', v['最大容积_L'], goods_vol_L)
        if v['最大容积_L']>goods_vol_L:
            # print('\n考虑这个箱子==============',k)
            # v.pop('温度使用范围_C') 
            # print('可行的箱子：', k, '===>', v)
            c_l = v.get('长')
            c_w = v.get('宽')
            c_h = v.get('有效高')
            c_max_v = v.get('最大容积_L')
            list1,list2,list3 = one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
            # print(k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)
            if list1[0]>=goods_qty:
                dict_x = {'箱子':k, '放法':'长长','每层':list3[0], '多余空间数':list1[0]-goods_qty, '箱子lwh余量':list2[0],'成本':v['成本'],'单位成本':round(v['成本']/list1[0], 3),'货物尺寸':[goods_l,goods_w,goods_h]}
                res_list.append(dict_x)
            if list1[1]>=goods_qty:
                dict_x = {'箱子':k, '放法':'长宽','每层':list3[1], '多余空间数':list1[1]-goods_qty, '箱子lwh余量':list2[1],'成本':v['成本'],'单位成本':round(v['成本']/list1[1], 3),'货物尺寸':[goods_l,goods_w,goods_h]}
                res_list.append(dict_x)

            if can_reverse==1:
                ########### 长高倒放，不考虑更复杂旋转
                a,b,c = goods_l,goods_w,goods_h
                goods_l = max(c, b)
                goods_w = min(c, b)
                goods_h = a
                list1,list2,list3 = one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                # print('长高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2) 
                if list1[0]>=goods_qty:
                    dict_x = {'箱子':k, '放法':'长高倒放-长长','每层':list3[0], '多余空间数':list1[0]-goods_qty, '箱子lwh余量':list2[0],'成本':v['成本'],'单位成本':round(v['成本']/list1[0], 3),'货物尺寸':[goods_l,goods_w,goods_h]}
                    res_list.append(dict_x)
                if list1[1]>=goods_qty:
                    dict_x = {'箱子':k, '放法':'长高倒放-长宽','每层':list3[1], '多余空间数':list1[1]-goods_qty, '箱子lwh余量':list2[1],'成本':v['成本'],'单位成本':round(v['成本']/list1[1], 3),'货物尺寸':[goods_l,goods_w,goods_h]}
                    res_list.append(dict_x)

                ########### 宽高倒放，不考虑更复杂旋转
                a,b,c = goods_l,goods_w,goods_h
                goods_l = max(c, a)
                goods_w = min(c, a)
                goods_h = b
                list1,list2,list3 = one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                # print('长高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)    
                if list1[0]>=goods_qty:
                    dict_x = {'箱子':k, '放法':'宽高倒放-长长','每层':list3[0], '多余空间数':list1[0]-goods_qty, '箱子lwh余量':list2[0],'成本':v['成本'],'单位成本':round(v['成本']/list1[0], 3),'货物尺寸':[goods_l,goods_w,goods_h]}
                    res_list.append(dict_x)
                if list1[1]>=goods_qty:
                    dict_x = {'箱子':k, '放法':'宽高倒放-长宽','每层':list3[1], '多余空间数':list1[1]-goods_qty, '箱子lwh余量':list2[1],'成本':v['成本'],'单位成本':round(v['成本']/list1[1], 3),'货物尺寸':[goods_l,goods_w,goods_h]}
                    res_list.append(dict_x)

    # for k in res_list:
    #     print(k)
    if len(res_list)>0:
        pass
        # print('find one container one item solution')
    else:
        print('no solution')
    return res_list

###### 将一种物品放入一个container
def one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h):
    '''
    cl：箱子长
    cw：箱子宽
    ch：箱子有效高
    c_max_v: 箱子实际最大容量
    goods_qty：货物数量
    goods_l：货物长
    goods_w：货物宽
    goods_h：货物高
    '''
    EXPAND_RATIO = 1
    goods_l,goods_w,goods_h = goods_l*EXPAND_RATIO,goods_w*EXPAND_RATIO,goods_h*EXPAND_RATIO
    max_layer_n = c_h//goods_h   # 从高度角度出发的最大层数

    ll_n = c_l//goods_l       # 长长数，货物的长对应container的长，最多放的个数
    ww_n = c_w//goods_w       # 宽宽数
    wl_n = c_w//goods_l       # 宽长数
    lw_n = c_l//goods_w       # 长宽数

    ll_left = c_l%goods_l     # 长长结余量,长长放法长度还剩余的量
    ww_left = c_w%goods_w     # 宽宽结余量
    lw_left = c_l%goods_w     # 长宽结余量
    wl_left = c_w%goods_l     # 宽长结余量

    ######## 长长放法
    ll_left_wn = ll_left//goods_w   # 长长放法长度剩余量，剩余的container长度可以放几个货宽
    l_final_left = ll_left%goods_w  # 长度最终的剩余量

    ####### 宽长放法
    wl_left_wn = wl_left//goods_w  # 宽长结余量宽数
    w_final_left = lw_left%goods_w  # 宽度最终的剩余量

    ## 长长放法
    ll_layer_max_n = ll_n*ww_n+ll_left_wn*wl_n  # 每层放的数量
    if ll_layer_max_n!=0:
        max_h_v_num =  (c_max_v*1000000/(goods_l*goods_w))//goods_h # 从体积角度出发的最大高度
        max_num = min(max_h_v_num, max_layer_n)  # 最大层高，综合高度和体积两个因素
        # if c_h==460:
        #     print('test EP125=======', max_h_v_num, max_layer_n)

    else:
        max_num = 0
    # print(ll_layer_max_n, '单层最大======test1=======最大高对比', max_h_v_num, max_layer_n)
    ll_method_n = int(max_num*ll_layer_max_n)  # 长长方法的最大数量
    lwh_left_list1 = [round(x) for x in [l_final_left, ww_left, int(c_h-max_num*goods_h)]]  # 最终长，宽，有效高的结余量

    ## 长宽放法
    lw_layer_max_n = lw_n*wl_n+ll_n*wl_left_wn  # 每层放的数量
    if ll_layer_max_n!=0:
        max_h_v_num2 =  (c_max_v*1000000/(goods_l*goods_w))//goods_h # 从体积角度出发的最大高度
        max_num2 = min(max_h_v_num2, max_layer_n)  # 最大层高，综合高度和体积两个因素
    else:
        max_num2 = 0
    # print(lw_layer_max_n, '单层最大======test2=========最大高对比', max_h_v_num2, max_layer_n)
    wl_method_n = int(max_num2*ll_layer_max_n)  # 长长方法的最大数量 
    lwh_left_list2 = [lw_left, w_final_left, int(c_h-max_num2*goods_h)]  # 最终长，宽，有效高的结余量

    # print('testttt',ll_method_n,wl_method_n)
    return [ll_method_n,wl_method_n],[lwh_left_list1, lwh_left_list2],[ll_layer_max_n, lw_layer_max_n]  # 长长放法数量，和宽长方法数量,每层放的数量



if __name__=='__main__':
    # goods_dict={
    #     'temp_type':'B20',              # 温区
    #     'goods_str':'107==>12*8*2;',     # 货物字符串,长度单位是里面（参考数据库）
    #     'can_reverse':1,                 # 1可以倒放
    #     'must_accept_bins':['PBX-EP46__EP46泡沫箱', 'PBX-EP133__EP133泡沫箱']      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    # }
    # goods_dict={
    #     'temp_type':'B20',              # 温区
    #     'goods_str':'1==>19*9*44;',     # 货物字符串
    #     'can_reverse':1,                 # 1可以倒放
    #     'must_accept_bins':[]            # 都可以接受
    # }

    goods_dict = {

        ####### 判断是否是M+
        'start_region_id':1234566,      # start, end region id用来找M+
        'end_region_id':1234567,
        'omc_time':'2022-12-25',        # 开始结束日期找M+

        ####### 温度可行箱子判断
        'omc_tem_id':'62',              # 温度id

        ####### 货物和订单属性
        'can_reverse':1,                # 1可以倒放, 空则0
        'goods_str':'107==>12*8*2;',    # 货物字符串,长度单位是里面（参考数据库）
        'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
        'specail_type_str':'B',         # 用来判断，可行箱子肯定性条件，空就没有要求

        #'must_accept_bins':['PBX-EP46__EP46泡沫箱', 'PBX-EP133__EP133泡沫箱']      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    }

    '''
    sto_id: 
    返回：'VIP168*2,VIP3*3'
    '''

    f_path = os.path.join(config.ROOT_PATH, 'data/bin/container_info.json')
    temp_container_dict = json.load(open(f_path, "rb")) # 参考json中的数据结构
    # select_able_containers(goods_dict,temp_container_dict)
    best_dict = select_best_container(goods_dict,temp_container_dict)
    print(best_dict)