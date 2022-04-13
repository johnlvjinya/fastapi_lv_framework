

import os
import hmac
import hashlib
import base64
import platform

######## 业务数据库

######### kudu下载数据的保存路径和覆盖方式
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
################## sea_table 生生分享的api
### 用户名：1040635691@qq.com 密码：wosh...  登录seatable
st_api_token = '0bfd623fc845592c776d8c35e2f24ae69cf3eb53'
server_url='https://cloud.seatable.cn'

###################################################### 数据和文件保存的路径
current_system = platform.system()
if current_system is 'Windows':
    pre_data_str = 'D:/fastapi_lv_framework'             # windows系统
    python = 'python'
else:
    pre_data_str = "/lvf/fastapi_lv_framework"       # linux系统
    python = 'python3.7'
f_stop_point_list = ['D:/', '/lvf']    # 文件展示停止递归的节点

f_path = {
    'temp':os.path.join(pre_data_str, 'temp'),
    'python_projects':os.path.join(pre_data_str, 'python_projects'),
    'md_files':os.path.join(pre_data_str, 'md_files'),
    'pickle':os.path.join(pre_data_str, 'pickle'),
    'stock':os.path.join(pre_data_str, 'stock'),
    'data_analysis_res':os.path.join(pre_data_str, 'data_analysis_res'),
    'json':os.path.join(pre_data_str, 'json'),
    'ec_json':os.path.join(pre_data_str, 'ec_json'),
    'excel':os.path.join(pre_data_str, 'excel'),
    'log':os.path.join(pre_data_str, 'log'),  # 检查数据输入是否规范
}
for k,v in f_path.items():
    if os.path.exists(v) is False:
        os.makedirs(v)
## 图片分析展示的列表
img_file_dict = {'data_analysis_res':os.path.join(pre_data_str, 'data_analysis_res'),}  # 注意每个项目有二级目录
img_pretext = '001_pretext.py'
########## 接受文件上传的目录
ac_dir_dict = {
'代码data目录':'data',
'数据目录':pre_data_str,
'readme':'readme',
}

########### fastapi_login
SECRET_KEY = '6b3a8722e818a07e6675777c105d502845b1a96f6bef69da774d5cbb6cc944f7'
PASSWORD_SALT = '497166f192bc8629d7449cf8ad8ea371331ebc2df53b1ee485cf0'  # 497166f192bc8629d7449cf8ad8ea371331ebc2df53b1ee485cf03db9279c3d9
def create_password_hash(str_passwd):
    res = hashlib.sha256( (str_passwd + PASSWORD_SALT).encode() ).hexdigest().lower()
    return res
users = {
"admin": {"password": create_password_hash('admin123'),"stop_list": [],},
"lvjinya": {"password": create_password_hash('123456'),"stop_list": ['operator_invoke', 'file_upload'],},
"guest": {"password": create_password_hash('123456'),"stop_list": ['file_tree', 'operator_invoke','file_upload','cs_js_pages'],},
}

def sign_data(data: str) -> str:
    '''Тhe function returns signed data; use hashlib library'''
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()

def get_username_from_signed_string(username_signed: str):
    '''The function returns a valid username from the hashed cookie'''
    username_base64, sign = username_signed.split('.')
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username

# print(get_username_from_signed_string('Z3Vlc3Q=.67AE3F14ED812F04A3E014D562735A8BA533A50738BF08F9CD251B61144941D0'))
