

import redis
import pickle

class MyRedis():

    def __init__(self, host='127.0.0.1'):
        self.rs = redis.StrictRedis(host=host)
        print('redis中keys', self.rs.keys())

    @property
    def get_test_df(self):
        import pandas as pd
        df=pd.DataFrame([range(5)]*5,index=list('HELLO'),columns=list('HELLO'))
        return df

    # save_key:保存的键， data保存的数据， 保存的名称
    def save_data(self, d_name, d_data):
        self.rs.set(d_name, pickle.dumps(d_data))   # 将数据Pickle化            

    def get_data(self, d_name):
        return pickle.loads(self.rs.get(d_name))
        
    def clear_all_keys(self):
        keys = self.rs.keys()
        for key in keys:
            self.rs.delete(key)
            print('delete......................', key)

    def print_all_keys(self):
        keys = self.rs.keys()
        for key in keys:
            print(key,'*******print\n', self.get_data(key))        

    def run(self):
        self.clear_all_keys()
        self.save_data('test_df', self.get_test_df)
        self.save_data('test_str', '保存字符串')
        self.save_data('test_num', 1)
        print('==========================')
        self.print_all_keys()   # 打印
        self.clear_all_keys()   # 删除
        self.print_all_keys()   # 再打印
        pass

if __name__=="__main__":
    MyRedis().run()