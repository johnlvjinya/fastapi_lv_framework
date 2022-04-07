#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append('..')
import os
import json
import config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns

from docxtpl import DocxTemplate,InlineImage,RichText
from docx.shared import Mm


plt.rcParams['font.sans-serif'] = ['SimHei']                        # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                          # 用来正常显示负号
########## https://www.nuomiphp.com/eplan/138338.html
sns.set_context(rc={"lines.linewidth": 0.75}) 
res_path = os.path.join(config.f_path['temp'], 'route_report')
if os.path.exists(res_path) is False: os.mkdir(res_path)

# print('tttttttttttt01', region_dict)


def plot_analysis_one_collection(c1='北京市',c2='上海市'):
    res_dict = {}

    f_path = os.path.join(config.f_path['data_json'], 'route_exists_real_route_list.json')    ## 箱子温度对应的体积字典       
    route_exists_real_route_dict = json.load(open(f_path, "rb"))

    f_path = os.path.join(config.f_path['kudu_table_pickle'], 'route.pickle')
    route_df = pd.read_pickle(f_path)
    route_id_name_dict = dict(zip(route_df['ro_id'], route_df['ro_name']))

    p1 = os.path.join(config.f_path['data_analysis_res'], '路由推荐/01路由基本分析/01路由节点的分布.xlsx')
    df1 = pd.read_excel(p1)
    region_dict = dict(zip(df1['地区名'], df1['地区ID']))
    

    c1_id = region_dict.get(c1)
    c2_id = region_dict.get(c2)
    res_dict['city_info'] = '%s(%s)发往%s(%s)'%(c1, c1_id, c2, c2_id)
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
    fname = '01按年份对比'
    sns.violinplot(x='order_年份', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x='order_年份', y='order_logistics_取派时间差(天)',
        data=df,jitter=True, size=4, alpha=0.7,palette=sns.hls_palette(8, l=.5, s=.8))   # palette=sns.hls_palette(8, l=.5, s=.8),    
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()

    ################################################################################## 
    try:
        fname = '03中午12点前收货'
        sns.violinplot(x='order_to_timelimit', y='order_logistics_取派时间差(天)', hue='order_12点前取件', 
                       data=df, split=True, inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
        sns.stripplot(x="order_to_timelimit", y="order_logistics_取派时间差(天)",hue='order_12点前取件',
            data=df,jitter=True, size=4, alpha=0.7,palette=sns.hls_palette(8, l=.5, s=.8))   # palette=sns.hls_palette(8, l=.5, s=.8),
        
        plt.tight_layout()
        plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
        plt.clf()
    except:
        pass
        
    ##################################################################################  
    try:
        fname = '04晚上17点前收货'
        sns.violinplot(x='order_to_timelimit', y='order_logistics_取派时间差(天)', hue='order_17点前取件', 
                       data=df, split=True, inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
        sns.stripplot(x="order_to_timelimit", y="order_logistics_取派时间差(天)",hue='order_17点前取件',
            data=df,jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)        
        plt.tight_layout()
        plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
        plt.clf()

        fname = '05对比温度'
        print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
        sns.violinplot(x='order_to_temperature', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
        sns.stripplot(x="order_to_temperature", y="order_logistics_取派时间差(天)",data=df,
                      jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
        # plt.ylim(-0.5, 5.5)
        plt.tight_layout()
        plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
        plt.clf()
    except:
        pass
    
    fname = '06对比order_cu_id'
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    # sns.violinplot(x='order_cu_id', y='order_logistics_取派时间差(天)',data=df,inner='quartile')
    sns.stripplot(x="order_cu_id", y="order_logistics_取派时间差(天)",data=df,
                  jitter=False,palette=sns.hls_palette(30, l=.5, s=.8), size=4, alpha=0.7)
    # plt.ylim(-0.5, 5.5)
    plt.xticks([])
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()
        
    fname = '07对比order_星期几'
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    sns.violinplot(x='order_星期几', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x="order_星期几", y="order_logistics_取派时间差(天)",data=df,
                  jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
    plt.ylim(-0.5, 5.5)
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()

    fname = '08对比order_小时'
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    sns.violinplot(x='order_小时', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x="order_小时", y="order_logistics_取派时间差(天)",data=df,
                  jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
    # plt.ylim(-0.5, 5.5)
    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()

    fname = '09对比路由ID'
    print(df['order_logistics_取派时间差(天)'].max(), df['order_logistics_取派时间差(天)'].min())
    sns.violinplot(x='dispatch_detail_ro_id', y='order_logistics_取派时间差(天)',data=df,inner='quartile',palette=['#FFFAFA', '#BBFFFF', '#FFFFE0', '#FFE1FF', '#E0FFFF'])
    sns.stripplot(x="dispatch_detail_ro_id", y="order_logistics_取派时间差(天)",data=df,
                  jitter=True,palette=sns.hls_palette(8, l=.5, s=.8), size=4, alpha=0.7)
    # plt.ylim(-0.5, 5.5)
    plt.xticks(rotation =30, size=6)

    plt.tight_layout()
    plt.savefig(os.path.join(res_path,'%s.png'%fname), dpi=150)
    plt.clf()

    res_dict['ro_list'] = route_dict_lv
    return res_dict


def get_report(c1='北京市',c2='绍兴市'):
    res_dict = plot_analysis_one_collection(c1=c1,c2=c2)
    if __name__=='__main__':
        tpl = DocxTemplate('route_report_t.docx')
    else:
        tpl = DocxTemplate('myutils/route_report_t.docx')



    fig_list = os.listdir(res_path)
    fig_dict = {
        'f1':'01按年份对比.png',
        'f3':'03中午12点前收货.png',
        'f4':'04晚上17点前收货.png',
        'f5':'05对比温度.png',
        'f6':'06对比order_cu_id.png',
        'f7':'07对比order_星期几.png',
        'f8':'08对比order_小时.png',
        'f9':'09对比路由ID.png',
    }

    context = {
       "res_dict": res_dict,
    }

    size_fig = 70

    if __name__=='__main__':
        fx_1 = 'default_fig.png'
    else:
        fx_1 = 'myutils/default_fig.png'

    for k,v in fig_dict.items():
        if v in fig_list:
            context[k] = InlineImage(tpl, image_descriptor=os.path.join(res_path, v), width=Mm(size_fig))
        else:
            context[k] = InlineImage(tpl, image_descriptor=fx_1, width=Mm(10))

    if fig_dict['f9'] in fig_list:
        context['f9_big'] = InlineImage(tpl, image_descriptor=os.path.join(res_path, fig_dict['f9']), width=Mm(180))
    else:
        context['f9_big'] = InlineImage(tpl, image_descriptor=os.path.join(res_path, fx_1), width=Mm(10))

    tpl.render(context)

    s_p = os.path.join(res_path, '路由报告.docx')
    tpl.save(s_p)

    for f in fig_list:
        if '.docx' not in f:
            try:os.remove(os.path.join(res_path, f))
            except:pass
    pass


if __name__=='__main__':
    # plot_analysis_one_collection(c1='北京市',c2='上海市')
    # res_dict = plot_analysis_one_collection(c1='北京市',c2='上海市')
    # print('结果======================================================')
    # for k,v in res_dict.items():
    #     print(k,v)

    get_report(c1='北京市',c2='上海市')
    # get_report(c1='常州市',c2='沈阳市')

