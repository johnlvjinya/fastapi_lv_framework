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
plt.rcParams['font.sans-serif'] = ['SimHei']                        # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                          # 用来正常显示负号

myname = 's01_basic_info_plt.py' ########## 这里要修改城文件名
df = pd.read_excel(os.path.join(config.ROOT_PATH, 'data_analysis/说明.xlsx'))
df = df[df['code_name']==myname]
res_dict = dict(zip(df.columns, df.iloc[0]))
res_path = os.path.join(config.f_path['data_analysis_res'], '%s/%s'%(res_dict['res_folder'], res_dict['res_file']))
if os.path.exists(res_path) is False:os.makedirs(res_path)
f2 = open(os.path.join(res_path,config.img_pretext), 'w', encoding='utf-8')
mydict = {}

################## 获取所有的站点信息
p_dict = {
    'route_db_region_connection_list':os.path.join(config.f_path['data_json'], 'route_db_region_connection_list.json'),
    'route_real_region_connection_list':os.path.join(config.f_path['data_json'], 'route_exists_real_route_list.json'),
    'route_region_lon_lat_dict':os.path.join(config.f_path['data_json'], 'route_region_lon_lat_dict.json'),
    'route_type':os.path.join(config.f_path['data_json'], 'route_type.json'),
}

j_dict = {}
for k,v in p_dict.items():
    with open(v, 'r', encoding='utf8')as fp: j_dict[k] =json.load(fp)  
print(j_dict['route_type'])


# In[3]:



fname = '01路由节点的分布'
rows = []
for k,v in j_dict['route_region_lon_lat_dict'].items():
    rows.append([k, v['地区名'],v['经度'],v['纬度']])
df = pd.DataFrame(rows, columns='地区ID,地区名,经度,纬度'.split(','))
plt.scatter(df['经度'],df['纬度'], alpha=0.3, cmap='viridis')
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

df.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)
with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('历史数据种出现的路由节点的分布', file=fp)




############################################# 地区的id对应的中文名
region_id_cn_dict = dict(zip(df['地区ID'].astype(int), df['地区名']))
region_cn_id_dict = dict(zip(df['地区名'], df['地区ID'].astype(int)))




# In[4]:


fname = '02路由连接的频次排序'

rows = []
for k,v in j_dict['route_real_region_connection_list'].items():
    # print(v)
    s_region_name = region_id_cn_dict.get(v['start_id'])
    e_region_name = region_id_cn_dict.get(v['end_id'])
    if s_region_name is None:
        s_region_name = v['start_id']
    if e_region_name is None:
        e_region_name = v['end_id']
    if len(list(v['route_time_dict'].keys()))>0:
        x = list(v['route_time_dict'].keys())[0]
    else:
        x = ''
    row_i = [s_region_name,e_region_name,v['order_num'],x]
    rows.append(row_i)

df = pd.DataFrame(rows, columns='出港地区,到港地区,order_num,跑过的路由类型'.split(','))
df = df[df['出港地区']!=-1]
df = df.sort_values('order_num', ascending=False).reset_index(drop=True)
# df['order_num'].plot()
plt.plot(df.index,df['order_num'])
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

df.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)
with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('出港和到港路由频次排序', file=fp)


# In[5]:


fname = '03到港非济南，前50名路由连接'
df2 = df[df['到港地区']!='济南市'].reset_index(drop=True)
N = min(50, df2.shape[0])
df1 = df2[:N]
# df['order_num'].plot()
plt.bar(df1.index,df1['order_num'])
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

df1.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)
with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('出港和到港路由频次排序', file=fp)


# In[6]:


fname = '04路由连接频次统计'
vol_list = [10,20,30,50,100,200,350,500,750,1000]
num_p_list = []
rows = []
for vol in vol_list:
    df_small_vol = df[df['order_num']<=vol].reset_index(drop=True)
    percent_i = round(df_small_vol.shape[0]/df.shape[0],3)
    vol_small_L = percent_i
    num_p_list.append(vol_small_L)
    rows.append([vol, percent_i])
dft = pd.DataFrame(rows, columns='连接小于此数量,节点连接占比'.split(","))
dft['连接小于此数量'] = dft['连接小于此数量'].astype(int)
dft.to_excel(os.path.join(res_path, '%s.xlsx'%fname), index=False)
#     print('尺寸小于%sL的货物数量占比:'%str(vol), vol_small_L)

