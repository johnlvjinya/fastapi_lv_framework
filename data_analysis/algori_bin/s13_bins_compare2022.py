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
plt.switch_backend('agg')
plt.rcParams['font.sans-serif'] = ['SimHei']                        # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                          # 用来正常显示负号
mydict = {}

from datetime import datetime
now = datetime.now()                # current date and time
date_year = now.strftime("%Y")
date_year_start = '%s-01-01'%date_year
print("date and time:",date_year, date_year_start)

date_month = now.strftime("%Y-%m")
date_month_start = '%s-01'%date_month
print("date and time:",date_year, date_month_start)


# In[2]:
myname = 's13_bins_compare2022.py' ########## 这里要修改城文件名
df1 = pd.read_excel(os.path.join(config.ROOT_PATH, 'data_analysis/说明.xlsx'))
df1 = df1[df1['code_name']==myname]
res_dict = dict(zip(df1.columns, df1.iloc[0]))
res_path = os.path.join(config.f_path['data_analysis_res'], '%s/%s'%(res_dict['res_folder'], res_dict['res_file']))
if os.path.exists(res_path) is False:os.makedirs(res_path)


# In[3]:
df1 = pd.read_excel(os.path.join(config.f_path['data_excel'], 'bin_存在尺寸的运单2022.xlsx'))
cols = df1.columns.tolist()
rename_dict = {'运输单序号':'运输单序号'}
for x in cols:
    if x!='运输单序号':
        rename_dict[x] = 'algori_'+x
df1.rename(columns=rename_dict,inplace=True)
for c in df1.columns:
    print(c)
df1_sto_id = df1[['运输单序号']]
to_goodstype = {
    1:'临床样本',3:'临床药品',
    5:'商业成品药',6:'脐带血',
    7:'细胞CAR-T',8:'IVD试剂（器械）',
    9:'特检普检',10:'科研样本',
    4:'其他物品',2:'回收药',
    11:'样品'
}
df1['algori_货物类型']=df1['algori_货物类型'].map(to_goodstype)  # 保存所有箱子的信息
# 'to_goodstype' => 
# [1=>'临床样本',3=>'临床药品',
#  5=>'商业成品药',6=>'脐带血',
#  7=>'细胞CAR-T',8=>'IVD试剂（器械）',
#  9=>'特检普检',10=>'科研样本',
#  4=>'其他物品',2=>'回收药',
#  11=>'样品'],


# In[4]:


f_path = os.path.join(config.f_path['kudu_table_pickle'], 'order_material.pickle')
df2 = pd.read_pickle(f_path)
df2 = df2[df2['visible']==1].reset_index(drop=True)
s_cols = [
    'to_id',# '运输单序号',
    'stt_id',# '存货类型序号',
    'sto_id',# '存货序号',
    'sto_name',# '存货名称',
    'om_quantity',# '数量',
]
df2 = df2[s_cols]
############ 找到对应的存货类型序号
df2['stt_id'] = df2['stt_id'].fillna(-999).astype(int)
print(df2['stt_id'].unique().tolist())

m_type_dict = {}
for k in [5,6,51,52,9]:m_type_dict[k]='箱子'
for k in [4,36]:m_type_dict[k]='温度计'
for k in [50,-999]:m_type_dict[k]='鼎为定位器'
df2['stt_id']=df2['stt_id'].map(m_type_dict)  # 保存所有箱子的信息
df2 = df2[df2['stt_id']=='箱子']
print(df2.shape)

cols = df2.columns.tolist()

rename_dict = {'to_id':'运输单序号'}
for x in cols:
    if x!='to_id':
        rename_dict[x] = 'material_'+x
df2.rename(columns=rename_dict,inplace=True)
for k,v in rename_dict.items():
    print(v)


# In[5]:


f_path = os.path.join(config.f_path['kudu_table_pickle'], 'order_material_plan.pickle')
df3 = pd.read_pickle(f_path)
print(df3.shape)
s_cols = [
    'omp_id',# '计划包装序号',
    'omp_to_id',# '运单序号',
    'omp_sto_id',# '存货序号',
    'omp_sto_name',# '存货名称',
    'omp_quantity',# '数量',
]
############ 找到对应的存货类型序号
df3['omp_sto_id'] = df3['omp_sto_id'].fillna(-999).astype(int)
print(df3['omp_sto_id'].unique().tolist())
print('df3.shape', df3.shape)
df3 = df3[s_cols]
cols = df3.columns.tolist()

rename_dict = {'omp_to_id':'运输单序号'}
for x in cols:
    if x!='omp_to_id':
        rename_dict[x] = 'plan_'+x
df3.rename(columns=rename_dict,inplace=True)
for k,v in rename_dict.items():
    print(v)


# In[6]:


