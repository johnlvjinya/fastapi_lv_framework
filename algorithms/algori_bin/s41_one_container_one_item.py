
import sys
sys.path.append('../..')

import os
import json
import config
import pandas as pd
from myutils.func_decorated import log_func_time




class OneContainerOneItemSolution():

    def __init__(self, goods_dict):
        
        ######### 箱子信息的初始化
        f_path = os.path.join(config.f_path['data_json'], 'bin_config_temperature_vol.json')    ## 箱子温度对应的体积字典       
        self.config_temperature_vol = json.load(open(f_path, "rb"))

        f_path = os.path.join(config.f_path['data_json'], 'bin_info.json')             # 箱子的基本信息字典
        self.container_info = json.load(open(f_path, "rb"))

        f_path = os.path.join(config.f_path['data_json'], 'bin_route_constraint.json')  # 箱子的路由约束字典
        self.container_route_constraint = json.load(open(f_path, "rb")) 

        f_path = os.path.join(config.f_path['data_json'], 'bin_special_type.json')   # 箱子的特殊类型字典
        self.container_special_type = json.load(open(f_path, "rb"))

        f_path = os.path.join(config.f_path['data_json'], 'bin_m_plus_case_list.json')   # m+要求
        self.m_plus_case_dict = json.load(open(f_path, "rb"))

        f_path = os.path.join(config.f_path['data_json'], 'bin_route_type_dict.json')   # 路由的字典
        self.route_type_dict = json.load(open(f_path, "rb"))

        f_path = os.path.join(config.f_path['data_json'], 'bin_sto_id.json')   # 路由的字典
        self.container_sto_id = json.load(open(f_path, "rb"))

        f_path = os.path.join(config.f_path['data_json'], 'bin_para_settings.json')   # 路由的字典
        self.bin_para_settings = json.load(open(f_path, "rb"))

        ############# 货物信息的初始化
        self.goods_dict = goods_dict
        if self.goods_dict.get('can_reverse') not in [0, 1]:
            self.goods_dict['can_reverse'] = 0
        self.can_reverse = goods_dict.get('can_reverse')

        self.accept_bins_dict = None

        self.msg = {}  # 记录
        self.right_state = True  # 是否异常判断

    def one_goods_one_box_package(self, c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h):  ###### 将一种物品放入一个container
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
        ratio_dict = self.get_expand_ratio()
        EXPAND_RATIO_l = ratio_dict.get("ratio_l")
        EXPAND_RATIO_w = ratio_dict.get("ratio_w")
        EXPAND_RATIO_h = ratio_dict.get("ratio_h")

        goods_l,goods_w,goods_h = goods_l*EXPAND_RATIO_l,goods_w*EXPAND_RATIO_w,goods_h*EXPAND_RATIO_h
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
        wl_method_n = int(max_num2*ll_layer_max_n)  # 长长放法的最大数量 
        lwh_left_list2 = [lw_left, w_final_left, int(c_h-max_num2*goods_h)]  # 最终长，宽，有效高的结余量

        # print('testttt',ll_method_n,wl_method_n)
        return [ll_method_n,wl_method_n],[lwh_left_list1, lwh_left_list2],[ll_layer_max_n, lw_layer_max_n]  # 长长放法数量，和宽长方法数量,每层放的数量

    def check_goods_str(self):
        '''
        goods_dict = {

            ####### 判断是否是M+
            'start_region_id':1234566,      # start, end region id用来找M+,整型
            'end_region_id':1234567,
            'omc_time':'2022-12-25',        # 开始结束日期找M+

            ####### 温度可行箱子判断
            'omc_tem_id':'62',              # 温度id

            ####### 货物和订单属性
            'can_reverse':1,                # 1可以倒放, 空则0
            'goods_str':'107==>12*8*2;',    # 货物字符串,长度单位是里面（参考数据库）
            'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
            'specail_type_str':'',         # 用来判断，可行箱子肯定性条件，空就没有要求
        }
        '''
        self.msg['check_goods_str'] = []
        key_list = 'start_region_id,end_region_id,omc_time,omc_tem_id,can_reverse,goods_str,route_type,specail_type_str'.split(',')
        for i in key_list:
            if i not in self.goods_dict:
                self.msg['check_goods_str'].append('goods_dict没有%s字段'%i)
                self.right_state = False

        self.goods_dict['omc_tem_id'] = str(self.goods_dict['omc_tem_id'])

        not_null_list = 'omc_tem_id,goods_str'.split(',')
        for i in not_null_list:
            if not self.goods_dict[i]:
                self.msg['check_goods_str'].append('字段%s不能为空'%i)
                self.right_state = False
        if self.goods_dict.get('is_fragile') is None:
            self.goods_dict['is_fragile'] = 0
        if __name__=='__main__':
            print('test05\n', self.goods_dict)

    def get_expand_ratio(self):
        if self.goods_dict['is_fragile'] == 1:
            ratio_l = self.bin_para_settings.get('fragile_shape_ratio_l')
            ratio_w = self.bin_para_settings.get('fragile_shape_ratio_w')
            ratio_h = self.bin_para_settings.get('fragile_shape_ratio_h')
        else:
            ratio_l = 1
            ratio_w = 1
            ratio_h = 1           

        ratio_dict = {
            "ratio_l":ratio_l,
            "ratio_w":ratio_w,
            "ratio_h":ratio_h,
        }

        return ratio_dict

    def check_m_plus(self):
        ### 计算箱子是否需要M+类型
        omc_tem_id = str(self.goods_dict.get('omc_tem_id'))
        if omc_tem_id not in self.m_plus_case_dict:           ## 温度不属于M+
            return 0,[]
        else:
            temp_type_dict = self.m_plus_case_dict.get(omc_tem_id)
            if __name__=='__main__':
                print('起始地对应', self.goods_dict.get('start_region_id'),'====>', self.m_plus_case_dict.get(omc_tem_id).get('region_list'))
                print('结束地对应', self.goods_dict.get('end_region_id'),'====>', self.m_plus_case_dict.get(omc_tem_id).get('region_list'))
                print('时间对应', self.m_plus_case_dict.get(omc_tem_id).get('start_time'),self.goods_dict.get('omc_time'), self.m_plus_case_dict.get(omc_tem_id).get('end_time'))

            rg1 = self.goods_dict.get('start_region_id')
            rg2 = self.goods_dict.get('end_region_id')
            rg_list = self.m_plus_case_dict.get(omc_tem_id).get('region_list')

            tx = self.goods_dict.get('omc_time')
            t1 = self.m_plus_case_dict.get(omc_tem_id).get('start_time')
            t2 = self.m_plus_case_dict.get(omc_tem_id).get('end_time')

            if (rg1 in rg_list or rg2 in rg_list) and (tx>t1 and tx<t2): # 地区匹配
                m_plus_list = self.m_plus_case_dict.get(omc_tem_id).get('accept_bins')
                if __name__=='__main__':
                    print('属于M+!!!!!!!!!!!', m_plus_list)
                return 1, m_plus_list  # 一个状态，一个结果
            else:
                if __name__=='__main__':
                    print('不属于M+!!!!!!!!!!!')
                return 0,[]  # 否则不是M+类别

    def get_accept_bins(self):
        # print('============================accept_bins_dict')
        self.check_goods_str()
        if not self.right_state:
            return {}
        omc_tem_id = self.goods_dict['omc_tem_id']

        temp_type_dict = self.config_temperature_vol.get('temp_type')
        # if __name__=='__main__':
        #     print('accept_bins===', temp_type_dict)
        ### 根据温度筛选箱子
        accept_bins_dict = self.container_info.get(temp_type_dict.get(omc_tem_id))

        # print(accept_bins_dict)
        ## 如果存在特殊要求
        spetial_type = self.goods_dict.get('specail_type_str')
        m_state,bins_list = self.check_m_plus() 

        # 检查m+
        if m_state==1:
            ac_bins_list = bins_list

            bin_t1 = {}  # 保存在bin_t1中
            for bin_i in ac_bins_list:
                if bin_i in accept_bins_dict:
                    bin_t1[bin_i] = accept_bins_dict[bin_i]
            accept_bins_dict = bin_t1

        elif spetial_type:
            ## 找到接受的箱子
            ac_bins_list = self.container_special_type.get(spetial_type)

            bin_t1 = {}  # 保存在bin_t1中
            for bin_i in ac_bins_list:
                if bin_i in accept_bins_dict:
                    bin_t1[bin_i] = accept_bins_dict[bin_i]
            accept_bins_dict = bin_t1
        else:
            ## 普通类型的箱子
            ac_bins_list = self.container_special_type.get('常规')
            if accept_bins_dict is None:
                accept_bins_dict = {}

            # print('accept_bins_dict===',accept_bins_dict)
            bin_t1 = {}  # 保存在bin_t1中
            for bin_i in ac_bins_list:
                if bin_i in accept_bins_dict:
                    bin_t1[bin_i] = accept_bins_dict[bin_i]
            accept_bins_dict = bin_t1

        
        self.accept_bins_dict = accept_bins_dict
        omc_tem_id = self.goods_dict['omc_tem_id']  # 温度ID
        temp_vol_dict = self.config_temperature_vol.get('temp_vol')
        vol_p = temp_vol_dict.get(omc_tem_id)

        for k,v in self.accept_bins_dict.items():
            v['最大容积_L'] = min(v['有效高容积'], v['容积']*vol_p)
            # if __name__=='__main__':
            #     print('accept_bins===', k, '==>', v)
        
        return self.accept_bins_dict

    def select_able_one_bin_one_item(self,goods_str='107==>12*8*2;'):
        self.get_accept_bins()
        can_reverse = self.can_reverse

        ########## 计算货物的信息
        one_order_str = goods_str.rstrip(';')
        goods_qty = int(one_order_str.split('==>')[0])
        goods_shape = one_order_str.split('==>')[1]
        [goods_l,goods_w,goods_h] = [10*float(i) for i in goods_shape.split('*')]  # 将厘米变成毫米
        ########## print('[goods_qty,goods_l,goods_w,goods_h]', [goods_qty,goods_l,goods_w,goods_h])
        goods_vol_L = round(goods_qty*goods_l*goods_w*goods_h/1000000,2)

        ######## 查看哪些箱子能放得下
        c_container_dict = self.accept_bins_dict                        # 只保留接受的箱子
        if not c_container_dict:
            if __name__=='__main__':
                print('无解！没找到匹配条件的箱子')
            self.msg['no_solu'] = '无解！没找到匹配条件的箱子'
            return {}  # 无解

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
            list1,list2,list3 = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)

            # print(k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)
            if list1[0]!=0:
                if goods_qty%list1[0]==0:
                    bb_num = goods_qty//list1[0]
                else:
                    bb_num = goods_qty//list1[0]+1
                dict_x = {'箱子':k, '放法':'长长', '每个箱子':list1[0],'每层':list3[0],
                    '箱子数-不考虑余量':goods_qty//list1[0], # goods_qty//list1[0]+1,
                    'last箱':goods_qty%list1[0],
                    '余量':list1[0]-goods_qty%list1[0],
                    '箱子最大容积_L':round(v.get('最大容积_L'),1),
                    'lwh余量':list2[0],
                    '成本':round(v['成本']*bb_num,3)
                    }
                res_list.append(dict_x)

            if list1[1]!=0:
                if goods_qty%list1[1]==0:
                    bb_num = goods_qty//list1[1]
                else:
                    bb_num = goods_qty//list1[1]+1                         
                dict_x = {'箱子':k, '放法':'长宽', '每个箱子':list1[1],'每层':list3[1], 
                    '箱子数-不考虑余量':goods_qty//list1[1],
                    'last箱':goods_qty%list1[1],
                    '余量':list1[1]-goods_qty%list1[1],
                    '箱子最大容积_L':round(v.get('最大容积_L'),1),
                    'lwh余量':list2[1],
                    '成本':round(v['成本']*bb_num,3)
                    }
                res_list.append(dict_x)

            if can_reverse==1:
                ########### 长高倒放，不考虑更复杂旋转
                a,b,c = goods_l,goods_w,goods_h
                goods_l = max(c, b)
                goods_w = min(c, b)
                goods_h = a
                list1,list2,list3 = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                # print('长高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2) 
                if list1[0]!=0:
                    if goods_qty%list1[0]==0:
                        bb_num = goods_qty//list1[0]
                    else:
                        bb_num = goods_qty//list1[0]+1
                    dict_x = {'箱子':k, '放法':'长长', '每个箱子':list1[0],'每层':list3[0],
                        '箱子数-不考虑余量':goods_qty//list1[0], # goods_qty//list1[0]+1,
                        'last箱':goods_qty%list1[0],
                        '余量':list1[0]-goods_qty%list1[0],
                        '箱子最大容积_L':round(v.get('最大容积_L'),1),
                        'lwh余量':list2[0],
                        '成本':round(v['成本']*bb_num,3)
                        }
                    res_list.append(dict_x)

                if list1[1]!=0:
                    if goods_qty%list1[1]==0:
                        bb_num = goods_qty//list1[1]
                    else:
                        bb_num = goods_qty//list1[1]+1                       
                    dict_x = {'箱子':k, '放法':'长宽', '每个箱子':list1[1],'每层':list3[1], 
                        '箱子数-不考虑余量':goods_qty//list1[1],
                        'last箱':goods_qty%list1[1],
                        '余量':list1[1]-goods_qty%list1[1],
                        '箱子最大容积_L':round(v.get('最大容积_L'),1),
                        'lwh余量':list2[1],
                        '成本':round(v['成本']*bb_num,3)
                        }
                    res_list.append(dict_x)

                ########### 宽高倒放，不考虑更复杂旋转
                a,b,c = goods_l,goods_w,goods_h
                goods_l = max(c, a)
                goods_w = min(c, a)
                goods_h = b
                list1,list2,list3 = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                # print('宽高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)    
                if list1[0]!=0:
                    if goods_qty%list1[0]==0:
                        bb_num = goods_qty//list1[0]
                    else:
                        bb_num = goods_qty//list1[0]+1
                    dict_x = {'箱子':k, '放法':'长长', '每个箱子':list1[0],'每层':list3[0],
                        '箱子数-不考虑余量':goods_qty//list1[0], # goods_qty//list1[0]+1,
                        'last箱':goods_qty%list1[0],
                        '余量':list1[0]-goods_qty%list1[0],
                        '箱子最大容积_L':round(v.get('最大容积_L'),1),
                        'lwh余量':list2[0],
                        '成本':round(v['成本']*bb_num,3)
                        }
                    res_list.append(dict_x)
                
                if list1[1]!=0:
                    if goods_qty%list1[1]==0:
                        bb_num = goods_qty//list1[1]
                    else:
                        bb_num = goods_qty//list1[1]+1                                            
                    dict_x = {'箱子':k, '放法':'长宽', '每个箱子':list1[1],'每层':list3[1], 
                        '箱子数-不考虑余量':goods_qty//list1[1],
                        'last箱':goods_qty%list1[1],
                        '余量':list1[1]-goods_qty%list1[1],
                        '箱子最大容积_L':round(v.get('最大容积_L'),1),
                        'lwh余量':list2[1],
                        '成本':round(v['成本']*bb_num,3)
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

    def one_container_one_item(self,goods_str='107==>12*8*2;'):
        # print('go to ...............one_container_one_item')
        res_list = self.select_able_one_bin_one_item(goods_str=goods_str)
        cost = 1000000000
        best_dict = {}
        for k in res_list:
            # print(k) 
            if k['成本']<cost:
                cost = k['成本']
                best_dict = k
        # print(best_dict)
        return best_dict

    def multi_container_one_item(self,goods_str='1070==>12*8*2;'):
        # print('go to ...............multi_container_one_item')
        res_list = self.select_able_one_bin_one_item(goods_str=goods_str)
        cost = 1000000000
        best_dict = {}
        able_container_list = []
        appear_list = []
        if __name__=='__main__':
            print('\ntest02')
            for res in res_list:
                print(res)
        for k in res_list:
            if k['箱子'] not in appear_list:
                able_container_list.append({k['箱子']:k['每个箱子']})
                appear_list.append(k['箱子'])
            if k['成本']<cost:
                cost = k['成本']
                best_dict = k
        best_dict['货物'] = goods_str
        best_dict['可选箱型'] = able_container_list
        if __name__=='__main__':
            print('\ntest3\n', best_dict)
        return best_dict

    def multi_container_multi_item(self):    # 将不同的货物放入最合适的container中，然后再考虑合并
        # print('go to ...............multi_container_one_item')
        multi_goods_str = self.goods_dict['goods_str'].rstrip(';')      # 拆分货物
        goods_str_list = multi_goods_str.split(';')
        item_container_list = []
        no_solution_goods_list = []

        # dict_x = {
        #     '箱子':k, 
        #     '放法':'长宽', 
        #     '每个箱子':list1[1],
        #     '每层':list3[1], 
        #     '箱子数-不考虑余量':goods_qty//list1[1],
        #     'last箱':goods_qty%list1[1],
        #     '余量':list1[1]-goods_qty%list1[1],
        #     '箱子最大容积_L':v.get('最大容积_L'),
        #     'lwh余量':list2[1],
        #     '成本':round(v['成本']*bb_num,3),'单位成本':round(v['成本']/list1[1], 3)
        # }

        for goods_str in goods_str_list:
            item_plan = self.multi_container_one_item(goods_str)
            if __name__=='__main__':                                # 测试时打印
                print('(%s)'%goods_str, '====>', item_plan)
            item_container_list.append(item_plan)                   # 可行的装箱方案
            if not item_plan.get('可选箱型'):
                no_solution_goods_list.append(goods_str)

        ############### 步骤一，每个货物用到的箱子减1
        container_need_dict = {}
        if __name__=='__main__':
            print('\ntest1\n', item_container_list)
        for item_plan in item_container_list:
            if item_plan.get('箱子'):
                if item_plan['箱子'] not in container_need_dict.keys():
                    container_need_dict[item_plan['箱子']] = item_plan['箱子数-不考虑余量']
                else:
                    container_need_dict[item_plan['箱子']] += item_plan['箱子数-不考虑余量']
                item_plan.pop('箱子数-不考虑余量')

        if len(item_container_list)==0:  # 没找到解
            res_dict = {'msg':self.msg, 'msg2':'没有匹配的箱型', '货物信息':self.goods_dict}
            return res_dict

        # print('================取整的箱子')
        # print(container_need_dict)
        # print('\n================待合并的箱子,重新梳理信息')
        rows = []
        for item_plan in item_container_list:
            if item_plan.get('箱子'):
                l,w,h=[float(x) for x in item_plan['货物'].split('==>')[1].split('*')]
                goods_total_vol = round(item_plan['last箱']*l*w*h/1000,4) # 货物体积
                rows_i = [
                            item_plan['货物'].split('==>')[1], # 货物尺寸
                            l,
                            w,
                            h, # 货物长宽高
                            goods_total_vol,
                            item_plan['箱子'], # 箱型
                            item_plan['箱子最大容积_L'], # 箱型
                            item_plan['last箱'],  # 货物数量
                            len(item_plan['可选箱型'])] # 可选箱型数量
                # print(item_plan) 
                rows.append(rows_i)
        cols_list = '货物尺寸,l,w,h,货物总体积_L,箱型,箱子最大容积_L,货物余量,可选箱型数量'.split(",")
        df = pd.DataFrame(rows, columns=cols_list)
        df = df.sort_values('货物总体积_L', ascending=False)
        df = df.sort_values('可选箱型数量', ascending=True).reset_index(drop=True)
        if __name__=='__main__':
            for k in df.columns:
                print('test7....', k)
        df = df[df['货物余量']!=0].reset_index(drop=True)          # 排除货物余量为0的货物


        # df.to_excel('test2.xlsx', index=False)

        
        # print('================取整的箱子')
        # print(container_need_dict)
        # if df.shape[0]==0:  # 没找到解
        #     res_dict = {'msg':self.msg}
        #     return res_dict

        # df = df[df['last箱']!=0].reset_index()
        ############### 步骤二，选择可选箱型最少的那个货物作为主箱子，如果都一样多，那么选择单个货物体积最大的作为主箱子

        if df.shape[0]>0:

            sum_vol = df['货物总体积_L'].sum()
            can_reverse = self.goods_dict.get('can_reverse')
            sum_container_vol = 0
            container_exists_list = list(container_need_dict.keys())
            # print(df)
            if df['箱型'][0] in container_exists_list:
                container_need_dict[df['箱型'][0]] += 1
            else:
                container_need_dict[df['箱型'][0]] = 1

            sum_container_vol += df['箱子最大容积_L'][0]
            for i in range(1, df.shape[0]):
                
                if can_reverse==1 and 0.8*sum_container_vol>sum_vol and df['可选箱型数量'][i]>1:
                    break
                if can_reverse==0 and 0.7*sum_container_vol>sum_vol and df['可选箱型数量'][i]>1:
                    break

                sum_container_vol += df['箱子最大容积_L'][i]
                if df['箱型'][i] in container_exists_list:
                    container_need_dict[df['箱型'][i]] += 1
                else:
                    container_need_dict[df['箱型'][i]] = 1

            # print(temp_container_dict.get(df['箱型'][i]))
        
        # print(container_need_dict)
        dict1 = {}
        res_str = ''
        
        bin_list = []
        for k,v in container_need_dict.items():
            if v!=0:
                res_for_bussiness = {}
                dict1[k] = v
                res_str += '%s*%s,'%(str(k), str(v))
                res_for_bussiness['sto_id'] = str(self.container_sto_id.get(k))
                res_for_bussiness['sto_name'] = k
                res_for_bussiness['num'] = str(v)
                bin_list.append(res_for_bussiness)

        res_dict = {
            'no_solution_goods':no_solution_goods_list,
            'res_dict':dict1,
            'res_str':res_str.rstrip(','),
            'res_for_bussiness':{'plan1':bin_list},
            'msg':self.msg
        }
        if __name__=='__main__':
            print('\nmulti_goods_str:', multi_goods_str, '================最终选的箱子:', res_dict)
        if not res_dict:
            res_dict = {'msg':self.msg}
        return res_dict

    def run(self):
        # self.check_goods_str()
        # self.check_m_plus()
        # self.get_accept_bins()
        # self.one_container_one_item()
        # self.multi_container_one_item()
        self.multi_container_multi_item()


if __name__=='__main__':
    goods_dict = {

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
        'goods_str':'20==>16.5*8.5*3.0',    # 货物字符串,长度单位是里面（参考数据库）
    }

    goods_dict = {

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
        'goods_str':'3==>13*30*10;10==>120*7*2;10==>120*70*2;',    # 货物字符串,长度单位是里面（参考数据库）
    }

    # goods_dict = {'start_region_id': 350200, 
    # 'end_region_id': 520300, 'omc_time': '2021-09-23', 
    # 'route_type': -1, 'specail_type_str': '', 'omc_tem_id': 41, 
    # 'can_reverse': 0, 'goods_str': '1==>5.0*1.0*1.0','is_fragile':0
    # }


    # goods_dict = {'start_region_id': 120000, 'end_region_id': 310000, 
    # 'omc_time': '2022-02-14', 'route_type': -1, 'specail_type_str': '', 
    # 'omc_tem_id': 51, 'can_reverse': 1, 'goods_str': '1==>5.0*1.0*1.0'}
     
    # goods_dict = {'start_region_id': 350200, 
    # 'end_region_id': 520300, 'omc_time': '2021-09-23', 
    # 'route_type': -1, 'specail_type_str': '', 'omc_tem_id': 41, 
    # 'can_reverse': 0, 'goods_str': '27==>13.0*13.0*13.0;6==>6.0*6.0*6.0','is_fragile':0
    # }

    # goods_dict = {

    #     ####### 判断是否是M+
    #     'start_region_id':140100,      # start, end region id用来找M+
    #     'end_region_id':140300,
    #     'omc_time':'2021-08-23',        # 开始结束日期找M+

    #     'route_type':'',                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
    #     'specail_type_str':'',         # 用来判断，可行箱子肯定性条件，空就没有要求

    #     ####### 温度可行箱子判断
    #     'omc_tem_id':'25',              # 温度id

    #     ####### 货物和订单属性
    #     'can_reverse':0,                # 1可以倒放, 空则0
    #     'goods_str':'2==>11*11*11;1==>10*10*10;',    # 货物字符串,长度单位是里面（参考数据库）
    # }




    '''
    sto_id: 
    返回：'VIP168*2,VIP3*3'
    '''
    OneContainerOneItemSolution(goods_dict).run()