plt.plot(vol_list, num_p_list)
plt.scatter(vol_list, num_p_list)
break_xy = (0,0)
for xy in zip(vol_list, num_p_list):
    if xy[1]>=0.8:
        plt.annotate("(%s,%s)" % xy, xy=xy, xytext=(-20, 10), textcoords='offset points', 
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', ec='k', lw=1, alpha=0.5))
        break_xy = xy
    else:
        plt.annotate("(%s,%s)" % xy, xy=xy, xytext=(-20, 10), textcoords='offset points', 
                     bbox=dict(boxstyle='round,pad=0.5', fc='green', ec='k', lw=1, alpha=0.5))
        break_xy = xy        
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('路由连接频次统计', file=fp)


# In[7]:


df3 = pd.read_pickle(os.path.join(config.f_path['data_clean_pickle'], 'route_order_info_merge.pickle'))
for col in df3.columns.tolist():
    print(col,'=========>', df3[col].dtypes)


# In[8]:


#### 选择跟订单相关的列分析
order_col_list = [
    'order_to_id',
    'order_cu_id',
    'order_to_timelimit',
    'order_to_temperature',
    'order_start_region_id',
    'order_stop_region_id',
    'order_to_status',
    'order_logistics_取派时间差(天)',
    'order_星期几',
    'order_年份',
    'order_小时',
    'order_12点前取件',
    'order_17点前取件',    

]
order_df = df3[order_col_list]
print(order_df.shape)
order_df = order_df.drop_duplicates()
print(order_df.shape)
timelimit_dict = {
    0:'12小时',
    1:'24小时',
    2:'36小时',
    3:'48小时',
    4:'t52小时'
}
order_df = order_df.sort_values('order_to_timelimit').reset_index(drop=True)
order_df['order_to_timelimit']=order_df['order_to_timelimit'].map(timelimit_dict)  # 保存所有箱子的信息


# In[9]:


x1 = order_df[order_df['order_logistics_取派时间差(天)']<0].shape[0]
y1 = round(100*x1/order_df.shape[0],4)

mydict['脏数据,取派时间差小于0'] = '共{0}条, 占比{0}(%)'.format(x1,y1)

x2 = order_df[order_df['order_logistics_取派时间差(天)']>10].shape[0]
y2 = round(100*x2/order_df.shape[0],4)
mydict['脏数据,取派时间差大于10天'] = '共{0}条, 占比{1}(%)'.format(x2,y2)

x3 = order_df[order_df['order_logistics_取派时间差(天)']>5].shape[0]
y3 = round(100*(x3-x2)/order_df.shape[0],4)
mydict['不考虑,取派时间差大于5天，小于10天'] = '共{0}条, 占比{1}(%)'.format(x3-x2,y3)
mydict['总共忽略的订单占比（%）'] = '共{0}'.format(round(y1+y2+y3,3))


# In[10]:



fname = '05volin图_x运送时限_y取派时间'

### 选择的订单
order_df_s = order_df[(order_df['order_logistics_取派时间差(天)']<5)&(order_df['order_logistics_取派时间差(天)']>0)].reset_index(drop=True)
sns.violinplot(x="order_to_timelimit", y="order_logistics_取派时间差(天)", data=order_df_s, palette='Set2')
# sns.stripplot(x="order_to_timelimit", y="order_logistics_取派时间差(天)",data=order_df_s, jitter=True,palette=sns.hls_palette(8, l=.5, s=.8))
# df1.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('volin图_x运送时限_y取派时间', file=fp)


# In[11]:


fname = '06_中午12点前收货'
sns.violinplot(x='order_to_timelimit', y='order_logistics_取派时间差(天)', hue='order_12点前取件', data=order_df_s, split=True, inner='quartile',palette=['green', 'orange'])
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()
with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('06_中午12点前收货', file=fp)


# In[12]:


fname = '06_晚上17点前取件'
sns.violinplot(x='order_to_timelimit', y='order_logistics_取派时间差(天)', hue='order_17点前取件', 
               data=order_df_s, split=True, inner='quartile',palette=['purple', 'cyan'])
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()
with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('order_17点前取件', file=fp)


# In[13]:


for k,v in mydict.items():
    print('============================',k, file=f2)
    print(v, file=f2)
f2.close()
plt.close()

