

import sys
import numpy as np
import pandas as pd
import warnings

from colour import Color

red = Color("#E066FF")
color_list = [str(x) for x in  list(red.range_to(Color("limegreen"),4))]

############## 直接读文件测试
def get_relation_network_by_corr_df(corr):  # corr是相关性df.corr()
    if corr.shape[0]<10:
        LOW_LINK = 0
    elif corr.shape[0]<100:
        LOW_LINK = 0.2+0.004*corr.shape[0]
    else:
        LOW_LINK = 0.6            ###### 相关性超出LOW_LINK才显示
    print('LOW_LINK-----------', LOW_LINK)
    corr_mean = corr.mean().mean()
    name_list = corr.columns.tolist()
    ### 节点数据
    mydict = {}
    category_list = []
    data_list = []
    for i in range(len(name_list)):
        dict_i = {}
        dict_i['name']=name_list[i]
        dict_i['label']=''
        dict_i['draggable']=True
        dict_i['category']=name_list[i]
        dict_i['symbolSize']=15+(sum([abs(val) for val in corr[name_list[i]]])/len(name_list))**2*30
        dict_i['label']={"normal":{}}
        dict_i['label']['normal']['show']=True
        dict_i['label']['normal']['fontSize']= dict_i['symbolSize']
        dict_i['label']['normal']['color']='white'
        data_list.append(dict_i)
        category_list.append({"name":name_list[i], "icon":"circle"})
    link_list = []
    for i in range(len(name_list)):
        for j in range(i, len(name_list)):
            if abs(corr[name_list[i]][j])>LOW_LINK:
                dict_ij = {}
                dict_ij['source'] = name_list[i]
                dict_ij['target'] = name_list[j]
                dict_ij['lineStyle'] = {'normal':{}}
                dict_ij['lineStyle']['normal']['show']=True
                dict_ij['lineStyle']['normal']['width']= (corr[name_list[i]][j])**3*int(40*(1-LOW_LINK))
                dict_ij['lineStyle']['normal']['color']='source'
                dict_ij['lineStyle']['normal']['curveness']=0.2
                dict_ij['lineStyle']['normal']['type']='solid'
                link_list.append(dict_ij)

    mydict['data'] = data_list
    mydict['link'] = link_list
    mydict['legend_data'] = category_list
    # print(mydict)
    return mydict

################################################################################  散点图
def get_scatter_by_v1_v2(df, col_list):
    v1 = col_list[0]    # vl为x轴
    v2 = col_list[1]    # v2为y轴       
    df = df[[v1, v2]].astype(float)
    mydict = {}
    rows = []
    for i in range(df.shape[0]):
        v1_f = float(df[v1][i])
        v2_f = float(df[v2][i])
        rows.append([v1_f, v2_f])
    mydict['data'] = rows
    mydict['xmin_max_ymin_max'] = [df[v1].min(), df[v1].max(), df[v2].min(), df[v2].max()]
    return mydict
