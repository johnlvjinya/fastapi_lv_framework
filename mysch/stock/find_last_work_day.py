

import time
import datetime
from chinese_calendar import is_workday, is_holiday


class FindLastWorkDay():
    def __init__(self):
        self.today_str = time.strftime('%Y-%m-%d',time.localtime(time.time()))  # 今天的日期
        self.year = int(self.today_str.split('-')[0])
        self.month = int(self.today_str.split('-')[1])
        self.day = int(self.today_str.split('-')[2])
        pass

    def find(self):
        today = datetime.date(self.year, self.month, self.day)
        sum_1 = 0
        i = 0
        while sum_1<1:
            i += 1
            day_i = today + datetime.timedelta(hours=-24*i)
            if is_workday(day_i):
                sum_1 += 1
        mydict = {"today":self.today_str, "last_work_day":str(day_i)}
        return mydict

    def run(self):
        res = self.find()
        print(res)
        pass

if __name__=='__main__':
    FindLastWorkDay().run()