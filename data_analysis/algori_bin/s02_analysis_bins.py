
import sys
sys.path.append('../..')

import os
import json
import config
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
plt.rcParams['font.sans-serif'] = ['SimHei']                        # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False                          # 用来正常显示负号

########################### 保存的目录
myname = 's02_analysis_bins.py'
df = pd.read_excel(os.path.join(config.ROOT_PATH, 'data_analysis/说明.xlsx'))
df = df[df['code_name']==myname]
res_dict = dict(zip(df.columns, df.iloc[0]))
p_path = os.path.join(config.f_path['data_analysis_res'], '%s/%s'%(res_dict['res_folder'], res_dict['res_file']))
if os.path.exists(p_path) is False:os.makedirs(p_path)

########################### 读取数据
df1 = pd.read_excel(os.path.join(config.ROOT_PATH, 'data/bin/箱子算法数据维护.xlsx'), sheet_name='箱子信息').sort_values('类型')
df1 = df1[df1['是否使用']==1].reset_index(drop=True)
df2 = pd.read_excel(os.path.join(config.ROOT_PATH, 'data/bin/箱子算法数据维护.xlsx'), sheet_name='温区分类字典').fillna(0)

########################### 第一个图片
FNAME = '01箱子尺寸'
df = df1['内径长_mm,内径宽_mm,内径高_mm'.split(',')]
df.index = df1['名称']
df.plot.bar()
plt.tight_layout()
plt.xlabel('mm')
plt.ylabel('箱子类别')        
plt.savefig(os.path.join(p_path, '%s.png'%FNAME), dpi=150)
# plt.show()
with open(os.path.join(p_path, '%s.py'%FNAME), 'w', encoding='utf-8') as f2:
    print('目前已有的箱型数量:%s'%str(df.shape[0]), file=f2)
    print('*'*10, file=f2)

df = df1['名称,内径长_mm,内径宽_mm,内径高_mm'.split(',')]
df.to_excel(os.path.join(p_path, '%s.xlsx'%FNAME), index=False)


def hat_graph(ax, xlabels, values, group_labels):
        """
        Create a hat graph.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Axes to plot into.
        xlabels : list of str
            The category names to be displayed on the x-axis.
        values : (M, N) array-like
            The data values.
            Rows are the groups (len(group_labels) == M).
            Columns are the categories (len(xlabels) == N).
        group_labels : list of str
            The group labels displayed in the legend.
        """

        def label_bars(heights, rects):
            """Attach a text label on top of each bar."""
            for height, rect in zip(heights, rects):
                ax.annotate(f'{height}',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 4),  # 4 points vertical offset.
                            textcoords='offset points',
                            ha='center', va='bottom')
        import numpy as np
        values = np.asarray(values)
        x = np.arange(values.shape[1])
        ax.set_xticks(x, labels=xlabels) # , labels=xlabels
        
        spacing = 0.3  # spacing between hat groups
        width = (1 - spacing) / values.shape[0]
        heights0 = values[0]
        for i, (heights, group_label) in enumerate(zip(values, group_labels)):
            style = {'fill': False} if i == 0 else {'edgecolor': 'black'}
            rects = ax.bar(x - spacing/2 + i * width, heights - heights0,
                           width, bottom=heights0, label=group_label, **style)
            label_bars(heights, rects)

# initialise labels and a numpy array make sure you have
# N labels of N number of values in the array

xlabels = df2['温度备注'].values
playerA = df2['最低温度'].astype(int).values
playerB = df2['最高温度'].astype(int).values

fig, ax = plt.subplots()
hat_graph(ax, xlabels, [playerA, playerB], ['最低温度', '最高温度'])

pl.xticks(rotation=60)
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('温区')
ax.set_ylabel('温度')
# ax.set_ylim(0, 60)
ax.set_title('温区')
ax.legend()

fig.tight_layout()
FNAME = '02温区范围图'
plt.savefig(os.path.join(p_path, '%s.png'%FNAME), dpi=150)
plt.clf()
# plt.show()

with open(os.path.join(p_path, '%s.py'%FNAME), 'w', encoding='utf-8') as f2:
    print('config配置对应键==>温度备注==>EP最小干冰体积比==>温度类别', file=f2)
    for i,r in df2.iterrows():
        print('config温度%s==>%s==>%s==>%s'%(int(r['config配置对应键']), r['温度备注'], r['EP最小干冰体积比'], r['温度类别']), file=f2)
plt.close()