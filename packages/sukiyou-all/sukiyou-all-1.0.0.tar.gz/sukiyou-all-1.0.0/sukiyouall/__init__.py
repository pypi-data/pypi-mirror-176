import os

t_path = '../../../../'
# t_path = './'

dir_list = [
	'bin',
	'config',
	'core',
	'interface',
	'lib',
	'log',
	'models',
	'test',
]
for x in dir_list:
	try:
		os.mkdir(t_path + x)
	except:
		pass

with open(t_path + 'config/db.ini', 'w', encoding='utf-8') as f:
	pass

with open(t_path + 'core/errorlog.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''
import os
import time


class errorlogs:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件目录
		self.ConfigPath = os.path.join(self.BASE_DIR, '../log')  # 自己的配置文件路径，根据项目需求，这里是--> 在当前目录下的config下存放目录文件
		self.file_name = "app_err_log.txt"
		self.file_path = os.path.join(self.ConfigPath, self.file_name)

	def writeLog(self, path, method, text, status):
		writetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		file = open(self.file_path, 'a+', encoding='utf8')
		str='[ time=> (' + writetime + ') ] - [ method=>' + method + ' ] - [ path=>' + path + ' ] - [ error_code=> ' + status + ' ] - [ error_message=> { ' + text + ' } ]  \n'
		file.write(str)
		file.close()

	def _test1(self):
		...

	def __test1(self):
		...


# if __name__ == '__main__':
# 	a = errorlogs().writeLog('/asdg/asdgasdg', 'POST', '测试字符串', '0')

		'''
	)

with open(t_path + 'interface/interface_import.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''
#
		'''
	)

with open(t_path + 'lib/config_r.py', 'w', encoding='utf-8') as f:
	f.write(
		r'''
# -*- coding: utf-8 -*-
import configparser
import os


class readini:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件目录
		self.ConfigPath = os.path.join(self.BASE_DIR, '../config')  # 自己的配置文件路径，根据项目需求，这里是--> 在当前目录下的config下存放目录文件
		self.slat = "IchLiebeWangLanPink"
		self.conf = configparser.ConfigParser()
		self.file_name = "db.ini"
		self.file_path = os.path.join(self.ConfigPath, self.file_name)
		...

	def readr(self, pal='mysql'):
		"""
		:param pal: sectionName
		:return:
		"""
		self.conf.read(self.file_path, encoding="utf-8")  # python3
		res = self.conf.items(pal)
		t = {}
		for x in res:
			x = list(x)
			p = {x[0]: x[1]}
			t.update(p)
		return t

		'''
	)

