

import pandas as pd


def list_non_duplicate_t(list_duplicate = [3, 1, 4, 3, 6, 3, 2, 4, 9, 1]):
    
    list_non_duplicate = list(set(list_duplicate))
    list_non_duplicate.sort(key=list_duplicate.index)
    return list_non_duplicate

########## 按照某一列group，然后其他列用;合并
def flatten_df_by_col(df, g_col):
    df = df.fillna(0)
    cols_list = df.columns.tolist()
    cols_list.remove(g_col)  # 去掉groupby的列
    for x in cols_list:
        df[x] = df[x].astype(str)
    group_df = df.groupby(g_col)
    new_rows = []
    for i in group_df:
        row_i = []
        row_i.append(i[0])
        # print(i[0])
        for j in cols_list:
            list_ij = list(set(i[1][j].tolist()))
            list_ij.sort()
            row_i.append(';'.join(list_ij).rstrip(';'))
        new_rows.append(row_i)
    df = pd.DataFrame(new_rows, columns=[g_col]+cols_list)
    return df


def flatten_df_by_col_with_turn_for_route(df, g_col):
    df = df.fillna(0)
    cols_list = df.columns.tolist()
    cols_list.remove(g_col)  # 去掉groupby的列
    for x in cols_list:
        df[x] = df[x].astype(str)
    group_df = df.groupby(g_col)
    new_rows = []
    for i in group_df:
        row_i = []
        row_i.append(i[0])
        # print(i[0])
        for j in cols_list:
            list_ij = list_non_duplicate_t(i[1][j].tolist())
            row_i.append(';'.join(list_ij).rstrip(';'))
        new_rows.append(row_i)
    df = pd.DataFrame(new_rows, columns=[g_col]+cols_list)
    return df





if __name__=='__main__':
    df = pd.read_excel('xx.xlsx')
    df1 = flatten_df_by_col(df, 'col1')
    df1.to_excel('flatten_df_by_col.xlsx', index=False)