################################################################################  index列为x轴
def get_multiline_by_v_list(df, col_list, plot_type='line'):
    # print(col_list)
    # print(df)
    df = df[col_list]
    mydict = {}
    mydict['legend_data'] = list(col_list)
    mydict['xAxis_data'] = df.index.astype(str).values.tolist()
    mydict['series'] = []
    mydict['color'] = color_list[len('-'.join(color_list))%len(color_list)]

    if plot_type in ['pie']:  # 注意选择Pie时col_list只能传过来一列
        v1 = col_list[0]
        df = df.sort_values(v1)
        mydict['name_list'] = [str(i) for i in df.index]
        mydict['data_list'] = []
        value_list = np.around(df[v1].values, decimals=2).tolist()
        for i in range(len(mydict['name_list'])):
            dict_i = {"name":mydict['name_list'][i], "value":value_list[i]}
            mydict['data_list'].append(dict_i)
        return mydict

    if plot_type in ['line', 'bar']:
        for i,v_i in enumerate(col_list):
            dict_i = {}
            dict_i['color'] = color_list[i%len(color_list)]
            dict_i['name']=v_i
            dict_i['type']=plot_type
            dict_i['data']= np.around(df[v_i].values, decimals=2).tolist()
            mydict['series'].append(dict_i)

        return mydict

    if plot_type in ['bar_stack']:
        for i,v_i in enumerate(col_list):
            dict_i = {}
            dict_i['color'] = color_list[i%len(color_list)]
            dict_i['name']=v_i
            dict_i['type']= 'bar'
            dict_i['stack']='stack'
            dict_i['emphasis']= {"focus": "series"}
            dict_i['data']= np.around(df[v_i].values, decimals=2).tolist()
            mydict['series'].append(dict_i)
        return mydict 

    if plot_type in ['area_stack']:
        for i,v_i in enumerate(col_list):
            dict_i = {}
            dict_i['name']=v_i
            dict_i['color'] = color_list[i%len(color_list)]
            dict_i['type']= 'line'
            dict_i['stack']='sum'
            dict_i["areaStyle"]=str('{}')
            dict_i['emphasis']= {"focus": "series"}
            dict_i['data']= np.around(df[v_i].values, decimals=2).tolist()
            mydict['series'].append(dict_i)
        return mydict

    if plot_type in ['line_bars_mix']:
        for i,v_i in enumerate(col_list):
            dict_i = {}
            if col_list.index(v_i)==0:  # 第一列为Line为线条
                dict_i['yAxisIndex']=1
                plt_type = 'line'
            else:
                plt_type = 'bar'
                dict_i['stack']='stack'
                dict_i['emphasis']= {"focus": "series"}

            dict_i['name'] = v_i
            dict_i['color'] = color_list[i%len(color_list)]
            dict_i['type'] = plt_type
            dict_i['data'] = np.around(df[v_i].values, decimals=2).tolist()
            mydict['series'].append(dict_i)
        return mydict


################################################################################  统计频率直方图
def get_multiline_hist_by_v_list(df, col_list, plot_type='line'):
    v_list = col_list
    df = df[v_list]             # v_list为数值列的列名
    max1 = df.max().max()
    min1 = df.min().min()
    min_max1 = np.array([max1, min1])
    MAX_BINS = 300
    MY_BINS = min(int(df.shape[0]/10), MAX_BINS)
    mydict = {}
    mydict['legend_data'] = v_list
    mydict['series'] = []
    mydict['color'] = color_list[len('-'.join(color_list))%len(color_list)]
    for v_i in v_list:
        values_i = np.append(df[v_i].values, min_max1)
        hist,bins = np.histogram(values_i, bins=MY_BINS)   #用numpy包计算直方图
        dict_i = {}
        dict_i['name']=v_i
        dict_i['type']=plot_type
        dict_i["emphasis"]: {"focus": "series"}
        dict_i['data']= np.around(hist/len(values_i), decimals=8).tolist()
        mydict['series'].append(dict_i)
    mydict['xAxis_data'] = np.around(bins, decimals=3).tolist()
    return mydict
         
################################################################################  数据透视表二维数据
def get_multiline_pivot_c1_c2_v1(df, col_list, plot_type='line'):
    c1 = col_list[0]        # 第1个分类字段
    c2 = col_list[1]        # 第2个分类字段
    v1 = col_list[2]        # 数值字段

    df = df[col_list]
    df = pd.pivot_table(index=c2, columns=c1, data=df).fillna(0)
    df.columns = df.columns.droplevel()
    # print(df,'测试1')
    # df = df.reset_index(drop=True)
    # print(df,'测试2')
    # df.to_excel('get_multiline_pivot_c1_c2_v1.xlsx', index=False)
    col_list = df.columns.tolist()
    mydict = get_multiline_by_v_list(df, col_list, plot_type=plot_type)
    return mydict
################################################################################  数据三维分类数据
def get_multiline_c1_c2_c3_v1(df, col_list, plot_type='line'):
    c1 = col_list[0]        # 第1个分类字段
    c2 = col_list[1]        # 第2个分类字段
    c3 = col_list[2]        # 数值字段
    v1 = col_list[3]        # 数值字段

    mydict = {}
    df = df[col_list]
    xAxis_data = df[c1].unique().tolist()           # x轴
    unique_c2_list = df[c2].unique().tolist()
    unique_c3_list = df[c3].unique().tolist()
    mydict['legend_data'] = unique_c2_list
    mydict['xAxis_data'] = xAxis_data
    mydict['series'] = []

    for unique_c2 in unique_c2_list:
        # print('===========unique_c2', unique_c2)
        df_i = df[df[c2]==unique_c2]
        for unique_c3 in unique_c3_list:
            dict_i = {}
            df_ij = df_i[df[c3]==unique_c3]
            dict_i['name'] = unique_c2
            dict_i['type'] = 'line'
            # dict_i['stack'] = 'stack'
            dict_i['data'] = df_ij[v1].values.tolist()
            mydict['series'].append(dict_i)
    return mydict