'''
order_material表对应material_：
    'to_id',# '运输单序号',
    'stt_id',# '存货类型序号',
    'sto_id',# '存货序号',
    'sto_name',# '存货名称',
    'om_quantity',# '数量',
'''

df_material = pd.merge(df1_sto_id, df2, on='运输单序号', how='left')
df_material.fillna('0', inplace=True)
df_material['实际箱型cn'] = df_material['material_om_quantity'].astype(int).astype(str)+'*'+df_material['material_sto_name']

df_material['实际箱型id'] = df_material['material_om_quantity'].astype(int).astype(str)+'*'+df_material['material_sto_id'].astype(int).astype(str)

# df_material.to_excel(os.path.join(config.ROOT_PATH, 'test.xlsx'), index=False)  # 实际的箱型匹配
# df_plan.to_excel(os.path.join(config.ROOT_PATH, 'test.xlsx'), index=False)  # 计划的箱型匹配


# In[7]:


############ 实际箱型
rows = []
for g in df_material.groupby('运输单序号'):
    rows_i = [g[0], ';'.join(g[1]['实际箱型cn']), ';'.join(g[1]['实际箱型id'])]
    rows.append(rows_i)
df_materil_bin = pd.DataFrame(rows, columns='运输单序号,实际箱型cn,实际箱型id'.split(","))
df_materil_bin.to_excel(os.path.join(config.ROOT_PATH, 'test.xlsx'), index=False)  # 实际的箱型匹配
df_materil_bin = df_materil_bin['运输单序号,实际箱型cn,实际箱型id'.split(',')]


# In[10]:


############ 计划箱型
'''
order_material_plan表对应plan_：
    'omp_id',# '计划包装序号',
    'omp_to_id',# '运单序号',
    'omp_sto_id',# '存货序号',
    'omp_sto_name',# '存货名称',
    'omp_quantity',# '数量',
'''

df_plan = pd.merge(df1_sto_id, df3, on='运输单序号', how='left')
df_plan.fillna('0', inplace=True)

df_plan['计划箱型cn'] = df_plan['plan_omp_quantity'].astype(int).astype(str)+'*'+df_plan['plan_omp_sto_name']

df_plan['计划箱型id'] = df_plan['plan_omp_quantity'].astype(int).astype(str)+'*'+df_plan['plan_omp_sto_id'].astype(int).astype(str)

# df_plan.to_excel(os.path.join(config.ROOT_PATH, 'test.xlsx'), index=False)  # 实际的箱型匹配
df_plan = df_plan['运输单序号,计划箱型cn,计划箱型id'.split(',')]

df = pd.merge(df1, df_materil_bin, on='运输单序号', how='left')
df = pd.merge(df, df_plan, on='运输单序号', how='left')
algori_real_compare_list = []
algori_plan_compare_list = []
plan_real_compare_list = []

df['algori_计算箱型cn'] = df['algori_计算箱型cn'].astype(str)
df['实际箱型cn'] = df['实际箱型cn'].astype(str)
df['计划箱型cn'] = df['计划箱型cn'].astype(str)

for i,r in df.iterrows():
    s1 = r['algori_计算箱型cn'].replace('VIP6M+', 'VIP6').replace('VIP6N', 'VIP6').replace('M+', '')
    s2 = r['实际箱型cn'].replace('VIP6M+', 'VIP6').replace('VIP6N', 'VIP6').replace('M+', '')
    s3 = r['计划箱型cn'].replace('VIP6M+', 'VIP6').replace('VIP6N', 'VIP6').replace('M+', '')

    s1 = s1.split(';')
    s1.sort()
    s1 = ';'.join(s1)

    s2 = s2.split(';')
    s2.sort()
    s2 = ';'.join(s2)

    s3 = s3.split(';')
    s3.sort()
    s3 = ';'.join(s3)

    if s1==s2:
        algori_real_compare_list.append('是')
    else:
        algori_real_compare_list.append('否')
        
    if s1==s3:
        algori_plan_compare_list.append('是')
    else:
        algori_plan_compare_list.append('否')       
        
    if s2==s3:
        plan_real_compare_list.append('是')
    else:
        plan_real_compare_list.append('否')
df['计算与实际是否一致'] = algori_real_compare_list
df['计算与计划是否一致'] = algori_plan_compare_list
df['计划与实际是否一致'] = plan_real_compare_list
df.to_excel(os.path.join(config.f_path['data_excel'], 'bin_计算箱型结果对比.xlsx'), index=False)


# In[11]:


fname = '01箱型计算结果'

