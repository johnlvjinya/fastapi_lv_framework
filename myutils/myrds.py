


import pymysql.cursors




def rds_sql_res(
    host='rm-uf607qm8l57p67nl2uo.mysql.rds.aliyuncs.com',
    port=52319,
    user='bigdata', 
    password='j0^&WkpZbub#7tge',
    db = 'oms',
    sql=''' SELECT to_id,ow_create_username FROM `order_worksheet` where to_id in(1576627,1574990) and ow_type in (1,6,8,11) ''',
    ):

    conn=pymysql.connect(host=host,port=port,user=user,password=password,db=db) # ,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    return res


if __name__=='__main__':
    res = rds_sql_res()
    print(res)