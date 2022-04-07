
import sys
sys.path.append('..')

import os
import json
import config
import pandas as pd
from myutils.func_decorated import log_func_time
import algori_bin.s33_multi_container as arcoi

# @log_func_time
def one_type_item_one_type_container(multi_goods_dict, temp_container_dict):    # 将不同的货物放入最合适的container中，然后再考虑合并
    multi_goods_str = multi_goods_dict['goods_str'].rstrip(';')
    goods_str_list = multi_goods_str.split(';')
    # print(goods_str_list)
    item_container_list = []
    for goods_str in goods_str_list:
        goods_dict = multi_goods_dict
        goods_dict['goods_str']=goods_str # 构造goods_dict
        item_plan = arcoi.select_best_container(goods_dict, temp_container_dict)

        item_container_list.append(item_plan)

    # print(item_container_list)
    ############### 步骤一，每个货物用到的箱子减1
    container_need_dict = {}
    for item_plan in item_container_list:
        if item_plan.get('箱子'):

            if item_plan['箱子'] not in container_need_dict.keys():
                container_need_dict[item_plan['箱子']] = item_plan['箱子数(n+1)']-1
            else:
                container_need_dict[item_plan['箱子']] += item_plan['箱子数(n+1)']-1
            item_plan.pop('箱子数(n+1)')
    # print('================取整的箱子')
    # print(container_need_dict)
    # print('\n================待合并的箱子,重新梳理信息')
    rows = []
    for item_plan in item_container_list:
        if item_plan.get('箱子'):
            l,w,h=[int(x) for x in item_plan['货物'].split('==>')[1].split('*')]
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
    # df.to_excel('test2.xlsx', index=False)

    ############### 步骤二，选择可选箱型最少的那个货物作为主箱子，如果都一样多，那么选择单个货物体积最大的作为主箱子
    # print('================取整的箱子')
    # print(container_need_dict)
    if df.shape[0]==0:  # 没找到解
        return {}

    sum_vol = df['货物总体积_L'].sum()
    can_reverse = multi_goods_dict.get('can_reverse')
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
        if can_reverse==0 and 0.6*sum_container_vol>sum_vol and df['可选箱型数量'][i]>1:
            break

        sum_container_vol += df['箱子最大容积_L'][i]
        if df['箱型'][i] in container_exists_list:
            container_need_dict[df['箱型'][i]] += 1
        else:
            container_need_dict[df['箱型'][i]] = 1

        # print(temp_container_dict.get(df['箱型'][i]))
    
    # print(container_need_dict)
    res_dict = {}
    for k,v in container_need_dict.items():
        if v!=0:
            res_dict[k] = v
    print('================最终选的箱子', res_dict)
    return res_dict


def get_space_free_space_after_package_goods_str(container_name, ):
    goods_dict={
        'temp_type':'-20',              # 温区
        'goods_str':'1==>19*9*44;',     # 货物字符串
        'can_reverse':0                 # 1可以倒放
    }
    pass



if __name__=='__main__':

    multi_goods_dict={
        'temp_type':'B20',              # 温区
        'goods_str':'1000==>14*6*5;',     # 货物字符串
        'can_reverse':0,                 # 1可以倒放
        'must_accept_bins':[]      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    }

    multi_goods_dict={
        'temp_type':'0',              # 温区
        'goods_str':'12==>5*5*7;6==>3*3*6;',     # 货物字符串
        'can_reverse':0,                 # 1可以倒放
        'must_accept_bins':['PBX-EP46__EP46泡沫箱', 'PBX-EP133__EP133泡沫箱']      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    }

    # multi_goods_dict={
    #     'temp_type':'B20',              # 温区
    #     'goods_str':'26==>13*6*2;1==>14*6*5;10==>14*6*5;2==>9*9*4;10==>12*7*2;',     # 货物字符串
    #     'can_reverse':0,                 # 1可以倒放
    #     'must_accept_bins':['PBX-EP78__EP78泡沫箱']      ## 默认都接受，但是如果出现限制条件就只能在限制箱子中选择
    # }
    f_path = os.path.join(config.ROOT_PATH, 'data/bin/container_info.json')
    temp_container_dict = json.load(open(f_path, "rb")) # 参考json中的数据结构
    one_type_item_one_type_container(multi_goods_dict,temp_container_dict)