################################################################################  列相关性
def get_relation_network_by_v_list(df, col_list, plot_type='relation_network'):
    corr = df.corr()
    return get_relation_network_by_corr_df(corr)

################################################################################  地图（热力图）
def get_map_heat_city_year_v_list(df, col_list, plot_type='map_heat'):
    name_col = col_list[0]    # 区名列
    year_col = col_list[1]    # 时间列
    val_col = col_list[2]    # value
    mydict = {"title":val_col+'热力地图', "data":[], "max_v":int(df[val_col].max()), "min_v":int(df[val_col].min())}
    unique_year_list = df[year_col].unique().tolist()
    unique_year_list.sort()
    # mydict = {"year_list":unique_year_list}
    for unique_year_i in unique_year_list:
        df_i = df[df[year_col]==unique_year_i].sort_values(val_col).reset_index(drop=True)
        dict_i = {"time":unique_year_i, "data":[]}

        for j in range(df_i.shape[0]):
            dict_ij = {}
            dict_ij['name']=df_i[name_col][j]
            dict_ij['value']=[df_i[val_col][j], df_i[val_col][j], df_i[name_col][j]]
            dict_i['data'].append(dict_ij)
        mydict['data'].append(dict_i)

    return mydict    
################################################################################  散点    
def get_map_last_year_scatter_city_year_lng_lat_v_list(df, col_list, plot_type='map_heat'):
    name_col = col_list[0]    # 区名列
    year_col = col_list[1]    # 时间列
    lng_col = col_list[2]
    lat_col = col_list[3]
    val_col = col_list[4]    # value
    mydict = {"title":val_col+'地图散点图', "points_list":[]}
    if year_col!='no_time_col':
        unique_year_list = df[year_col].unique().tolist()
        unique_year_list.sort()
        df = df[df[year_col]==unique_year_list[len(unique_year_list)-1]].reset_index(drop=True)
    max_val = df[val_col].max()
    for i in range(df.shape[0]):
        dict_i = {}
        dict_i['name']=df[name_col][i]
        dict_i['value']=[df[lng_col][i], df[lat_col][i]]
        dict_i['symbolSize']=3+20*df[val_col][i]/max_val
        mydict['points_list'].append(dict_i)

    return mydict    

def run():
    # get_1d_v1_by_c1_groupby(df, '日', '接通量', agg_type='mean', plot_type='line')
    # get_scatter_by_v1_v2(df, '接通量', '首次按键总量')
    df1 = pd.read_excel('db_jsonify_pandas_test1.xlsx', sheet_name='test1')
    df1.index = df1['创建时间']
    df1 = df1['c1,c2,c3'.split(',')]
    import dict_json_saver as mdjs
    dict_pie = get_multiline_by_v_list(df1, ['c1'], plot_type='pie')
    mdjs.save_dict_to_json(dict_pie, file_path='test/pie.json')

    dict_pie = get_multiline_by_v_list(df1, ['c1','c2'], plot_type='line')
    mdjs.save_dict_to_json(dict_pie, file_path='test/line.json')

    dict_pie = get_multiline_by_v_list(df1, ['c1','c2'], plot_type='bar')
    mdjs.save_dict_to_json(dict_pie, file_path='test/bar.json')

    dict_pie = get_multiline_by_v_list(df1, ['c1','c2', 'c3'], plot_type='bar_stack')
    mdjs.save_dict_to_json(dict_pie, file_path='test/bar_stack.json')

    dict_pie = get_multiline_by_v_list(df1, ['c1','c2', 'c3'], plot_type='area_stack')
    mdjs.save_dict_to_json(dict_pie, file_path='test/area_stack.json')

    dict_pie = get_multiline_by_v_list(df1, ['c1','c2', 'c3'], plot_type='line_bars_mix')
    mdjs.save_dict_to_json(dict_pie, file_path='test/line_bars_mix.json')


if __name__=='__main__':
    run()
