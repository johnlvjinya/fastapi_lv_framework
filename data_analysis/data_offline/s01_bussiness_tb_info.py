
import sys
sys.path.append('../..')
import os
import config
import pandas as pd
import myutils.db_one as mmp


class GetTableToExcel():
	def __init__(self):
		self.MOD = mmp.MysqlOneDatabase(host=config.host, 
			port=int(config.port), 
			user=config.user, 
			password=config.password, 
			db=config.db)

	def get_tb_rows_num(self, tb):
		sql = ''' 
		SELECT COUNT(*) FROM `%s`
		'''%tb
		rows_num = self.MOD.sql_select_one(sql)[0]
		# print('%s表行数'%tb, rows_num)
		return rows_num

	def get_all_tb_name(self):
		sql = '''
		SELECT TABLE_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '%s'
		'''%(config.db)
		res = [i[0] for i in self.MOD.sql_select_all(sql)]

		res1 = list(set(res))
		# print(res1[:10])
		res1.sort()
		return res1

	def get_tb_cols(self, tb):
		sql = '''
		SELECT COLUMN_NAME,column_comment FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'
		'''%(config.db, tb)
		cols_list = [i[0] for i in self.MOD.sql_select_all(sql)]
		cn_list = [i[1] for i in self.MOD.sql_select_all(sql)]
		return cols_list,cn_list

	def get_one_tb(self, tb, rows_n=None):
		rows_num = self.get_tb_rows_num(tb)
		
		cols_list,cn_list = self.get_tb_cols(tb)
		if rows_n is not None:
			limit_n = min(rows_n, rows_num)
			limit_str = 'limit %s'%str(limit_n)
		else:
			limit_str = ''
		sql = '''
		SELECT %s from %s %s
		'''%(','.join(cols_list), tb, limit_str)
		rows = self.MOD.sql_select_all(sql)
		df = pd.DataFrame(rows, columns=cn_list)
		# print(df)
		return df,rows_num

	def get_one_tb_col_en(self, tb, rows_n=None):
		rows_num = self.get_tb_rows_num(tb)
		
		cols_list,cn_list = self.get_tb_cols(tb)
		if rows_n is not None:
			limit_n = min(rows_n, rows_num)
			limit_str = 'limit %s'%str(limit_n)
		else:
			limit_str = ''
		sql = '''
		SELECT %s from %s %s
		'''%(','.join(cols_list), tb, limit_str)
		rows = self.MOD.sql_select_all(sql)
		df = pd.DataFrame(rows, columns=cols_list)
		# print(df)
		return df,rows_num


	def get_one_tb_all_to_pickle(self, tb):
		cols_list,cn_list = self.get_tb_cols(tb)
		sql = '''
		SELECT %s from %s
		'''%(','.join(cols_list), tb)
		rows = self.MOD.sql_select_all(sql)
		df = pd.DataFrame(rows, columns=cn_list)
		return df

	def get_db_tb_info(self, db_tb_list):
		df_rows = []
		max_len = 0
		loop_list = db_tb_list[:]  # 循环的表
		rows2 = []
		for tb in loop_list:
			print('正在获取表%s信息............'%tb)
			rows_num = self.get_tb_rows_num(tb)
			rows2.append([tb, rows_num])
			cols_list,cn_list = self.get_tb_cols(tb)
			df_rows.append([tb, rows_num]+cols_list)
			df_rows.append([tb+'_cn',rows_num]+cn_list)
			if len(cols_list)>max_len:
				max_len = len(cols_list)
		new_rows = []
		for row in df_rows:
			row += (max_len-len(row))*['']
			new_rows.append(row)
		# print(new_rows)
		df = pd.DataFrame(new_rows)
		df = df.T
		df.columns = df.iloc[0].tolist()

		df1 = df.drop(index=[0])  # 全量表字段
		df2 = pd.DataFrame(rows2, columns='表,行数'.split(','))
		return df1,df2

	def get_db_tb_info_ALL(self): # 获得数据库所有表的字段
		db_tb_list = self.get_all_tb_name()
		df1,df2 = self.get_db_tb_info(db_tb_list)
		f1_path = os.path.join(config.f_path['bussiness_tb_info'], '全部表字段.xlsx')
		df1.to_excel(f1_path, index=False)
		f2_path = os.path.join(config.f_path['bussiness_tb_info'], '全部表行数统计.xlsx')
		df2.to_excel(f2_path, index=False)

	def get_3d_mbpp_tb_by_input_excel(self): # 获得算法相关表的测试数据
		f_path = os.path.join(config.ROOT_PATH, 'data/input_seatable_业务表信息维护.xlsx')
		df1 = pd.read_excel(f_path).fillna('')

		f2_path = os.path.join(config.f_path['bussiness_tb_info'], '算法相关表样例数据.xlsx')
		writer=pd.ExcelWriter(f2_path)
		for i in range(df1.shape[0]):
			# print(df['算法模块'][i], type(df['算法模块'][i]))
			if '箱型选择' in df1['算法模块'][i]:
				tb = df1['表'][i]
				print('正在获取表：', tb)
				df,rows_num = self.get_one_tb(tb, 100)  # 得到样例数据
				df.to_excel(writer,sheet_name=tb[:30],index=False)

				# df_all = self.get_one_tb_all_to_pickle(tb)
				# df_all.to_picle('output/%s.pickle'%tb)
		writer.save() 


	def run(self):
		self.get_db_tb_info_ALL()


if __name__=='__main__':
	GetTableToExcel().run()
