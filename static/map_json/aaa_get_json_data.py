


jsonMapData = {
    '中国': '/asset/get/s/data-1594956060000-wzSYdj4lt.json',
    '上海': '/asset/get/s/data-1594958113307-cxRUVth12.json',
    '河北': '/asset/get/s/data-1594957443106-mUbmYqE_T.json',
    '山西': '/asset/get/s/data-1594957766868-uxxAlaOQg.json',
    '内蒙古': '/asset/get/s/data-1594957676205-3QrKkEs35.json',
    '辽宁': '/asset/get/s/data-1594957651717-Gpv1HF9L3.json',
    '吉林': '/asset/get/s/data-1594957628423-QcNxuZC4W.json',
    '黑龙江': '/asset/get/s/data-1594957464890-ReTKD9z2j.json',
    '江苏': '/asset/get/s/data-1594957547861-KHdRNauVp.json',
    '浙江': '/asset/get/s/data-1594957975764-hU_4mjjCM.json',
    '安徽': '/asset/get/s/data-1594956457905-qkfohCrdY.json',
    '福建': '/asset/get/s/data-1594957317412-_IqC6cGfe.json',
    '江西': '/asset/get/s/data-1594957574860-XllJ4xelw.json',
    '山东': '/asset/get/s/data-1594957742389-8f6xMmJyc.json',
    '河南': '/asset/get/s/data-1594957480524-SL6qHJ-Fq.json',
    '湖北': '/asset/get/s/data-1594957504930-HOA-bJ-4Z.json',
    '湖南': '/asset/get/s/data-1594957530163-LdNpZfmvz.json',
    '广东': '/asset/get/s/data-1594957374153-nlVvqecih.json',
    '广西': '/asset/get/s/data-1594957389111-PYkaJMOc7.json',
    '海南': '/asset/get/s/data-1594957424894-jIDqZ7UZi.json',
    '四川': '/asset/get/s/data-1594957804051-2CAptA9LX.json',
    '贵州': '/asset/get/s/data-1594957404398-tHnBWFTJS.json',
    '云南': '/asset/get/s/data-1594957958466-t8sorr-Eh.json',
    '西藏': '/asset/get/s/data-1594957940133-OoVRveNig.json',
    '陕西': '/asset/get/s/data-1594957786745-Q7bywuAwG.json',
    '甘肃': '/asset/get/s/data-1594957335316-fAoKcplcm.json',
    '青海': '/asset/get/s/data-1594957718199-FGvYekca9.json',
    '宁夏': '/asset/get/s/data-1594957693688-bKgaSBp5A.json',
    '新疆': '/asset/get/s/data-1594957899456-0opYrqO1x.json',
    '北京': '/asset/get/s/data-1594956490489-Sr9M4AyTs.json',
    '天津': '/asset/get/s/data-1594957840497-nj8mwSNuj.json',
    '重庆': '/asset/get/s/data-1594957282133-TKWoEZjqH.json',
    '香港': '/asset/get/s/data-1594957863764-lSsoVf8U2.json',
    '澳门': '/asset/get/s/data-1594956484374-Els_HG1wo.json',
    '台湾': '/asset/get/s/data-1594957826344-_a_9jgYdN.json',
};


f_str = 'https://www.isqqw.com/'

import urllib.request

for k,v in jsonMapData.items():
    content = urllib.request.urlopen(f_str+v)
    str1 = content.read().decode()
    with open(k+'.json', 'w', encoding='utf-8') as f2:
        f2.write(str1)



