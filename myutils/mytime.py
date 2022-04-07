


import pandas as pd
from datetime import datetime

now = datetime.now()                # current date and time

today1 = now.strftime("%H:%M:%S")
print('今天的日期：', today1)

date_time = now.strftime("%Y-%m-%dT%H:%M:%S")
print("date and time:",date_time)

###### 时间戳
rows = [[1471248120, 1534404000],[1471248120, 1534404000]]
df = pd.DataFrame(rows, columns=['p_time','d_time'])
df['t1']=pd.to_datetime(df['p_time'].values, unit='s', utc=True).tz_convert('Asia/Shanghai').strftime("%Y-%m-%d %H:%M:%S")
df['t2']=pd.to_datetime(df['d_time'].values, unit='s', utc=True).tz_convert('Asia/Shanghai').strftime("%Y-%m-%d %H:%M:%S")
df['t3'] = ['2022-01-13 15:20:00', '2022-01-13 5:20:00']


import time
x = '2022-03-01'
t_stamp = time.mktime(time.strptime(x,'%Y-%m-%d'))
print(t_stamp)

# 1471248120
# 1642003200

# df.to_excel('test.xlsx', index=False)
x = pd.to_datetime(df['t3']).dt
df['weekday'] = x.dayofweek+1
df['year'] = x.year
df['month'] = x.month
df['hour'] = x.hour
df['before_noon'] = df['hour'].apply(lambda x: 1 if x<12 else 0)

print(df)