x_list=[1,2,3]#X轴数据
y_list = [1, 2, 3]
plt.plot(x_list, y_list)
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=5)
plt.clf()
print(df.columns.tolist())
cos_s_dict = {
    '运输单序号':'运单号',
    'algori_纸质运单编号':'纸质运单编号',
    'algori_运输温度':'运输温度',
    'algori_委托客户序号':'客户序号',
    'algori_项目序号':'项目序号',
    'algori_创建时间':'创建时间',
    'algori_shape_str':'货物尺寸',
    'algori_货物类型数':'货物类别数',
    'algori_货物名称':'货物名称',
    'algori_货物类型':'货物类型',
    'algori_计算箱型cn':'计算箱型',
    'algori_求解方案':'求解方案',
    '实际箱型cn':'实际箱型',
    '计划箱型cn':'计划箱型',
    '计算与实际是否一致':'计算VS实际',
    '计算与计划是否一致':'计算VS计划',
    '计划与实际是否一致':'计划VS实际',
}

df = df[list(cos_s_dict.keys())]
df.rename(columns=cos_s_dict,inplace=True)

df = df[df['创建时间']>date_year_start]
df.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('对比计算箱型-实际箱型-计划箱型', file=fp)
for col in df.columns:
    print(col)


# In[12]:


# df = pd.read_excel('02箱型计算对比.xlsx')
# print(df.columns.tolist())
def create_consistent_count(res_path=res_path, xcol='创建时间',customer=None):
    import pandas as pd
    def cal_y_col(ycol = '计算VS实际',xcol='创建时间', customer=None):
        import pandas as pd
        df = pd.read_excel(os.path.join(res_path,'01箱型计算结果.xlsx'))
        df = df[df['实际箱型']!='0*0'].reset_index(drop=True)
        if customer is not None:
            df[df['客户序号']==customer]
        # xcol = '创建时间'
        # ycol = '计算VS实际'
        count_col = '运单号'
        df_p = pd.pivot_table(df,index=[xcol],columns=[ycol],
                              values=[count_col], aggfunc = 'count').fillna(0) # , aggfunc = 'count'
        list1 = [x for x in df_p.index.tolist()]  # 温度config_id
        list2 = [x[1] for x in df_p.T.index.tolist()]

        # print(list1)
        # print(list2)
        df_p = df_p.T.reset_index(drop=True).T
        df_p.index = list1
        df_p.columns = list2
        print(df_p.columns)
        df_p[ycol+'一致率(%)'] =( 100*df_p['是']/(df_p['是']+df_p['否'])).round(1)
        rename_dict = {'否':ycol+'不一致', '是':ycol+'一致',}
        df_p.insert(0,  xcol, df_p.index)
        df_p.sort_values(xcol, inplace=True)
        df_p.rename(columns=rename_dict,inplace=True)
        return df_p

    df1 = cal_y_col(ycol = '计算VS实际',xcol=xcol,customer=None)
    df2 = cal_y_col(ycol = '计算VS计划',xcol=xcol,customer=None)
    df3 = cal_y_col(ycol = '计划VS实际',xcol=xcol,customer=None)

    df = pd.merge(df1, df2, on=xcol)
    df = pd.merge(df, df3, on=xcol)
    import matplotlib.pyplot as plt
    color_map = plt.get_cmap('GnBu')  # 颜色选择参考
    
    df_style_excel = df[[xcol,'计算VS实际一致率(%)','计算VS计划一致率(%)','计划VS实际一致率(%)']].style.background_gradient(
        color_map, subset=['计算VS实际一致率(%)']).background_gradient(
        color_map, subset=['计算VS计划一致率(%)']).background_gradient(
        color_map, subset=['计划VS实际一致率(%)']
        )
    return df, df_style_excel


xcol = '创建时间'
df, df_style_excel = create_consistent_count(xcol=xcol,customer=None)
print(df.columns.tolist())
############ 
fname = '01运单数量一致性堆积图'
df_style_excel.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)

# if df.shape[0]>30:
#     start_n = 30
# else:
#     start_n = 0
# df = df[start_n:]

############ 画第一个子图
df_t = df['计算VS实际一致,计算VS实际不一致'.split(',')]
df_t.index=df[xcol]

ax1 = df_t.plot.bar(stacked=True, alpha=0.8)

import myutils.db_jsonify_pandas as mdjp
import myutils.dict_json_saver as mdjs

# e_dict = mdjp.get_multiline_by_v_list(df_t, df_t.columns, plot_type='bar_stack')
# mdjs.save_dict_to_json(e_dict, file_path=os.path.join(config.f_path['ec_json'], 'bin_inconsistant_bar_stack.json'))

df_t.insert(0, '一致率', df_t['计算VS实际一致']/(df_t['计算VS实际一致']+df_t['计算VS实际不一致']))
e_dict = mdjp.get_multiline_by_v_list(df_t, list(df_t.columns), plot_type='line_bars_mix')
mdjs.save_dict_to_json(e_dict, file_path=os.path.join(config.f_path['ec_json'], 'bin_inconsistant_line_bars_mix.json'))



ax2 = ax1.twinx() 

