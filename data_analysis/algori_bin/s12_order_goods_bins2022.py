#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append('../..')
import os
import json
import config
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pylab as pl
from algorithms.algori_bin import s41_one_container_one_item as as41coi
from algorithms.algori_bin import s42_algori_bin_ver3 as as42ver

plt.switch_backend('agg')
plt.rcParams['font.sans-serif'] = ['SimHei']                        # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                          # 用来正常显示负号
mydict = {}


# In[2]:


myname = 's12_order_goods_bins2022.py' ########## 这里要修改城文件名
df = pd.read_excel(os.path.join(config.ROOT_PATH, 'data_analysis/说明.xlsx'))
df = df[df['code_name']==myname]
res_dict = dict(zip(df.columns, df.iloc[0]))
res_path = os.path.join(config.f_path['data_analysis_res'], '%s/%s'%(res_dict['res_folder'], res_dict['res_file']))
if os.path.exists(res_path) is False:os.makedirs(res_path)
f2 = open(os.path.join(res_path,config.img_pretext), 'w', encoding='utf-8')


# In[3]:


f_path = os.path.join(config.f_path['kudu_table_pickle'], 'order_goods.pickle')
df = pd.read_pickle(f_path)
s1 = df.shape[0]
df = df.fillna(0)
'''
og_long	长（厘米）
og_width	宽（厘米）
og_height	高（厘米）
og_quantity	数量

'''

df = df[(df['og_long']!=0)&(df['og_width']!=0)&(df['og_height']!=0)&(df['og_quantity']!=0)].reset_index(drop=True)
df['shape_str'] = df['og_quantity'].astype(int).astype(str)+'==>'+df['og_long'].astype(str)+'*'+df['og_width'].astype(str)+'*'+df['og_height'].astype(str)
has_lwh_percent = str(round(100*df.shape[0]/s1, 2))+'%'

mydict['具有长宽高的货物占比'] = has_lwh_percent
mydict['shape_str示例'] = df['shape_str'][:3]
print(mydict)


# In[4]:


df['单个货物体积'] = df['og_long'].astype(float)*df['og_width'].astype(float)*df['og_height'].astype(float)/1000
t_dict = {
    '货物体积类别':len(df['单个货物体积'].unique().tolist()),
    '单个货物的平均体积（L）':df['单个货物体积'].mean().round(4),
    '单个货物的最大体积（L）':df['单个货物体积'].max().round(4),
    '单个货物的最小体积（L）':df['单个货物体积'].min().round(4),
}

mydict['货物体积信息'] = t_dict
print(t_dict)


# In[5]:


df_big_vol = df[df['单个货物体积']>5000].reset_index(drop=True)
str1 = ''
for g in df_big_vol.groupby('单个货物体积'):
    # og_name	货物名称
    pstr = '体积（L）：%s'%str(g[0])+'==>对应货物(首个)：%s'%str(g[1]['og_name'].tolist()[:10])
    str1 += pstr+'\n'
    print(pstr)
mydict['大尺寸货物示例(脏数据？)'] = str1


# In[6]:


fname = '01货物尺寸体积比例'
vol_list = [0.001,0.1,1,2,3,4,5,10,15,30,60]
num_p_list = []
rows = []
for vol in vol_list:
    df_small_vol = df[df['单个货物体积']<=vol].reset_index(drop=True)
    percent_i = round(df_small_vol.shape[0]/df.shape[0],3)
    vol_small_L = percent_i
    num_p_list.append(vol_small_L)
    rows.append([vol, percent_i])
dft = pd.DataFrame(rows, columns='体积L,货物占比'.split(","))
dft.to_excel(os.path.join(res_path, '%s.xlsx'%fname), index=False)
#     print('尺寸小于%sL的货物数量占比:'%str(vol), vol_small_L)

plt.plot(vol_list, num_p_list)
plt.scatter(vol_list, num_p_list)
break_xy = (0,0)
for xy in zip(vol_list, num_p_list):
    if xy[1]>=0.95:
        plt.annotate("(%s,%s)" % xy, xy=xy, xytext=(-20, 10), textcoords='offset points', 
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.5))
        break_xy = xy
        break
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('参考图中货物尺寸的信息，为了清晰脏数据首先分析当货物的体积大于多少时就不再考虑', file=fp)
    x1 = break_xy[1]*100
    x2 = break_xy[0]
    print('{0}%的货物体积小于{1}L,下面仅考虑体积小于{1}L的货物'.format(x1,x2),file=fp)


# In[7]:


df = df[df['单个货物体积']<x2].reset_index(drop=True)
rows = []
# to_id	运输单序号
# og_name	货物名称

