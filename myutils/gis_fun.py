
import re
import requests
from math import radians, cos, sin, asin, sqrt

def get_address_gis(address_name):      # 高德地图获得经纬度
    ###### key的来源为高德地图，参考： https://console.amap.com/dev/key/app
    url = 'https://restapi.amap.com/v3/geocode/geo?address=%s&output=XML&key=abc30d0e3cddad8c248d6d9008ef9ad2'%address_name
    response  = requests.get(url)
    res1 = re.findall(r'<location>(.*?)</location>', response.text)
    res2 = [float(i) for i in res1[0].split(',')]
    return res2

def geodistance(lng1,lat1,lng2,lat2):
    #lng1,lat1,lng2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    distance=round(distance/1000,3)
    return distance

if __name__=='__main__':
    res1 = get_address_gis('北京市朝阳区阜通东大街6号')  ############ 函数
    print(res1)
    print(geodistance(121.473701, 31.230416, 120.585315, 31.298886))