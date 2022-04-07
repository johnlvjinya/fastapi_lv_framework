

import pandas as pd


def check_df(df):
    s1 = df.dtypes
    s2 = df.isnull().sum()
    res_df = pd.DataFrame([], columns=['col_name'])
    res_df['col_name'] = s1.index
    res_df['类型'] = s1.tolist()
    res_df['空值num'] = s2.tolist()
    res_df['空值percent'] = (res_df['空值num']/df.shape[0]).round(3) #显示3位
    unique_list = []
    for col in df.columns.tolist():
        try:
            unique_list.append(len(df[col].unique().tolist()))
        except:
            print(col,'========error', type(df[col]))
            unique_list.append(0)

    res_df['唯一num'] = unique_list
    res_df['唯一percent'] = (res_df['唯一num']/df.shape[0]).round(3) #显示3位

    res_df = res_df.reset_index(drop=True)
    # res_df.to_excel('df_basic_info.xlsx', index=False)
    return res_df





if __name__=='__main__':

    df = pd.read_pickle('E:/SS_KUDU/customer.pickle')
    res_df = check_df(df)
    # print(res_df)


