######双坐标， df.plot参数 https://blog.csdn.net/h_hxx/article/details/90635650
cols_list = ['计算VS实际一致率(%)','计算VS计划一致率(%)','计划VS实际一致率(%)']
df_t2 = df[cols_list]
df_t2.plot(kind='line',ax=ax2, secondary_y=False,lw=1) 

ax2.fill_between(df_t2.index, df_t2['计算VS实际一致率(%)'], df_t2['计划VS实际一致率(%)'], facecolor='cyan', alpha=0.2)
ax1.legend(bbox_to_anchor=(1.1, 0), loc=1, borderaxespad=0, frameon=False)
ax2.legend(bbox_to_anchor=(1.005, 1), loc=1, borderaxespad=0, frameon=False)
plt.xticks([])
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('根据订单的创建时间分析，计算箱型与计划和实际的一致性', file=fp)

# In[13]:


xcol='货物类别数'
df, df_style_excel = create_consistent_count(xcol=xcol,customer=None)
############ 
fname = '04箱型一致性统计VS货物类别数'
df_style_excel.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)

############ 画第一个子图
df_t = df['计算VS实际一致,计算VS实际不一致'.split(',')]
df_t.index=df[xcol]
ax1 = df_t.plot.bar(stacked=True, alpha=0.8)
ax2 = ax1.twinx() 

######双坐标， df.plot参数 https://blog.csdn.net/h_hxx/article/details/90635650
cols_list = ['计算VS实际一致率(%)','计算VS计划一致率(%)','计划VS实际一致率(%)']
df_t2 = df[cols_list]
df_t2.plot(kind='line',ax=ax2, secondary_y=False,lw=1) 

ax1.legend(bbox_to_anchor=(1.1, 0), loc=1, borderaxespad=0, frameon=False)
ax2.legend(bbox_to_anchor=(1.005, 1), loc=1, borderaxespad=0, frameon=False)
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()


with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('根据订单的货物类别数分析，计算箱型与计划和实际的一致性', file=fp)
    print('注意：货物类别数表示，这个订单种出现了多少种货物', file=fp)


# In[14]:


xcol='货物类型'
df, df_style_excel = create_consistent_count(xcol='货物类型',customer=None)
############ 
fname = '05箱型一致性统计VS货物类型'
df_style_excel.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)

############ 画第一个子图
df_t = df['计算VS实际一致,计算VS实际不一致'.split(',')]
df_t.index=df[xcol]
ax1 = df_t.plot.bar(stacked=True, alpha=0.8)
ax2 = ax1.twinx() 

######双坐标， df.plot参数 https://blog.csdn.net/h_hxx/article/details/90635650
cols_list = ['计算VS实际一致率(%)','计算VS计划一致率(%)','计划VS实际一致率(%)']
df_t2 = df[cols_list]
df_t2.plot(kind='line',ax=ax2, secondary_y=False,lw=1) 

ax1.legend(bbox_to_anchor=(1.1, 0), loc=1, borderaxespad=0, frameon=False)
ax2.legend(bbox_to_anchor=(1.005, 1), loc=1, borderaxespad=0, frameon=False)
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()


with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('根据订单的货物类型数分析，计算箱型与计划和实际的一致性', file=fp)
    print('注意观察，不同的货物类型对于一致性的影响', file=fp)


# In[15]:


xcol='创建时间'
df, df_style_excel = create_consistent_count(xcol=xcol,customer=201600962)
print(df.index.tolist())
print(df[xcol].tolist())

############ 
fname = '06箱型一致性统计VS创建时间（客户-柯乾）'
df_style_excel.to_excel(os.path.join(res_path,'%s.xlsx'%fname), index=False)

############ 画第一个子图
df_t = df['计算VS实际一致,计算VS实际不一致'.split(',')]
df_t.index=df[xcol]
ax1 = df_t.plot.bar(stacked=True, alpha=0.8)
ax2 = ax1.twinx() 

######双坐标， df.plot参数 https://blog.csdn.net/h_hxx/article/details/90635650
cols_list = ['计算VS实际一致率(%)','计算VS计划一致率(%)','计划VS实际一致率(%)']
df_t2 = df[cols_list]
df_t2.plot(kind='line',ax=ax2, secondary_y=False,lw=1) 

ax1.legend(bbox_to_anchor=(1.1, 0), loc=1, borderaxespad=0, frameon=False)
ax2.legend(bbox_to_anchor=(1.005, 1), loc=1, borderaxespad=0, frameon=False)
plt.xticks([])
plt.tight_layout()
plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
plt.clf()

with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
    print('根据订单的创建时间分析，计算箱型与计划和实际的一致性', file=fp)
    print('*'*50, file=fp)
    print('柯乾'*10, file=fp)
    print('*'*50, file=fp)


# In[ ]:


plt.close()

