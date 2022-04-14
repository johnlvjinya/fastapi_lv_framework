
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import csv
import os


secret_id = 'AKIDZkleguZzmCNXS9D39tTO5XG6hCSW4mCY'  # 替换为用户的 secretId
secret_key = 'LtJwQTKwKYkjZAhz2vZVDfDWlA2hKqBJ'  # 替换为用户的 secretKey
secret_string = '-1257726623'
region = 'ap-shanghai'                  # 替换为用户的 Region
token = None                            # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'                        # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

bucket_name = 'flask-file-manage'
real_bname = bucket_name+secret_string   # 真实的bucket名称需要加上secret_string
config_cos = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
client = CosS3Client(config_cos)               # 获取客户端对象




def get_contained_file_list():              # 获得存储桶下的所有文件夹
    response = client.list_objects(
        Bucket=real_bname,
        Delimiter='/'
    )
    res = response['CommonPrefixes']
    res = [i['Prefix'].rstrip('/') for i in res]
    return res

def get_prefix_file_list(prefix):              # 获得存储桶下的所有文件夹
    response = client.list_objects(
        Bucket=real_bname,
        Prefix='%s/'%prefix
    )
    res = response['Contents']
    for x in res:
        print(x)

    return 1



def create_new_file_list(new_file_list):                 # 需要创建文件夹
    current_file_list = get_contained_file_list()
    for new_file in new_file_list:
        if new_file not in current_file_list:                   # 创建文件
            if os.path.exists(new_file) is False:
                os.mkdir(new_file)
            with open(new_file+'/'+'a_a_a_first-file-test.txt', 'w') as f2:
                print('欢迎使用腾讯云COS对象存储', file=f2)

            with open(new_file+'/'+'a_a_a_first-file-test.txt', 'rb') as fp:
                response = client.put_object(
                    Bucket=config.real_bname,  # 存储桶的名称
                    Body=fp,
                    Key=new_file+'/'+'a_a_a_first-file-test.txt',  # 文件名
                    StorageClass='STANDARD',
                    EnableMD5=False
                )
            os.remove(new_file+'/'+'a_a_a_first-file-test.txt')  # path是文件的路径
            os.rmdir(new_file)  # path是文件夹路径，注意文件夹需要时空的才能被删除
            print('成功创建文件夹..', new_file)

def get_values_bucket_filelist_info():                  # bucket_list 需要分析的bucket_列表
    # f = open('file_list.csv','w',encoding='utf-8-sig',newline='')
    # new_cols_list = 'file_path,p,sub1,sub2,sub3,name,last_modified,size,url'.split(',')
    # new_col_str = ','.join(new_col_list)                      # 拼接成string
    # s_str = '%s,'*len(new_col_list)                           # 拼接 %s 代号
    # s_str = s_str.rstrip(',')                                 # 去掉最后一个','
    # sql = "insert into {0}({1}) values ({2}) ".format(localhost_tb, new_col_str, s_str)
    response = client.list_objects(            # 查询所有文件
        Bucket=config.real_bname,
        MaxKeys=300000                              # 最多的文件
    )
    rows = []
    for item in response['Contents']:
        info_list = item['Key'].split('_')          # 以空格为分隔符，包含 \n
        if len(info_list)==4:
            file_path = info_list[0].split('/')[0]
            p = info_list[0].split('/')[1]
            sub1 = info_list[1]
            sub2 = info_list[2]
            sub3 = info_list[3]
            name = p+'_'+sub1+'_'+sub2+'_'+sub3
            last_modified = item['LastModified']
            size = item['Size']
            url = 'https://'+config.real_bname+'.cos.ap-shanghai.myqcloud.com/'+item['Key']
            row_i = [file_path,p,sub1,sub2,sub3,name,last_modified,size,url]
            rows.append(row_i)
    # with open('rows.txt', 'w', encoding='utf-8') as f2:
    #     for i in rows:
    #         print(i, file=f2)
    return rows


def delete_bucket_file(file_name):                  # bucket_list 需要分析的bucket_列表
    response = client.delete_object(
        Bucket=config.real_bname,
        Key=file_name
    )
    print(config.real_bname,'======',  file_name, '======has been deleted')

def download_bucket_file(file_name):
    response = client.get_object(
        Bucket=config.real_bname,
        Key=file_name,
    )
    response['Body'].get_stream_to_file(file_name)

def upload_bucket_file(file_name):
    with open(file_name, 'rb') as fp:
        response = client.put_object(
            Bucket=config.real_bname,  # 存储桶的名称
            Body=fp,
            Key=file_name,  # 文件名
            # Key=file_path,                # 出现在存储桶中的是个文件夹
            StorageClass='STANDARD',
            EnableMD5=False
        )

def change_bucket_file(file_path, file_name, new_file_name):                  # bucket_list 需要分析的bucket_列表

    split_list = file_name.split('.')
    new_split_list = new_file_name.split('.')
    # name_left = ''.join(split_list[:len(split_list)-1])
    name_right = split_list[len(split_list)-1]
    new_name_right = new_split_list[len(new_split_list)-1]
    if name_right == new_name_right:                         # 两次格式必须一样
        if os.path.exists(file_path) is False:
            os.mkdir(file_path)
        download_bucket_file(file_name)                # 下载文件
        os.rename(file_name, new_file_name)
        upload_bucket_file(new_file_name)
        delete_bucket_file(file_name)
        os.remove(new_file_name)

        os.rmdir(file_path)  # path是文件夹路径，注意文件夹需要时空的才能被删除


if __name__=='__main__':
    res = get_contained_file_list()
    print(res)


    