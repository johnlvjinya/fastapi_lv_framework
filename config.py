

import os

import platform
import myutils.login_hash as mlh

######### kudu下载数据的保存路径和覆盖方式
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
################## sea_table 生生分享的api
### 用户名：1040635691@qq.com 密码：wosh...  登录seatable
st_api_token = '0bfd623fc845592c776d8c35e2f24ae69cf3eb53'
server_url='https://cloud.seatable.cn'

################## 腾讯云配置，参考myutils.tencent_cos_action

### 数据和文件保存的路径
current_system = platform.system()
if current_system is 'Windows':
    python = 'python'
    pre_data_str = 'D:/fastapi_lv_framework'             # windows系统
else:
    pre_data_str = "/mnt/app/ss_data"       # linux系统
    python = 'python3.7'
f_stop_point_list = ['D:/', '/mnt/app/']    # 文件展示停止递归的节点
ac_dir_dict = {
'本地文件':pre_data_str,
}

f_path = {
    'temp':os.path.join(pre_data_str, 'temp'),
    'data_json':os.path.join(pre_data_str, 'data/json'),
    'data_excel':os.path.join(pre_data_str, 'data/excel'),
    'ec_json':os.path.join(pre_data_str, 'ec_json'),
}
for k,v in f_path.items():
    if os.path.exists(v) is False:
        os.makedirs(v)


users = {
"admin": {"password": mlh.create_password_hash('admin123'),"stop_list": [],},
}


# print(get_username_from_signed_string('Z3Vlc3Q=.67AE3F14ED812F04A3E014D562735A8BA533A50738BF08F9CD251B61144941D0'))