for g in df.groupby('to_id'):
    dispatch_id = g[0]
    dispatch_df = g[1]
    xg1 = dispatch_df['og_name'].tolist()
#     print(xg1)
    rows_i = [dispatch_id, ';'.join(dispatch_df['shape_str']), dispatch_df.shape[0],xg1[0]]
    rows.append(rows_i)

df_dispatch = pd.DataFrame(rows, columns='to_id,shape_str,货物类型数,货物名称'.split(',')).sort_values('货物类型数',ascending=False)
# df_dispatch = df_dispatch[df_dispatch['货物类型数']<6]
# df_dispatch.to_excel(os.path.join(config.ROOT_PATH, 'test.xlsx'), index=False)
order_mean_goods_type_num = str(round(df.shape[0]/df_dispatch.shape[0], 2))
mydict['平均每单货物的货物类型数量'] = order_mean_goods_type_num


# In[8]:


fname = '02货物类型数量出现频率'
df_dispatch_g = df_dispatch.groupby('货物类型数')
rows = []
for g in df_dispatch_g:
    row_i = [g[0], g[1].shape[0]]
    rows.append(row_i)
    
df_p = pd.DataFrame(rows, columns='货物类型数,出现次数'.split(','))
df_p.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)
df_p.index=df_p['货物类型数']
df_p = df_p[['出现次数']]
df_p.plot.bar()
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('下面仅分析货物类型数小于6次的运单,dispatch_df示例如下，下面考虑关联运单的其他属性', file=fp)
    df_dispatch = df_dispatch[df_dispatch['货物类型数']<6].reset_index(drop=True)
    print(df_dispatch[:5], file=fp)
    
f_path = os.path.join(config.f_path['kudu_table_pickle'], 'transport_order.pickle')
df_order = pd.read_pickle(f_path)
print(df_order.shape)


# In[10]:


col_s = [
    'to_no',# 纸质运单编号
    'to_id',# '运输单序号',
    'cu_id',#'委托客户序号',
    'cp_id',#'项目序号',
    'to_temperature',#'运输温度,1 CW0-30,2 HW15-25,3 HW18-30,4 LB2-8,5 GB-20,6 YD-150',
    'start_region_id',#'发件所在地区ID',
    'stop_region_id',#'收件所在地区ID',
    'to_createtime',#'创建时间',
    'to_remark',#'客户备注',
    'to_goodstype',# '货物类型（1=血样,2=样本,3=药品）'
]

df_order = df_order[col_s]
df_order['cu_id'] = df_order['cu_id'].fillna(-1).astype(int).astype(str)
df_order['cp_id'] = df_order['cp_id'].fillna(-1).astype(int).astype(str)

print(df_order.shape)
print('dict(df_order.iloc[0]).....', dict(df_order.iloc[0]))



df_dispatch = pd.merge(df_dispatch, df_order, on='to_id', how='left')
df_dispatch['to_createtime']=pd.to_datetime(df_dispatch['to_createtime'].values, unit='s', utc=True).tz_convert('Asia/Shanghai').strftime("%Y-%m-%d")
df_dispatch = df_dispatch[df_dispatch['to_createtime']>='2022-01-01'].reset_index(drop=True)


# In[11]:




cn_list = []
id_list = []
solution_plan_list = []
df_dispatch.fillna(0, inplace=True)
# test_str = 1578712  # 运输单序号，测试用
# df_iter =  df_dispatch[df_dispatch['to_id']==test_str].reset_index(drop=True)

df_iter = df_dispatch
for i,r in df_iter.iterrows():
    goods_dict = {
        ####### 判断是否是M+
        "thermometer_num":1,
        "cu_id": str(r['cu_id']),  # 客户编号
        "cp_id":  str(r['cp_id']),          # 项目编号
        "goods_name": r['货物名称'],  # 货物名称 

        'start_region_id':int(r['start_region_id']),      # start, end region id用来找M+
        'end_region_id':int(r['stop_region_id']),
        'omc_time':r['to_createtime'],        # 开始结束日期找M+
        'route_type':-1,                 # 用来判断路由否定的箱型，可行箱子否定性条件，空就没有要求
        'specail_type_str':'',         # 用来判断，可行箱子肯定性条件，空就没有要求
        ####### 温度可行箱子判断
        'omc_tem_id':int(r['to_temperature']),              # 温度id
        ####### 货物和订单属性
        'can_reverse':0,                # 1可以倒放, 空则0
        'goods_str':r['shape_str'],    # 货物字符串,长度单位是里面（参考数据库）
    }    

    ################# 算法1
    # A = as41coi.OneContainerOneItemSolution(goods_dict)
    # res = A.multi_container_multi_item()

    ################# 算法2
    A = as42ver.OneContainerOneItemSolution(goods_dict)
    res = A.run()

