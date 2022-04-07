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
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']                        # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                          # 用来正常显示负号

myname = 's02_analysis_one_collection.py' ########## 这里要修改城文件名
df = pd.read_excel(os.path.join(config.ROOT_PATH, 'data_analysis/说明.xlsx'))
df = df[df['code_name']==myname]
res_dict = dict(zip(df.columns, df.iloc[0]))
res_path = os.path.join(config.f_path['data_analysis_res'], '%s/%s'%(res_dict['res_folder'], res_dict['res_file']))
if os.path.exists(res_path) is False:os.makedirs(res_path)
f2 = open(os.path.join(res_path,config.img_pretext), 'w', encoding='utf-8')
mydict = {}


f_path = os.path.join(config.f_path['kudu_table_pickle'], 'route.pickle')
route_df = pd.read_pickle(f_path)
route_id_name_dict = dict(zip(route_df['ro_id'], route_df['ro_name']))


p1 = os.path.join(config.f_path['data_analysis_res'], '路由推荐/01路由基本分析/01路由节点的分布.xlsx')
df1 = pd.read_excel(p1)
print(df1.columns.tolist())
region_dict = dict(zip(df1['地区名'], df1['地区ID']))
# print('tttttttttttt01', region_dict)

p2 = os.path.join(config.f_path['data_analysis_res'], '路由推荐/01路由基本分析/03到港非济南，前50名路由连接.xlsx')
df2 = pd.read_excel(p2)
print(df2.columns.tolist())
print('十大出港，到港城市路由')
print('十大出港，到港城市路由',file=f2)
for i,r in df2[:10].iterrows():
    print(r['出港地区'], region_dict.get(r['出港地区']),'===>',r['到港地区'], region_dict.get(r['到港地区']),)
    print(r['出港地区'], region_dict.get(r['出港地区']),'===>',r['到港地区'], region_dict.get(r['到港地区']),file=f2)   

print('..................................以下以部分路由节点为例分析',file=f2)
# In[3]:

f_path = os.path.join(config.f_path['data_json'], 'route_exists_real_route_list.json')    ## 箱子温度对应的体积字典       
route_exists_real_route_dict = json.load(open(f_path, "rb"))



def plot_analysis_one_collection(c1='北京市',c2='上海市', region_dict=region_dict,res_path=res_path):
    f_path = os.path.join(config.f_path['data_json'], 'route_exists_real_route_list.json')    ## 箱子温度对应的体积字典       
    route_exists_real_route_dict = json.load(open(f_path, "rb"))

    f_path = os.path.join(config.f_path['kudu_table_pickle'], 'route.pickle')
    route_df = pd.read_pickle(f_path)
    route_id_name_dict = dict(zip(route_df['ro_id'], route_df['ro_name']))

    
    import matplotlib.pyplot as plt
    import pylab as pl
    import seaborn as sns
    ########## https://www.nuomiphp.com/eplan/138338.html
    sns.set_context(rc={"lines.linewidth": 0.75}) 

    c1_id = region_dict.get(c1)
    c2_id = region_dict.get(c2)
    print('城市...', c1, c1_id, c2, c2_id)
    region_route_str = '%s--%s.pickle'%(str(c1_id), str(c2_id))
    df = pd.read_pickle(os.path.join(config.f_path['route_region_df'], region_route_str))
    c_route_exists_real_route_dict = route_exists_real_route_dict.get('%s--%s'%(str(c1_id), str(c2_id)))
    if c_route_exists_real_route_dict is None:
        c_route_exists_real_route_dict = {}

    route_id_list = []
    for route_id_str in c_route_exists_real_route_dict.get('route_time_dict').keys():
        route_id_list += route_id_str.split(';')

    route_en_list = [int(x)for x in route_id_list]
    route_cn_list = [route_id_name_dict.get(int(x)) for x in route_id_list]
    route_dict_lv = dict(zip(route_en_list, route_cn_list))
    print(route_dict_lv)

    ########## 清晰时间差脏数据
    df = df[(df['order_logistics_取派时间差(天)']<5)
                          &(df['order_logistics_取派时间差(天)']>0)].reset_index(drop=True)
    
    with open(os.path.join(config.f_path['data_json'],'route_type.json'), 'r', encoding='utf8')as fp: 
        route_type_dict =json.load(fp)
    route_en_cn_dict = route_type_dict.get('en_cn_dict')

    # df['route_rt_id']=df['route_rt_id'].astype(str).map(route_en_cn_dict)  # 保存所有箱子的信息
    # 运送时限,0：12小时,1：24小时,2：36小时,3：48小时,4：52小时
    df['order_to_timelimit']=df['order_to_timelimit'].astype(str).map(
        {'0':'12小时','1':'24小时','3':'48小时','4':'52小时'})
    df = df.sort_values('order_to_timelimit').reset_index(drop=True)  # 保存所有箱子的信息
    print(df.shape[0])
