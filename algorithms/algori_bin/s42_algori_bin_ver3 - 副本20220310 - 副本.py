
import sys
sys.path.append('../..')

import os
import json
import config
import pandas as pd
from myutils.func_decorated import log_func_time
from copy import deepcopy



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
        self.goods_type_num = None  # 货物类型的数量
        self.m_state = None  # m+
        self.m_bins_list = None # m+

        self.thermometer_shape = '12*10*3'  # 温度计的尺寸
        self.shape_thermometer_num = {}

        if __name__=='__main__':
            if os.path.exists('test_output') is False:os.mkdir('test_output')

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

        ####### 长长放法
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

        ####### 长宽放法
        lw_layer_max_n = lw_n*wl_n+ll_n*wl_left_wn  # 每层放的数量
        if ll_layer_max_n!=0:
            max_h_v_num2 =  (c_max_v*1000000/(goods_l*goods_w))//goods_h # 从体积角度出发的最大高度
            max_num2 = min(max_h_v_num2, max_layer_n)  # 最大层高，综合高度和体积两个因素
        else:
            max_num2 = 0
        # print(lw_layer_max_n, '单层最大======test2=========最大高对比', max_h_v_num2, max_layer_n)
        wl_method_n = int(max_num2*ll_layer_max_n)  # 长长放法的最大数量 
        lwh_left_list2 = [int(x) for x in [lw_left, w_final_left, int(c_h-max_num2*goods_h)]]  # 最终长，宽，有效高的结余量

        # print('testttt',ll_method_n,wl_method_n)

        # ll_n = c_l//goods_l       # 长长数，货物的长对应container的长，最多放的个数
        # ww_n = c_w//goods_w       # 宽宽数
        # wl_n = c_w//goods_l       # 宽长数
        # lw_n = c_l//goods_w       # 长宽数

        dict_str = json.dumps({"长长数":int(ll_n),"宽宽数":int(ww_n), "宽长数":int(wl_n), "长宽数":int(lw_n), "层数":int(max_layer_n)})
        return [ll_method_n,wl_method_n],[lwh_left_list1, lwh_left_list2],[ll_layer_max_n, lw_layer_max_n],dict_str  # 长长放法数量，和宽长方法数量,每层放的数量

    def get_min_num_x1x2(self, x1, x2):
        if x1%x2 ==0:
            return int(x1//x2)
        else:
            return int(x1//x2)+1

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

        ########################################################################################### 字段不能为空
        self.goods_dict['omc_tem_id'] = str(self.goods_dict['omc_tem_id'])
        not_null_list = 'omc_tem_id,goods_str'.split(',')
        for i in not_null_list:
            if not self.goods_dict[i]:
                self.msg['check_goods_str'].append('字段%s不能为空'%i)
                self.right_state = False
        if self.goods_dict.get('is_fragile') is None:
            self.goods_dict['is_fragile'] = 0
        # if __name__=='__main__':
        #     print('\ntest05,self.goods_dict:', self.goods_dict)

        ################################################################################ EP箱型多类型货物不支持计算
        temp_type_dict = self.config_temperature_vol.get('temp_type')
        omc_tem_id = self.goods_dict['omc_tem_id']
        if int(omc_tem_id)==71:
            self.right_state = False
            self.msg['液氨'] = '液氨不支持计算'

        # if temp_type_dict.get(omc_tem_id)!='T0' and self.goods_type_num>=2:
        #     self.msg['check_goods_str'].append('EP箱型多类型货物不支持计算')
        #     self.right_state = False

        ############################################################################# 整理货物字典,根据货物的单个尺寸排序，并考虑温度计的尺寸
        goods_str_list = self.goods_dict['goods_str'].rstrip(';').split(';')
        # self.thermometer_shape = '12*10*3'  # 温度计的尺寸
        goods_str_dict = {}
        sort_area_dict = {}
        ############################### 第一步，先合并一模一样的尺寸
        for goods_str in goods_str_list:
            shape_str = goods_str.split('==>')[1]
            num_str = goods_str.split('==>')[0]

            if shape_str not in goods_str_dict:
                goods_str_dict[shape_str] = {}
                goods_str_dict[shape_str]['num'] = int(num_str)  # 注意
                goods_str_dict[shape_str]['底面积'] = float(shape_str.split('*')[0])*float(shape_str.split('*')[1])  # 底面积cm2,底面积大的先放
                
                sort_area_dict[shape_str] = goods_str_dict[shape_str]['底面积']**0.5 * int(num_str)
            else:
                goods_str_dict[shape_str]['num'] += int(num_str)
                sort_area_dict[shape_str] += goods_str_dict[shape_str]['底面积']**0.5 * int(num_str)



        ################### 根据货物底面积降序排列
        # print('\ntest0001, sort_area_dict1:',sort_area_dict)
        sort_area_dict = dict(sorted(sort_area_dict.items(), key=lambda item:item[1], reverse=True))
        # print('\ntest0002, sort_area_dict:',sort_area_dict)

        final_goods_dict = {}
        for k in sort_area_dict:
            final_goods_dict[k] = goods_str_dict[k]

        self.final_goods_dict = final_goods_dict
        self.goods_type_num = len(self.final_goods_dict)
        # if __name__=='__main__':
        #     print('self.goods_type_num货物类型数量..........',self.goods_type_num)
        ############################## 第二部,将温度计变成货物,占用的体积越小越好.
        tlwh = [float(x) for x in self.thermometer_shape.split('*')]  #### 温度计的长宽高
        tlwh.sort()
        tmin1 = tlwh[0]  # 温度计的最短边
        tmiddle1 = tlwh[1] 
        tmax1 = tlwh[2] 

        #### 货物尺寸 

        for k,v in self.final_goods_dict.items():
            
            lwh = [float(x) for x in k.split('*')]
            lwh.sort()
            min1 = lwh[0]           # 货物的最短边
            middle1 = lwh[1] 
            max1 = lwh[2]        #### 货物尺寸

            ############# 问题几个货物加起来就比温度计长宽高都大了?
            ### 温度计-货物
            ### 可能性1: l-l, w-w, h-h  # 这样对应
            n1 = self.get_min_num_x1x2(tmin1, min1)*self.get_min_num_x1x2(tmiddle1, middle1)*self.get_min_num_x1x2(tmax1, max1)
            # print(self.get_min_num_x1x2(tmin1, min1))
            # print(self.get_min_num_x1x2(tmiddle1, middle1))
            # print(self.get_min_num_x1x2(tmax1, max1))
            ### 可能性2: l-l, w-h, h-w  # 这样对应
            n2 = self.get_min_num_x1x2(tmin1, min1)*self.get_min_num_x1x2(tmiddle1, max1)*self.get_min_num_x1x2(tmax1, middle1)
            ### 可能性3: l-w, w-l, h-h  # 这样对应
            n3 = self.get_min_num_x1x2(tmin1, middle1)*self.get_min_num_x1x2(tmiddle1, min1)*self.get_min_num_x1x2(tmax1, max1)
            ### 可能性4: l-w, w-h, h-l  # 这样对应
            n4 = self.get_min_num_x1x2(tmin1, middle1)*self.get_min_num_x1x2(tmiddle1, max1)*self.get_min_num_x1x2(tmax1, tmin1)
            # print('tmax1, tmin1', tmax1, tmin1, self.get_min_num_x1x2(tmax1, tmin1))
            # print(self.get_min_num_x1x2(tmiddle1, max1))
            # print(self.get_min_num_x1x2(tmax1, tmin1))
            ### 可能性5: l-h, w-w, h-l  # 这样对应
            n5 = self.get_min_num_x1x2(tmin1, max1)*self.get_min_num_x1x2(tmiddle1, middle1)*self.get_min_num_x1x2(tmax1, tmin1)
            ### 可能性6: l-h, w-l, h-w  # 这样对应
            n6 = self.get_min_num_x1x2(tmin1, max1)*self.get_min_num_x1x2(tmiddle1, min1)*self.get_min_num_x1x2(tmax1, middle1)


            min_n123456 = min([n1, n2, n3, n4, n5, n6])
            goods_str = '%s==>%s'%(str(int(v['num'])), k)  # 构造货物的字符串

            self.shape_thermometer_num[goods_str] = min_n123456
            # self.shape_thermometer_num[goods_str] = 0  # 不考虑温度计
            # print('self.shape_thermometer_num[goods_str]温度计货物等效数量...', self.shape_thermometer_num[goods_str])
            # print('test002, tlwh, lwh..........', tlwh, lwh, 'n123456', [n1, n2, n3, n4, n5, n6])
            ############# 保存最小的货物体积
        # print('self.shape_thermometer_num',self.thermometer_shape, self.shape_thermometer_num)
        # ####### 找到温度计对应几个货物后,修改货物的数量(================================================================待完成)
     

        # print('\ntest0001, goods_str_dict:',goods_str_dict)
        # print('\ntest0002, sort_area_dict:',sort_area_dict)
        # print('\ntest0003, self.final_goods_dict:',self.final_goods_dict)

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
            # if __name__=='__main__':
            #     print('起始地对应', self.goods_dict.get('start_region_id'),'====>', self.m_plus_case_dict.get(omc_tem_id).get('region_list'))
            #     print('结束地对应', self.goods_dict.get('end_region_id'),'====>', self.m_plus_case_dict.get(omc_tem_id).get('region_list'))
            #     print('时间对应', self.m_plus_case_dict.get(omc_tem_id).get('start_time'),self.goods_dict.get('omc_time'), self.m_plus_case_dict.get(omc_tem_id).get('end_time'))

            rg1 = self.goods_dict.get('start_region_id')
            rg2 = self.goods_dict.get('end_region_id')
            rg_list = self.m_plus_case_dict.get(omc_tem_id).get('region_list')

            tx = self.goods_dict.get('omc_time')
            t1 = self.m_plus_case_dict.get(omc_tem_id).get('start_time')
            t2 = self.m_plus_case_dict.get(omc_tem_id).get('end_time')

            if (rg1 in rg_list or rg2 in rg_list) and (tx>t1 and tx<t2): # 地区匹配
                # m_plus_list = self.m_plus_case_dict.get(omc_tem_id).get('accept_bins')
                m_plus_list = self.container_special_type.get('M+')    ########### 考虑所有的M+
                if __name__=='__main__':
                    print('属于M+!!!!!!!!!!!', m_plus_list)
                return 1, m_plus_list  # 一个状态，一个结果
            else:
                # if __name__=='__main__':
                #     print('不属于M+!!!!!!!!!!!')
                return 0,[]  # 否则不是M+类别

    def get_accept_bins(self):
        # print('============================accept_bins_dict')

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
            # print(k,'==>', v)
            if k=='EP6泡沫箱':
                v['最大容积_L'] = min(v['有效高容积'], v['容积']*0.11)
            else:
                v['最大容积_L'] = min(v['有效高容积'], v['容积']*vol_p)
            # if __name__=='__main__':
            #     print('accept_bins===', k, '==>', v)
        
        return self.accept_bins_dict

    def select_able_one_bin_one_item(self,goods_str='107==>12*8*2;'):
        self.get_accept_bins()  # 首先得到可以用的箱型
        can_reverse = self.can_reverse

        ########## 计算货物的信息
        one_order_str = goods_str.rstrip(';')
        goods_qty = int(one_order_str.split('==>')[0])
        goods_shape = one_order_str.split('==>')[1]

        [goods_lx,goods_wx,goods_hx] = [float(i) for i in goods_shape.split('*')]  # 将厘米变成毫米

        goods_l_real = max(goods_lx,goods_wx)
        goods_w_real = min(goods_lx,goods_wx)
        goods_h_real = min(goods_hx,1000000)
        ########## print('[goods_qty,goods_l,goods_w,goods_h]', [goods_qty,goods_l,goods_w,goods_h])
        goods_vol_L = round(goods_qty*goods_l_real*goods_w_real*goods_h_real/1000000,2)

        ######## 查看哪些箱子能放得下

        dict_x = {
                    '箱子':'no_solution',
                    '箱长':'no_solution',
                    '箱宽':'no_solution',
                    '箱高':'no_solution',
                    'max_L':'no_solution',
                    '放法':'no_solution',
                    'dict_str':'no_solution',
                    'l':goods_l_real,
                    'w':goods_w_real,
                    'h':goods_h_real,                        
                    '每箱':'no_solution',
                    '层数':'no_solution',
                    '每层':'no_solution',
                    '整箱':'no_solution',
                    'last箱':'no_solution',
                    '余量':'no_solution',
                    'bb_num':'no_solution',
                    'l余量':'no_solution',
                    'w余量':'no_solution',
                    'h余量':'no_solution',
                    '成本':'no_solution',
                    }
        no_solution_list = [dict_x]

        c_container_dict = self.accept_bins_dict                        # 只保留接受的箱子
        if not c_container_dict:
            return no_solution_list

        res_list = []
        for k,v in c_container_dict.items():
            # print('最大容积_L, goods_vol_L', v['最大容积_L'], goods_vol_L)
                # print('\n考虑这个箱子==============',k)
                # v.pop('温度使用范围_C') 
                # print('可行的箱子：', k, '===>', v)
            c_l = round(v.get('长')/10,1)  # 变成厘米
            c_w = round(v.get('宽')/10,1)
            c_h = round(v.get('有效高')/10,1)


            c_max_v = v.get('最大容积_L')
            goods_l = goods_l_real
            goods_w = goods_w_real
            goods_h = goods_h_real
            # print('正常', goods_lt,goods_wt,goods_ht,goods_l,goods_w,goods_h)
            list1,list2,list3,dict_str = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)

            # print(k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)
            if list1[0]!=0:
                if goods_qty%list1[0]==0:
                    bb_num = goods_qty//list1[0]
                else:
                    bb_num = goods_qty//list1[0]+1
                dict_x = {
                    '箱子':k,
                    '箱长':c_l,
                    '箱宽':c_w,
                    '箱高':c_h,
                    'max_L':round(v.get('最大容积_L'),1),
                    '放法':'长长',
                    'dict_str':dict_str,
                    'l':goods_l,
                    'w':goods_w,
                    'h':goods_h,
                    '每箱':list1[0],
                    '层数':int(list1[0]/list3[0]),
                    '每层':int(list3[0]),
                    '整箱':goods_qty//list1[0], # goods_qty//list1[0]+1,
                    'last箱':goods_qty%list1[0],
                    '余量':list1[0]-goods_qty%list1[0],
                    'bb_num':bb_num,

                    'l余量':list2[0][0],
                    'w余量':list2[0][1],
                    'h余量':list2[0][2],
                    '成本':round(v['成本']*bb_num,3)
                    }
                # print('l余量...............', list2[0][0], type(list2[0][0]))
                res_list.append(dict_x)

            if list1[1]!=0:
                if goods_qty%list1[1]==0:
                    bb_num = goods_qty//list1[1]
                else:
                    bb_num = goods_qty//list1[1]+1                         
                dict_x = {
                    '箱子':k,
                    '箱长':c_l,
                    '箱宽':c_w,
                    '箱高':c_h,
                    'max_L':round(v.get('最大容积_L'),1),
                    '放法':'长宽', 
                    'dict_str':dict_str,
                    'l':goods_l,
                    'w':goods_w,
                    'h':goods_h,                    
                    '每箱':list1[1],
                    '层数':int(list1[1]/list3[1]),
                    '每层':int(list3[1]), 
                    '整箱':goods_qty//list1[1],
                    'last箱':goods_qty%list1[1],
                    '余量':list1[1]-goods_qty%list1[1],
                    'bb_num':bb_num,
                    'l余量':list2[1][0],
                    'w余量':list2[1][1],
                    'h余量':list2[1][2],
                    '成本':round(v['成本']*bb_num,3)
                    }
                res_list.append(dict_x)

            if can_reverse==1:
                ########### 长高倒放，不考虑更复杂旋转
                goods_l = goods_h_real
                goods_w = goods_w_real
                goods_h = goods_l_real
                # print('长高倒放', goods_lt,goods_wt,goods_ht,goods_h,goods_w,goods_l)
                list1,list2,list3,dict_str = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                # print('长高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2) 
                if list1[0]!=0:
                    if goods_qty%list1[0]==0:
                        bb_num = goods_qty//list1[0]
                    else:
                        bb_num = goods_qty//list1[0]+1
                    dict_x = {
                        '箱子':k,
                        '箱长':c_l,
                        '箱宽':c_w,
                        '箱高':c_h,
                        'max_L':round(v.get('最大容积_L'),1),
                        '放法':'长长-lh倒',
                        'dict_str':dict_str,
                        'l':goods_l,
                        'w':goods_w,
                        'h':goods_h,
                        '每箱':list1[0],
                        '层数':int(list1[0]/list3[0]),
                        '每层':int(list3[0]),
                        '整箱':goods_qty//list1[0], # goods_qty//list1[0]+1,
                        'last箱':goods_qty%list1[0],
                        '余量':list1[0]-goods_qty%list1[0],
                        'bb_num':bb_num,
                        'l余量':list2[0][0],
                        'w余量':list2[0][1],
                        'h余量':list2[0][2],
                        '成本':round(v['成本']*bb_num,3)
                        }
                    res_list.append(dict_x)

                if list1[1]!=0:
                    if goods_qty%list1[1]==0:
                        bb_num = goods_qty//list1[1]
                    else:
                        bb_num = goods_qty//list1[1]+1                       
                    dict_x = {
                        '箱子':k,
                        '箱长':c_l,
                        '箱宽':c_w,
                        '箱高':c_h,
                        'max_L':round(v.get('最大容积_L'),1),
                        '放法':'长宽-lh倒',
                        'dict_str':dict_str,
                        'l':goods_l,
                        'w':goods_w,
                        'h':goods_h,                         
                        '每箱':list1[1],
                        '层数':int(list1[1]/list3[1]),
                        '每层':int(list3[1]), 
                        '整箱':goods_qty//list1[1],
                        'last箱':goods_qty%list1[1],
                        '余量':list1[1]-goods_qty%list1[1],
                        'bb_num':bb_num,
                        'l余量':list2[1][0],
                        'w余量':list2[1][1],
                        'h余量':list2[1][2],
                        '成本':round(v['成本']*bb_num,3)
                        }
                    res_list.append(dict_x)

                ########### 宽高倒放，不考虑更复杂旋转
                goods_l = goods_l_real
                goods_w = goods_h_real
                goods_h = goods_w_real
                # print('宽高倒放',goods_lt,goods_wt,goods_ht ,goods_h,goods_w,goods_l)
                list1,list2,list3,dict_str = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                # print('宽高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)    
                if list1[0]!=0:
                    if goods_qty%list1[0]==0:
                        bb_num = goods_qty//list1[0]
                    else:
                        bb_num = goods_qty//list1[0]+1
                    dict_x = {
                        '箱子':k,
                        '箱长':c_l,
                        '箱宽':c_w,
                        '箱高':c_h,
                        'max_L':round(v.get('最大容积_L'),1),
                        '放法':'长长-wh倒',
                        'dict_str':dict_str,
                        'l':goods_l,
                        'w':goods_w,
                        'h':goods_h,
                        '每箱':list1[0],
                        '层数':int(list1[0]/list3[0]),
                        '每层':int(list3[0]),
                        '整箱':goods_qty//list1[0], # goods_qty//list1[0]+1,
                        'last箱':goods_qty%list1[0],
                        '余量':list1[0]-goods_qty%list1[0],
                        'bb_num':bb_num,
                        'l余量':list2[0][0],
                        'w余量':list2[0][1],
                        'h余量':list2[0][2],
                        '成本':round(v['成本']*bb_num,3)
                        }
                    res_list.append(dict_x)
                
                if list1[1]!=0:
                    if goods_qty%list1[1]==0:
                        bb_num = goods_qty//list1[1]
                    else:
                        bb_num = goods_qty//list1[1]+1                                            
                    dict_x = {
                        '箱子':k,
                        '箱长':c_l,
                        '箱宽':c_w,
                        '箱高':c_h,
                        'max_L':round(v.get('最大容积_L'),1), 
                        '放法':'长宽-wh倒',
                        'dict_str':dict_str,
                        'l':goods_l,
                        'w':goods_w,
                        'h':goods_h,                        
                        '每箱':list1[1],
                        '层数':int(list1[1]/list3[1]),
                        '每层':int(list3[1]), 
                        '整箱':goods_qty//list1[1],
                        'last箱':goods_qty%list1[1],
                        '余量':list1[1]-goods_qty%list1[1],
                        'bb_num':bb_num,
                        'l余量':list2[1][0],
                        'w余量':list2[1][1],
                        'h余量':list2[1][2],
                        '成本':round(v['成本']*bb_num,3)
                        }
                    res_list.append(dict_x)

        if len(res_list)>0:
            return res_list

        else:
            return no_solution_list
            
    def solution_list(self):
        # print('go to ...............multi_container_one_item')
        cols_list = ['good_str', '箱子', '箱长', '箱宽', '箱高', 'max_L', '放法','dict_str', 'l','w','h', '每箱', '层数', '每层', '整箱', 'last箱', '余量','bb_num', 'l余量', 'w余量', 'h余量', '成本']
        df = pd.DataFrame([], columns=cols_list)
        bins_cost = self.container_info.get('bin_成本')

        ############################################################################ 货物尺寸的列表
        goods_str_list = []

        ############# 循环所有货物，看看各个箱子能装多少
        for k,v in self.final_goods_dict.items():
            goods_str = '%s==>%s'%(str(int(v['num'])), k)  # 构造货物的字符串
            goods_str_list.append(goods_str)

            res_list = self.select_able_one_bin_one_item(goods_str=goods_str)
            # print('\ntest005, self.shape_thermometer_num', self.shape_thermometer_num)
            ##################################################################### 长宽高都不够放温度计了,需要将温度计折算成货物数量
            for i in res_list:
                if i['l余量']=='no_solution':
                    continue
                if max([i['l余量'], i['w余量'], i['h余量']])<3:

                    i['last箱']+=self.shape_thermometer_num[goods_str]
                    if i['last箱']>=i['每箱']:
                        i['整箱']+=i['last箱']//i['每箱']
                        i['last箱'] = i['last箱']%i['每箱']
                        if i['last箱']==0:
                            n = i['整箱']
                        else:
                            n = i['整箱']+1
                        i['成本'] = bins_cost.get(i['箱子'])*n

                    i['余量'] = i['每箱']-(i['last箱']+i['整箱']*i['每箱'])%i['每箱']


            df_i = pd.DataFrame(res_list)
            df_i.insert(0, 'good_str', goods_str)
            df = df.append(df_i)

        ############ 找到无解的货物
        no_solution_df = df[df['箱子']=='no_solution'].reset_index(drop=True)
        if no_solution_df.shape[0]>0:
            no_solution_goods = no_solution_df['good_str'].tolist()
        else:
            no_solution_goods = []

        ############ 找到有解的货物
        has_solution_goods1 = list(set(goods_str_list)-set(no_solution_goods))
        has_solution_goods = []
        ########### 构造有解货物字符串
        for k,v in self.final_goods_dict.items():
            goods_str = '%s==>%s'%(str(int(v['num'])), k)  # 构造货物的字符串
            if goods_str in has_solution_goods1:
                has_solution_goods.append(goods_str)

        # print('\ntest09,has_solution_goods:', no_solution_goods)
        # print('\ntest10,has_solution_goods:', has_solution_goods)
        mydict = {'no_solution_goods':no_solution_goods}
        if df.shape[0] == 0:
            return mydict    # 没有有效的货物，直接返回
        if len(has_solution_goods)==0:
            return mydict    # 没有有效的货物，直接返回
        #########################   得到所有有解货物的信息
        df = df[df['箱子']!='no_solution']
        #########################   根据成本对结果排序
        df = df.sort_values(['good_str', '成本']) 
        if __name__=='__main__':
            try:df.to_excel('test_output/has_solution_goods.xlsx', index=False)
            except:pass

        #########################   箱子名称对应的sto_id
        if len(has_solution_goods)==1:  ############ 只有一个货物时
            if __name__=='__main__':
                print('\ntest111,.........有一个货物时')
            r_dict = dict(zip(cols_list, df.iloc[0]))
            if r_dict.get('bb_num')==1:
                mydict['res_dict'] = {r_dict.get('箱子'):r_dict.get('bb_num')}
                self.msg['求解方案说明'] = "单货物，放法：%s"%r_dict.get('放法')
                return mydict
            if r_dict.get('bb_num')>1:
                mydict = {}
                # print("一种类型货物，需要多个箱子")
                ############### 构造每个箱子最多装的数量
                goods_num = df['整箱'][0]*df['每箱'][0]+df['last箱'][0]
                df_hsl = df[df['放法']=='长长'].sort_values('每箱', ascending=False).reset_index(drop=True)
                first_bin_name = df_hsl['箱子'][0]
                first_bin_num = int(goods_num//df_hsl['每箱'][0])
                # print('first_bin_name,first_bin_num', first_bin_name,first_bin_num)
                last_bin_num = goods_num-first_bin_num*df_hsl['每箱'][0]
                df_x = df[df['每箱']>=last_bin_num]

                df_x=df_x.sort_values('max_L').reset_index(drop=True)
                # print(df_x)
                last_bin_name = df_x['箱子'][0]
                mydict['res_dict'] = {first_bin_name:first_bin_num, last_bin_name:1}
                self.msg['求解方案说明'] = "单货物，放法：最大长长"
                return mydict                



        ##################### 先把多货物，多箱子的方案保存
        rows = []
        appear_list = []
        for i,r in df.iterrows():
            if r['good_str'] not in appear_list:
                appear_list.append(r['good_str'])
                rows.append(r)
        df_min = pd.DataFrame(rows, columns=df.columns)
        if __name__=='__main__':
            try:df_min.to_excel('test_output/df_min_最小成本方案.xlsx', index=False)
            except:pass

         
        multi_container_solution = {}
        for i,r in df_min.iterrows():
            if r['last箱']>0:
                n_i = r['整箱']+1
            else:
                n_i = r['整箱']
            multi_container_solution[r['箱子']] = n_i


        ######################################################################## 开始计算多类型货物  
        '''
        注意：先假设一个箱子就能放下，如果放不下，就返回 multi_container_solution
        '''
        ########### 第一步，找到公共箱子
        able_bins = set(df['箱子'].unique().tolist())
        for goods_i in has_solution_goods:           ##### 循环所有的可行货物，找到他们可行箱子
            bins_i_list = set(df[df['good_str']==goods_i]['箱子'].unique().tolist())
            able_bins = able_bins&bins_i_list
        able_bins = list(able_bins)

        cost_list = []
        for bin_i in able_bins:
            cost_list.append(bins_cost.get(bin_i))
        able_bins_cost_dict = dict(zip(able_bins, cost_list))
        ############ 根据可行箱子从小到大排序
        sort_cost_bins = list(dict(sorted(able_bins_cost_dict.items(), key=lambda item:item[1])).keys())

        if __name__=='__main__':
            print('sort_cost_bins....', sort_cost_bins)
        ####################################################################### 构造空dataFrame，将结果都append
        
        # print('根据成本排序后的箱子交集....', sort_cost_bins)
        df['实际数量'] = df['每箱']*df['整箱']+df['last箱']
        df['总货物体积_L'] = (df['实际数量']*df['l']*df['w']*df['h']/1000)#.round(4)
        # print(has_solution_goods)
        df_not_main_goods = df[df['good_str']!=has_solution_goods[0]].reset_index(drop=True) 

        df = df[df['good_str']==has_solution_goods[0]].reset_index(drop=True)  # 只需要考虑主货物
        df = df.sort_values('总货物体积_L', ascending=False)

        if __name__=='__main__':
            try:df.to_excel('test_output/开始计算多类型货物.xlsx', index=False)
            except:pass

        ###################################################################### 这些货物要放在子空间中
        space_goods_list = has_solution_goods[1:]
        x = df_not_main_goods.drop_duplicates(['good_str'])
        cols_list = x.columns.tolist()
        space_goods_dict = {}
        for i,r in x.iterrows():
            if r['good_str'] in space_goods_list:
                space_goods_dict[r['good_str']]=dict(zip(cols_list, r))
        if __name__=='__main__':
            print('space_goods_dict,这些货物要放在子空间中', space_goods_dict)
        ####################################################################### 循环每个可行的箱子
        
        for bin_i in sort_cost_bins:
            if __name__=='__main__':
                print('正在测试箱子================================================================================================', bin_i)
            df_i = df[(df['箱子']==bin_i)]  # 找到这个箱子
            if df_i.shape[0]==0: # 没找到
                continue
            ########## space_dict(下面根据放法，得到所有的装完主货物后的子空间)
            space_dict = {}  ############################################################ 构造各类剩余空间的字典
            short_nnn = 1  # 实际的空间有损失

            for lay_type in df_i['放法'].unique().tolist():                         # 循环所有可行的放法
                df_ij = df_i[df_i['放法']==lay_type].reset_index(drop=True)         # 得到长长类放法
                goods_str1_dict = dict(zip(df_i.columns, df_i.iloc[0]))             # 这个货物对应的信息（货物已经根据总体积排序了）
                dict_str = json.loads(goods_str1_dict.get('dict_str'))
                if __name__=='__main__':
                    print('lay_type,dict_str===', lay_type,dict_str)
                if '长长' in lay_type:
                    l1 = dict_str['长长数']*dict_str['层数']                         # 每一个横排能放的数量
                    if l1==0:
                        continue
                    if goods_str1_dict['实际数量']%l1==0:
                        n1 = goods_str1_dict['实际数量']//l1
                    else:
                        n1 = goods_str1_dict['实际数量']//l1+1                       # 看看需要几个横排能放完
                    # print('n1.........', n1)
                    last_line_num = dict_str['宽宽数'] - n1
                    # if __name__=='__main__':
                    #     print('长长主货物：{}，每排能放{},实际需要{}排，因为实际数量有{}'.format(has_solution_goods[0], l1, n1, goods_str1_dict['实际数量']))
                    if  last_line_num<0:
                        # print('放不下')
                        continue

                    '''
                    长长放法对应的余量空间
                    -===================================================================== -
                    ------------------------------------------------                       -
                    -               |              |                | ////宽-长余空间////   -
                    -------------------------------------------------                      -
                    ------------------------  -----------------------                      -
                    -               |              |                | ////宽-长余空间////   -
                    -------------------------------------------------                      -
                    -------------------------------------------------                      -
                    -               |  ///主货余空间（余量忽略）///   | ////宽-长余空间////   -
                    ------------------------ ------------------------                      -
                            ///////////长-宽余空间//////////         |                      -
                    ====================================================================== -
                    高余空间:space_h
                    宽长余空间:space_wl
                    长宽余量空间:space_lw
                    主货余空间:space_goods(忽略)

                    算出来这四个空间，把这四个空间，当成分割出来的箱子
                    '''

                    ## 高余空间:space_h
                    # short_nnn = 2  # 实际的空间有损失
                    space_h = [
                        int(dict_str['长长数']*goods_str1_dict['l'])-short_nnn,
                        int(n1*goods_str1_dict['w'])-short_nnn,
                        int(goods_str1_dict['h余量']),
                        ]
                    ## 宽长余空间:space_wl
                    space_wl = [
                        int(goods_str1_dict['箱长'])-short_nnn,
                        int(last_line_num*goods_str1_dict['w']+goods_str1_dict['w余量'])-short_nnn,
                        int(goods_str1_dict['箱高']),
                    ]
                    ## 长宽余量空间:space_lw
                    space_lw = [
                        int(goods_str1_dict['箱宽'])-short_nnn,
                        int(goods_str1_dict['箱长']-dict_str['长长数']*goods_str1_dict['l'])-short_nnn,
                        int(goods_str1_dict['箱高']),
                    ]
                    space_dict[lay_type+'堆'] = {'space_h':space_h, 'space_wl':space_wl, 'space_lw':space_lw}
                    if __name__=='__main__':
                        print('长长堆余空间===', space_dict[lay_type+'堆'])

                    ####################################################################################################### 按层排
                    # if goods_str1_dict['实际数量']%goods_str1_dict['每层']==0:
                    #     n1 = goods_str1_dict['实际数量']//goods_str1_dict['每层']
                    # else:
                    #     n1 = goods_str1_dict['实际数量']//goods_str1_dict['每层']//l1+1                       # 看看需要几个层能放完
                    # if l1==0:
                    #     continue
                    # ### 剩余层数为
                    # n2 = goods_str1_dict['层数']-n1
                    # if  n2<0:
                    #     # print('放不下')
                    #     continue

                    # # print('剩余层数层数', n2)
                    # ##### 主货物的高空间为
                    # space_layer_last_h = [
                    #     goods_str1_dict['箱长']-short_nnn, 
                    #     goods_str1_dict['箱宽']-short_nnn, 
                    #     n2*(goods_str1_dict['h'])+goods_str1_dict['h余量'],
                    # ]
                    # space_dict[lay_type+'层'] = {'space_h':space_layer_last_h}
                    # if __name__=='__main__':
                    #     print('长长层余空间===', space_dict[lay_type+'层'])

                if '长宽' in lay_type:
                    l1 = dict_str['长宽数']*dict_str['层数']                         # 每一个横排能放的数量
                    if l1==0:
                        continue
                    
                    if goods_str1_dict['实际数量']%l1==0:
                        n1 = goods_str1_dict['实际数量']//l1
                    else:
                        n1 = goods_str1_dict['实际数量']//l1+1                       # 看看需要几个横排能放完
                    last_line_num = dict_str['宽长数'] - n1
                    if  last_line_num<0:
                        # print('放不下')
                        continue
                    if __name__=='__main__':
                        print('长宽主货物：{}，每排能放{},实际需要{}排，因为实际数量有{}'.format(has_solution_goods[0], l1, n1, goods_str1_dict['实际数量']))
                    ## 高余空间:space_h
                    
                    space_h = [
                        int(dict_str['长宽数']*goods_str1_dict['l'])-short_nnn,
                        int(n1*goods_str1_dict['w'])-short_nnn,
                        int(goods_str1_dict['h余量']),
                        ]
                    ## 宽长余空间:space_wl
                    space_wl = [
                        int(goods_str1_dict['箱长'])-short_nnn,
                        int(goods_str1_dict['l余量']),
                        int(goods_str1_dict['箱高']),
                    ]
                    ## 长宽余量空间:space_lw
                    space_lw = [
                        int(goods_str1_dict['箱长']-n1*goods_str1_dict['w']-short_nnn),
                        int(dict_str['宽长数']*goods_str1_dict['l'])-short_nnn,
                        int(goods_str1_dict['箱高']),
                    ]
                    space_dict[lay_type+'堆'] = {'space_h':space_h, 'space_wl':space_wl, 'space_lw':space_lw}

                    if __name__=='__main__':
                        print('长宽层堆余空间===', space_dict[lay_type+'堆'])

            if __name__=='__main__':
                print('放法和剩余的空间', space_dict, list(space_goods_dict.keys()))

            for space_name,space_v in space_dict.items():       # 取余空间的类别（每个类别有多组）
                # print(bin_i,' 箱子', space_name, '==>', space_v)
                res_list = [] # 保存解，只要找到解就停止循环了
                df0_cols = ['箱子', '余空间类别','good_str', '余空间名称', '箱长', '箱宽', '箱高', '放法', 'l', 'w', 'h', '每箱', 
                '层数', '每层', '整箱', 'last箱', '余量', 'bb_num', 'l余量', 'w余量', 'h余量']
                df0 = pd.DataFrame([], columns=df0_cols)

                for goods,g_dict in space_goods_dict.items():   # 取某一个货物
                    for sp_k,sp_v in space_v.items():       # 取某一个余空间
                        c_l = sp_v[0]  # 变成厘米
                        c_w = sp_v[1]
                        c_h = sp_v[2]

                        c_max_v = 1000
                        goods_lx = g_dict['l']
                        goods_wx = g_dict['w']
                        goods_hx = g_dict['h']

                        goods_l_real = max(goods_lx,goods_wx)
                        goods_w_real = min(goods_lx,goods_wx)
                        goods_h_real = min(goods_hx,1000000)

                        goods_qty = g_dict['实际数量']
                        # print('正常', goods_lt,goods_wt,goods_ht,goods_l,goods_w,goods_h)
                        list1,list2,list3,dict_str = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l_real,goods_w_real,goods_h_real)

                        # print(k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)
                        if list1[0]!=0:
                            if goods_qty%list1[0]==0:
                                bb_num = goods_qty//list1[0]
                            else:
                                bb_num = goods_qty//list1[0]+1

                            if list3[0]!=0:
                                dict_x = {
                                    '箱子':bin_i,
                                    '余空间类别':space_name,
                                    'good_str':g_dict['good_str'],
                                    '余空间名称':sp_k,

                                    '箱长':c_l,
                                    '箱宽':c_w,
                                    '箱高':c_h,
                                    '放法':'长长',
                                    'l':goods_l_real,
                                    'w':goods_w_real,
                                    'h':goods_h_real,
                                    '每箱':list1[0],
                                    '层数':int(list1[0]/list3[0]),
                                    '每层':int(list3[0]),
                                    '整箱':goods_qty//list1[0], # goods_qty//list1[0]+1,
                                    'last箱':goods_qty%list1[0],
                                    '余量':list1[0]-goods_qty%list1[0],
                                    'bb_num':bb_num,
                                    'l余量':list2[0][0],
                                    'w余量':list2[0][1],
                                    'h余量':list2[0][2],
                                    }
                                # print('l余量...............', list2[0][0], type(list2[0][0]))
                                res_list.append(dict_x)

                        if list1[1]!=0:
                            if goods_qty%list1[1]==0:
                                bb_num = goods_qty//list1[1]
                            else:
                                bb_num = goods_qty//list1[1]+1

                            if list3[1]!=0:                      
                                dict_x = {
                                    '箱子':bin_i,
                                    '余空间类别':space_name,
                                    'good_str':g_dict['good_str'],
                                    '余空间名称':sp_k,
                                    '箱长':c_l,
                                    '箱宽':c_w,
                                    '箱高':c_h,
                                    '放法':'长宽', 
                                    'l':goods_l_real,
                                    'w':goods_w_real,
                                    'h':goods_h_real,                    
                                    '每箱':list1[1],
                                    '层数':int(list1[1]/list3[1]),
                                    '每层':int(list3[1]), 
                                    '整箱':goods_qty//list1[1],
                                    'last箱':goods_qty%list1[1],
                                    '余量':list1[1]-goods_qty%list1[1],
                                    'bb_num':bb_num,
                                    'l余量':list2[1][0],
                                    'w余量':list2[1][1],
                                    'h余量':list2[1][2],
                                    }
                                res_list.append(dict_x)

                        if self.can_reverse==1:
                            ########### 长高倒放，不考虑更复杂旋转
                            goods_l = goods_h_real
                            goods_w = goods_w_real
                            goods_h = goods_l_real
                            # print('长高倒放', goods_lt,goods_wt,goods_ht,goods_h,goods_w,goods_l)
                            list1,list2,list3,dict_str1 = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                            # print('长高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2) 
                            if list1[0]!=0:
                                if goods_qty%list1[0]==0:
                                    bb_num = goods_qty//list1[0]
                                else:
                                    bb_num = goods_qty//list1[0]+1

                                if list3[0]!=0:

                                    dict_x = {
                                        '箱子':bin_i,
                                        '余空间类别':space_name,
                                        'good_str':g_dict['good_str'],
                                        '余空间名称':sp_k,
                                        '箱长':c_l,
                                        '箱宽':c_w,
                                        '箱高':c_h,
                                        '放法':'长长-lh倒',
                                        'l':goods_l,
                                        'w':goods_w,
                                        'h':goods_h,
                                        '每箱':list1[0],
                                        '层数':int(list1[0]/list3[0]),
                                        '每层':int(list3[0]),
                                        '整箱':goods_qty//list1[0], # goods_qty//list1[0]+1,
                                        'last箱':goods_qty%list1[0],
                                        '余量':list1[0]-goods_qty%list1[0],
                                        'bb_num':bb_num,
                                        'l余量':list2[0][0],
                                        'w余量':list2[0][1],
                                        'h余量':list2[0][2],
                                        }
                                    res_list.append(dict_x)

                            if list1[1]!=0:
                                if goods_qty%list1[1]==0:
                                    bb_num = goods_qty//list1[1]
                                else:
                                    bb_num = goods_qty//list1[1]+1

                                if list3[1]!=0:

                                    dict_x = {
                                        '箱子':bin_i,
                                        '余空间类别':space_name,
                                        'good_str':g_dict['good_str'],
                                        '余空间名称':sp_k,
                                        '箱长':c_l,
                                        '箱宽':c_w,
                                        '箱高':c_h,
                                        '放法':'长宽-lh倒',
                                        'l':goods_l,
                                        'w':goods_w,
                                        'h':goods_h,                         
                                        '每箱':list1[1],
                                        '层数':int(list1[1]/list3[1]),
                                        '每层':int(list3[1]), 
                                        '整箱':goods_qty//list1[1],
                                        'last箱':goods_qty%list1[1],
                                        '余量':list1[1]-goods_qty%list1[1],
                                        'bb_num':bb_num,
                                        'l余量':list2[1][0],
                                        'w余量':list2[1][1],
                                        'h余量':list2[1][2],
                                        }
                                    res_list.append(dict_x)

                            ########### 宽高倒放，不考虑更复杂旋转
                            goods_l = goods_l_real
                            goods_w = goods_h_real
                            goods_h = goods_w_real
                            # print('宽高倒放',goods_lt,goods_wt,goods_ht ,goods_h,goods_w,goods_l)
                            list1,list2,list3,dict_str = self.one_goods_one_box_package(c_l,c_w,c_h,c_max_v, goods_qty,goods_l,goods_w,goods_h)
                            # print('宽高倒放=======>', k, '两种方法的数量对比===>', list1,'长长剩余VS宽长剩余===>', list2)    
                            if list1[0]!=0:
                                if goods_qty%list1[0]==0:
                                    bb_num = goods_qty//list1[0]
                                else:
                                    bb_num = goods_qty//list1[0]+1
                                if list3[0]!=0:
                                    dict_x = {
                                        '箱子':bin_i,
                                        '余空间类别':space_name,
                                        'good_str':g_dict['good_str'],
                                        '余空间名称':sp_k,
                                        '箱长':c_l,
                                        '箱宽':c_w,
                                        '箱高':c_h,
                                        '放法':'长长-wh倒',
                                        'l':goods_l,
                                        'w':goods_w,
                                        'h':goods_h,
                                        '每箱':list1[0],
                                        '层数':int(list1[0]/list3[0]),
                                        '每层':int(list3[0]),
                                        '整箱':goods_qty//list1[0], # goods_qty//list1[0]+1,
                                        'last箱':goods_qty%list1[0],
                                        '余量':list1[0]-goods_qty%list1[0],
                                        'bb_num':bb_num,
                                        'l余量':list2[0][0],
                                        'w余量':list2[0][1],
                                        'h余量':list2[0][2],
                                        }
                                    res_list.append(dict_x)
                            
                            if list1[1]!=0:
                                if goods_qty%list1[1]==0:
                                    bb_num = goods_qty//list1[1]
                                else:
                                    bb_num = goods_qty//list1[1]+1
                                if list3[1]!=0:                                            
                                    dict_x = {
                                        '箱子':bin_i,
                                        '余空间类别':space_name,
                                        'good_str':g_dict['good_str'],
                                        '余空间名称':sp_k,
                                        '箱长':c_l,
                                        '箱宽':c_w,
                                        '箱高':c_h,
                                        '放法':'长宽-wh倒',
                                        'l':goods_l,
                                        'w':goods_w,
                                        'h':goods_h,                        
                                        '每箱':list1[1],
                                        '层数':int(list1[1]/list3[1]),
                                        '每层':int(list3[1]), 
                                        '整箱':goods_qty//list1[1],
                                        'last箱':goods_qty%list1[1],
                                        '余量':list1[1]-goods_qty%list1[1],
                                        'bb_num':bb_num,
                                        'l余量':list2[1][0],
                                        'w余量':list2[1][1],
                                        'h余量':list2[1][2],
                                        }
                                    res_list.append(dict_x)                        
                df_res_list = pd.DataFrame(res_list)
                ####### 其中一个解
                df0 = df0.append(df_res_list)
                df0 = df0[df0['每箱']>0].reset_index(drop=True)
                ######## 第一步保存每个余空间能够放的各个货物的最大值
                goods_num_dict_decrease = {}
                for goods,g_dict in space_goods_dict.items():
                    goods_num_dict_decrease[goods] = g_dict.get('实际数量')
                # print('goods_num_dict_decrease....', goods_num_dict_decrease)
                max_v_list = []
                for sp_k in df0['余空间名称'].unique().tolist():
                    for goods,g_dict in space_goods_dict.items():
                        max_v = df0[(df0['余空间名称']==sp_k)&(df0['good_str']==goods)]['每箱'].max()
                        max_v_list.append([sp_k, goods, max_v])

                # print('max_v_list......', max_v_list)
                max_v_dict = {}
                for max_v in max_v_list:
                    if max_v[1] not in max_v_dict:
                        max_v_dict[max_v[1]] = max_v[2]
                    else:
                        max_v_dict[max_v[1]] += max_v[2]
                # print('max_v_dict', max_v_dict)

                '''
                goods_num_dict_decrease.... {'20==>6*6*11.5': 22, '20==>12.5*3.0*7.5': 22}
                max_v_list = [
                ['space_h', '20==>6*6*11.5', 60], 
                ['space_h', '20==>12.5*3.0*7.5', 96], 
                ['space_lw', '20==>6*6*11.5', 50], 
                ['space_lw', '20==>12.5*3.0*7.5', 88]]
                
                max_v_dict = 
                {'20==>6*6*11.5': 110, '20==>12.5*3.0*7.5': 184}
                '''

                current_vol_p = 0
                # if __name__=='__main__':
                #     print('bin____xxx_______goods_num_dict_decrease',goods_num_dict_decrease)                
                for k,v in goods_num_dict_decrease.items():
                    if k in max_v_dict:
                        # print('v,max_v_dict[k]...k',k, v, max_v_dict[k])
                        current_vol_p += v/max_v_dict[k]
                    else:
                        current_vol_p += 1.1  # 如果不存在直接加满
                # if __name__=='__main__':
                #     print('bin___________current_vol_p', bin_i, current_vol_p)
                if self.goods_type_num==2:  # 只有两个货物
                    if current_vol_p<=1:
                        mydict['res_dict'] = {bin_i:1}
                        self.msg['求解方案说明'] = "主货物:%s,余空间类别:%s"%(has_solution_goods[0], space_name)
                        return mydict

                if current_vol_p<0.8:
                    mydict['res_dict'] = {bin_i:1}
                    self.msg['求解方案说明'] = "主货物:%s,余空间类别:%s"%(has_solution_goods[0], space_name)
                    return mydict

                if __name__=='__main__':
                    try:df0.to_excel('test_output/某一个箱子的结果.xlsx', index=False)
                    except:print('保存错误1168')


        ############ 单个箱子已经不够
        self.msg['求解方案说明']='多类型货物，单箱子装不下,需要后期优化'
        mydict['res_dict'] = {}
        return mydict


    # @log_func_time
    def run(self):
        #################################################################### 输入检查和m+状态和信息的获取
        self.check_goods_str()
        if not self.right_state:
            res = {'msg':self.msg}
            if __name__=='__main__':
                print('最终的结果出来了................', res_dict)
            return res

        self.m_state,self.m_bins_list = self.check_m_plus() 
        # if __name__=='__main__':
        #     print('m+状态和m+箱型',self.m_state,self.m_bins_list)
        #################################################################### 只有一种类型的货物
        res = self.solution_list()

        ############ 重新整理结果
        '''
        res_dict:{
        "no_solution_goods":[],
        "res_dict":{"VIP6N保温箱":1},
        "res_str":"VIP6N保温箱*1",
        "res_for_bussiness":{"plan1":[{"sto_id":"200648",
        "sto_name":"VIP6N保温箱","num":"1"}]},
        "msg":{"check_goods_str":[]}}}',
        '''
        res_dict = {}
        if res is None:
            res_dict['msg'] = self.msg
            res_dict['goods_dict'] = self.goods_dict
            # print(res_dict)
            res = {}

        bin_shape_dict =self.container_info['bin_shape']
        if res.get('res_dict') is not None:
            res_dict['no_solution_goods'] = res.get('no_solution_goods')
            res_dict['res_dict'] = res.get('res_dict')
            res_dict['msg'] = self.msg

            dict1 = {}
            res_str = ''
            bin_list = []
            for k,v in res.get('res_dict').items():
                res_for_bussiness = {}
                dict1[k] = v
                res_str += '%s*%s,'%(str(k), str(v))
                res_for_bussiness['sto_id'] = str(self.container_sto_id.get(k))
                res_for_bussiness['sto_name'] = k
                res_for_bussiness['num'] = str(v)
                res_for_bussiness['bin_shape'] = bin_shape_dict.get(k)
                bin_list.append(res_for_bussiness)


            res_dict['res_str'] = res_str.rstrip(',')
            res_dict['res_for_bussiness']={'plan1':bin_list}

        if __name__=='__main__':
            print('最终的结果出来了................', res_dict)
        return res_dict





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
        'goods_str':'1070==>12*8*2;',    # 货物字符串,长度单位是里面（参考数据库）
    }

    goods_dict = {

        ####### 判断是否是M+
        'start_region_id':310000,      # start, end region id用来找M+
        'end_region_id':130600,
        'omc_time':'2022-02-14',        # 开始结束日期找M+

        'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
        'specail_type_str':'',         # 用来判断，可行箱子肯定性条件，空就没有要求

        ####### 温度可行箱子判断
        'omc_tem_id':'31',              # 温度id

        ####### 货物和订单属性
        'can_reverse':1,                # 1可以倒放, 空则0
        'goods_str':'2==>7.5*8.0*5.5;',    # 货物字符串,长度单位是里面（参考数据库）
    }

    '''
    20|6.0*6.0*11.5____ 20|12.5*3.0*7.5
    计算:1*VIP16保温箱;1*VIP28保温箱
    实际:1*VIP36保温箱
    计划:1*VIP36保温箱
    '''

    ########## 2月24日 62354581
    goods_dict = {
    'start_region_id': 310000,  # start, end region id用来找M+
    'end_region_id': 320500, 
    'omc_time': '2020-12-14', 

    'route_type': -1,           # 用来判断路由否定的箱型
    'specail_type_str': '',     # 可行箱子特殊条件，空就没有要求
    'omc_tem_id': '31',         # 温度id
    'can_reverse': 0,           # 是否可以倒放
    'goods_str': '2==>16.0*11.5*5.5;1==>16.0*12.0*6.0',   # 货物尺寸20个6*6*11.5, ...
    'is_fragile': 0             # 是否是易碎品
    }

    ################################## M+测试
    goods_dict = {
    'start_region_id': 130600,  # start, end region id用来找M+
    'end_region_id': 140300, 
    'omc_time': '2022-01-28', 

    'route_type': -1,           # 用来判断路由否定的箱型
    'specail_type_str': '',     # 可行箱子特殊条件，空就没有要求
    'omc_tem_id': '31',         # 温度id
    'can_reverse': 0,           # 是否可以倒放
    'goods_str': '20==>19.0*18.5*16.0',   # 货物尺寸20个6*6*11.5, ...
    'is_fragile': 0             # 是否是易碎品
    }

    goods_dict = {"start_region_id":130600,"end_region_id":140300,"omc_time":"2022-01-28","route_type":-1,
    "specail_type_str":"","omc_tem_id":"31","can_reverse":0,"goods_str":"20==>19.0*18.5*16.0","is_fragile":0,"cp_id":"2920"}
    '''    
    26|16.0*12.0*6.0____ 10|16.0*12.0*6.0
    计算:2*VIP56保温箱
    实际:1*VIP56保温箱
    计划:1*VIP56保温箱
    '''
    # goods_dict = {'start_region_id': 310000, 'end_region_id': 320500, 'omc_time': '2020-12-14', 'route_type': -1, 
    # 'specail_type_str': '', 'omc_tem_id': '31', 'can_reverse': 1, 'goods_str': '26==>16.0*12.0*6.0;10==>16.0*12.0*6.0', 'is_fragile': 0}
    

    '''
    9|15.0*11.5*7.5
    计算:1*VIP28保温箱
    实际:1*VIP36保温箱
    计划:1*VIP36保温箱

    297*297*295VS374*297*295
    2022-02-18||62664158||22||1590484|| RX518 胶囊/模拟胶囊+吉非替尼片/模拟片

    '''

    # goods_dict = {
    # 'start_region_id': 310000,  # start, end region id用来找M+
    # 'end_region_id': 320500, 
    # 'omc_time': '2020-12-14', 

    # 'route_type': -1,           # 用来判断路由否定的箱型
    # 'specail_type_str': '',     # 可行箱子特殊条件，空就没有要求
    # 'omc_tem_id': '31',         # 温度id
    # 'can_reverse': 1,           # 是否可以倒放
    # 'goods_str': '9==>15.0*11.5*7.5;',   # 货物尺寸20个6*6*11.5, ...
    # 'is_fragile': 0             # 是否是易碎品
    # }


    # goods_dict = {

    #     ####### 判断是否是M+
    #     'start_region_id':140100,      # start, end region id用来找M+
    #     'end_region_id':140300,
    #     'omc_time':'2021-08-23',        # 开始结束日期找M+

    #     'route_type':1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
    #     'specail_type_str':'',         # 用来判断，可行箱子肯定性条件，空就没有要求

    #     ####### 温度可行箱子判断
    #     'omc_tem_id':'61',              # 温度id

    #     ####### 货物和订单属性
    #     'can_reverse':1,                # 1可以倒放, 空则0
    #     'goods_str':'3==>13*30*10;10==>12*7*2;10==>120*70*2;',    # 货物字符串,长度单位是里面（参考数据库）
    # }



    '''
    sto_id: 
    返回：'VIP168*2,VIP3*3'
    '''
    OneContainerOneItemSolution(goods_dict).run()

