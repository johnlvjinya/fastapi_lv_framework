
import pandas as pd


df = pd.read_excel('test.xlsx')

print(df.columns.tolist())

df.index = df['_id']

res_dict1 = df.to_dict('index')

print(res_dict1)
print(type(res_dict1))