#     df.to_excel(os.path.join(config.ROOT_PATH,'test.xlsx'),  index=False)
    
    ################################################################################## 
    fname = '%s_%s_01按年份对比'%(c1, c2)
    sns.violinplot(x='order_年份', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x='order_年份', y='order_logistics_取派时间差(天)',
        data=df,jitter=True, size=4, alpha=0.7,palette=sns.hls_palette(8, l=.5, s=.8))   # palette=sns.hls_palette(8, l=.5, s=.8),    
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()
    with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
        print('02_按年份对比,对比可以看出每年的时间基本稳定', file=fp)
        
    ################################################################################## 
    try:
        fname = '%s_%s_03中午12点前收货'%(c1, c2)
        sns.violinplot(x='order_to_timelimit', y='order_logistics_取派时间差(天)', hue='order_12点前取件', 
                       data=df, split=True, inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
        sns.stripplot(x="order_to_timelimit", y="order_logistics_取派时间差(天)",hue='order_12点前取件',
            data=df,jitter=True, size=4, alpha=0.7,palette=sns.hls_palette(8, l=.5, s=.8))   # palette=sns.hls_palette(8, l=.5, s=.8),
        
        plt.tight_layout()
        plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
        plt.clf()
        with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
            print('01_中午12点前收货', file=fp)
    except:
        pass
        
    ##################################################################################  
    try:
        fname = '%s_%s_04晚上17点前收货'%(c1, c2)
        sns.violinplot(x='order_to_timelimit', y='order_logistics_取派时间差(天)', hue='order_17点前取件', 
                       data=df, split=True, inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
        sns.stripplot(x="order_to_timelimit", y="order_logistics_取派时间差(天)",hue='order_17点前取件',
            data=df,jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)        
        plt.tight_layout()
        plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
        plt.clf()
        with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
            print('02_晚上17点前收货', file=fp) 

        fname = '%s_%s_05对比温度'%(c1, c2)
        print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
        sns.violinplot(x='order_to_temperature', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
        sns.stripplot(x="order_to_temperature", y="order_logistics_取派时间差(天)",data=df,
                      jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
        # plt.ylim(-0.5, 5.5)
        plt.tight_layout()
        plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
        plt.clf()
        with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
            print('02对比温度', file=fp)
    except:
        pass
    
    fname = '%s_%s_06对比order_cu_id'%(c1, c2)
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    # sns.violinplot(x='order_cu_id', y='order_logistics_取派时间差(天)',data=df,inner='quartile')
    sns.stripplot(x="order_cu_id", y="order_logistics_取派时间差(天)",data=df,
                  jitter=False,palette=sns.hls_palette(30, l=.5, s=.8), size=4, alpha=0.7)
    # plt.ylim(-0.5, 5.5)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()
    with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
        print('02对比温度', file=fp)
        
    fname = '%s_%s_07对比order_星期几'%(c1, c2)
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    sns.violinplot(x='order_星期几', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x="order_星期几", y="order_logistics_取派时间差(天)",data=df,
                  jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
    plt.ylim(-0.5, 5.5)
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()
    with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
        print('02对比温度', file=fp)    
        
    fname = '%s_%s_08对比order_小时'%(c1, c2)
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    sns.violinplot(x='order_小时', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x="order_小时", y="order_logistics_取派时间差(天)",data=df,
                  jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
    # plt.ylim(-0.5, 5.5)
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()
    with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
        print('02对比温度', file=fp) 

    fname = '%s_%s_09对比路由ID'%(c1, c2)
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    sns.violinplot(x='dispatch_detail_ro_id', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x="dispatch_detail_ro_id", y="order_logistics_取派时间差(天)",data=df,
                  jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
    # plt.ylim(-0.5, 5.5)
    plt.xticks(rotation =30, size=6)

    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()
    with open(os.path.join(res_path,'%s.py'%fname), 'w', encoding='utf-8') as fp:
        # c1_id = region_dict.get(c1)
        # c2_id = region_dict.get(c2)
        print('原始数据：{0}--{1}.pickle'.format(c1_id, c2_id), file=fp)
        print('路由id序列', file=fp) 
        for k,v in route_dict_lv.items():
            print(k, '====>', v, file=fp)

    
print(df.shape[0])


# In[4]:


# 北京市 110000 ===> 上海市 310000
# 上海市 310000 ===> 北京市 110000
# 上海市 310000 ===> 广州市 440100
# 广州市 440100 ===> 上海市 310000
# 南京市 320100 ===> 上海市 310000
# 长春市 220100 ===> 上海市 310000
# 杭州市 330100 ===> 上海市 310000
# 天津市 120000 ===> 上海市 310000
# 郑州市 410100 ===> 上海市 310000
# 杭州市 330100 ===> 北京市 11000

plot_analysis_one_collection(c1='北京市',c2='上海市')
plot_analysis_one_collection(c1='上海市',c2='佛山市')
plot_analysis_one_collection(c1='遵义市',c2='无锡市')

# plot_analysis_one_collection(c1='长春市',c2='攀枝花市')


# In[5]:


for k,v in mydict.items():
    print('============================',k, file=f2)
    print(v, file=f2)
f2.close()
plt.close()