with open(t_path + 'lib/database_conn.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
import datetime
import json

from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from lib.config_r import readini

DB_INFO = readini().readr()
engine = create_engine(f"mysql+pymysql://{DB_INFO.get('user')}:{DB_INFO.get('pwd')}"
					   f"@{DB_INFO.get('host')}/{DB_INFO.get('dbname')}?",
					   echo=False,
					   pool_recycle=10,
					   pool_size=10,
					   max_overflow=5,
					   pool_timeout=10,
					   isolation_level="READ UNCOMMITTED"
					   )

SQLALCHEMY_POOL_RECYCLE = 10
SQLALCHEMY_POOL_TIMEOUT = 10

Base = declarative_base()

# 创建session
DbSession = sessionmaker(bind=engine)
session = DbSession()

if session:
	print("The database connection was initialized successfully. Procedure")




class CUdr:

	def __init__(self):
		pass

	@classmethod
	def insert(cls, emps):
		'''
		emps = Store_score(
			store_id=store_id,
			class . column = val
		)
		'''
		try:
			session.add(emps)
			session.commit()
			return True
		except Exception as e:
			print(f"e==>{e} <=")
			session.rollback()
			return False

	# finally:
	# session.close()

	@classmethod
	def delete_real(cls, filter):
		try:
			res = session.query(cls)
			for x in filter:
				res = res.filter(x)

			res.delete()
			session.commit()
			return True
		except:
			session.rollback()
			return False

	# finally:
	#     session.close()

	@classmethod
	def delete(cls, filter):
		try:
			res = session.query(cls)
			for x in filter:
				res = res.filter(x)
			update = {
				'is_use': 0
			}
			res.update(update)
			session.commit()
			return True
		except:
			session.rollback()
			return False

	# finally:
	#     session.close()

	@classmethod
	def update(cls, filter, update: dict):
		'''
		:param filter: 查询条件
		:param update: 更改内容
		:return:
		:ex.
				update = {
					'nick_name': nick_name,
					'phone': phone
				}
				filter = {User.id == id}
		'''
		try:
			res = session.query(cls)
			for x in filter:
				res = res.filter(x)
			# res = res.filter(filter)
			res.update(update)
			session.commit()
			return True
		except:
			session.rollback()
			return False

	# finally:
	#     session.close()

	@classmethod
	def __other_info(cls):
		res = session.query(cls).count()
		return res

	@classmethod
	def fetch_all(cls, limit=False, group=False, order: tuple = False, filter: dict = False):
		last_page = 'no limit'

		res = session.query(cls)
		if filter:
			for x in filter:
				res = res.filter(x)
		if group:
			res = res.group_by(group)
		if order:
			if order[1]:
				res = res.order_by(order[0].desc())
			else:
				res = res.order_by(order[0])
		if limit:
			start = (limit[0] - 1) * limit[1]
			stop = limit[0] * limit[1]
			try:
				res2 = res.slice(start, stop).all()
			except:
				session.rollback()
				res2 = res.slice(start, stop).all()
			res_len = len(res2)
			last_page = False
			if res_len < limit[1]:
				last_page = True
			res = res.slice(start, stop)
		try:
			res = res.all()
		except:
			session.rollback()
			res = res.all()
		session.flush()
		a = []
		for x in res:
			x = cls.to_dict(x)
			a.append(x)
		count = cls.__other_info()
		result = {
			"list": a,
			"list_length": len(res),
			"total_count": count,
			"lastPage": last_page
		}
		# session.close()
		return result

	@classmethod
	def fetch_one(cls, limit=False, group=False, order: tuple = False, filter=False):
		res = session.query(cls)
		if filter:
			for x in filter:
				res = res.filter(x)
		try:
			res = res.first()
		except:
			session.rollback()
			res = res.first()
		# count = cls.__other_info()
		session.flush()
		result = {
			"list": cls.to_dict(res),
		}
		# session.close()
		return cls.to_dict(res)

	def __repr__(self):
		fields = self.__dict__
		if "_sa_instance_state" in fields:
			del fields["_sa_instance_state"]

		return json.dumps(fields, cls=DateEncoder, ensure_ascii=False)

	@classmethod
	def to_dict(cls, obj):
		if obj is None:
			return None
		d = dict()
		for c in cls.__table__.columns:
			v = getattr(obj, c.name)
			if c.name == "create_time" or c.name == 'update_time':
				v = v.strftime("%Y-%m-%d %H:%M:%S")
			d[c.name] = v
		return d


# 处理json格式化时 时间问题
class DateEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime("%Y-%m-%d %H:%M:%S")
		else:
			return json.JSONEncoder.default(self, obj)


"""
	)
with open(t_path + 'lib/main_app.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
import base64
import json
import os
import uuid

from flask import Flask, request, render_template, url_for
from flask_cors import *
from werkzeug.utils import secure_filename, redirect
from flask import g
from core.errorlog import errorlogs

#  init server system
app = Flask(__name__)
CORS(app, supports_credentials=True)  # 设置跨域

# init log system
__log__ = errorlogs()


@app.route('/', methods=['POST', 'GET'])
def test():
	path = request.path
	return "这里发生了一些错误"


@app.after_request
def __after__(response):
	# ------------------- 定义返回值 -----------------------------------------
	try:
		if type(eval(response.data)) is list or type(eval(response.data)) is dict:
			msg = "success"
			if g.get('message'):
				msg = g.get('message')
			response.data = json.dumps({"message": msg, "code": '0', 'data': eval(response.data)})
			error_code = 200
		else:
			msg = response.data.decode('utf-8')
			response.data = json.dumps(
				{"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8')+" ]", "code": '0',
				 'data': False})
			error_code = 500
	except:
		msg = response.data.decode('utf-8')
		response.data = json.dumps(
			{"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8')+" ]", "code": '0', 'data': False})
		error_code = 500
	# -------------------- 写日志 ---------------------------------------------
	__log__.writeLog(request.path, request.method, str(msg), str(error_code))
	return response

"""
	)
with open(t_path + 'lib/public.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
import time
import json

def get_loca_time():
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
"""
	)
with open(t_path + 'log/sukiyou.sukiyou', 'w', encoding='utf-8') as f:
	f.write(
		r'''
#
		'''
	)
with open(t_path + 'models/create_model.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
import os

table_list = [
]
for x in table_list:
	print(x + '\r')
	command = "sqlacodegen  --outfile " + x + ".py --table " + x + " mysql+pymysql://seven_pyp_conf:GG6L2eEJmWm6c42m@222.186.150.48:3306/seven_pyp_conf?charset=utf8"
	os.system(command)

"""
	)
with open(t_path + 'models/ex_import.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
from lib.database_conn import *
from lib.public import *
from sqlalchemy import *
from sqlalchemy.dialects.mysql import *

import hashlib
"""
	)

with open(t_path + 'app.py', 'w', encoding='utf-8') as f:
	f.write(
r"""
from lib.main_app import app, g, __log__
# main_app 内包含一个 '/' 路由用于测试服务是否启动成功
#				一个 after_request方法, 重新格式化返回值及写流水日志
#
# -----------------------------------------------
# -----------------------------------------------
app.run(port=12369, host='0.0.0.0', debug=True)
"""
	)