#     print(res)


    
    res_cn = ''
    res_id = ''
    solution_plan = ''
    if res.get('res_str') is not None:
        # res_cn = str(res.get('res_str')).replace(',',';')
        res_id = ''
        res_cn = ''
        for j in res.get('res_for_bussiness').get('plan1'):
            res_id +=str(j.get('num'))+'*'+str(j.get('sto_id'))+';'
            res_cn +=str(j.get('num'))+'*'+str(j.get('sto_name'))+';'
        res_id = res_id.rstrip(';')
        res_cn = res_cn.rstrip(';')
        solution_plan = res['msg'].get('求解方案说明')
    cn_list.append(res_cn)
    id_list.append(res_id)
    solution_plan_list.append(solution_plan)

df_dispatch['计算箱型cn'] = cn_list
df_dispatch['计算箱型id'] = id_list
df_dispatch['求解方案'] = solution_plan_list

# In[12]:
print(df_dispatch.columns.tolist())
df_dispatch['to_createtime'] = df_dispatch['to_createtime'].astype('str')
df_dispatch = df_dispatch.sort_values('to_createtime', ascending=False)
rename_dict = {
    'to_id':'运输单序号', 
    'shape_str':'shape_str', 
    '货物类型数':'货物类型数', 
    '货物名称':'货物名称', 
    'to_no':'纸质运单编号', 
    'cu_id':'委托客户序号', 
    'cp_id':'项目序号', 
    'to_temperature':'运输温度', 
    'start_region_id':'发件所在地区ID', 
    'stop_region_id':'收件所在地区ID', 
    'to_createtime':'创建时间', 
    'to_remark':'客户备注', 
    'to_goodstype':'货物类型', 
    '计算箱型cn':'计算箱型cn', 
    '计算箱型id':'计算箱型id',
    '求解方案':'求解方案'
    
}

df_dispatch.rename(columns=rename_dict,inplace=True)
df_dispatch.to_excel(os.path.join(config.f_path['data_excel'], 'bin_存在尺寸的运单2022.xlsx'), index=False)

# In[13]:


fname = '03存在货物尺寸的客户'
df_p = pd.pivot_table(df_dispatch,index='委托客户序号',values=['运输单序号'] , aggfunc = 'count')
df_p = df_p.sort_values('运输单序号', ascending=False)
df_p.columns = ['运单数量']
x1 = df_p[df_p['运单数量']<=100].shape[0]
x2 = df_p[df_p['运单数量']<=100]['运单数量'].sum().round()
df_p.index = [int(x) for x in df_p.index]

df_p = df_p[df_p['运单数量']>100]
custormer_str_list = [int(x) for x in df_p.index]
print('custormer_str_list....', custormer_str_list)

df_p.plot.bar()
df_p.insert(0,'客户编号',df_p.index)
df_p.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('分析哪些客户会填写货物尺寸,注意只考虑运单数量超过100的客户', file=fp)
    print('数量小于100的客户有{0}个，总共有{1}个订单'.format(x1,x2), file=fp)
print(df_p.head(3), type(df_p))

# result1 = pd.pivot_table(data,index='洲' , values = ['销售额','利润'] , aggfunc = np.sum)
# result1.head()


# In[14]:


fname = '04对比温度config_id'

xcol = '运输温度'
ycol = '委托客户序号'
count_col = '运输单序号'
df_p = pd.pivot_table(df_dispatch,index=[xcol],
                      columns=[ycol],
                      values=[count_col], aggfunc = 'count').fillna(0) # , aggfunc = 'count'
list1 = [int(x) for x in df_p.index.tolist()]  # 温度config_id
list2 = [int(x[1]) for x in df_p.T.index.tolist()]
print(list1)
print(list2)
df_p = df_p.T.reset_index(drop=True).T
df_p.index = list1
df_p.columns = list2
print(list2)
print(custormer_str_list)
df_p = df_p[custormer_str_list]

df_p.plot.barh(stacked=True)
plt.ylabel('温度config_id')
plt.xlabel('运单数量')
plt.legend(bbox_to_anchor=(1.005, 0), loc=3, borderaxespad=0, frameon=False)
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

df_p.insert(0,'温度config_id',df_p.index)
df_p.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)

# with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
#     print('分析哪些温区会填写货物尺寸,注意只考虑运单数量超过100的温区', file=fp)
#     print('数量小于100的温区有{0}个，总共有{1}个订单'.format(x1,x2), file=fp)
# print(df_p.head(3), type(df_p))


# In[15]:


for k,v in mydict.items():
    print('*'*50, k, file=f2)
    print(v, file=f2)
    
f2.close()
plt.close()

