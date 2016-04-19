#import _mysql
import time
from config import Parser


class MySQLDataBase(object):


	def __init__(self):
		self.config = Parser()
		self.connection = None


	def __connect(self):
		host = self.config.get('database', 'host')
		user = self.config.get('database', 'user')
		password = self.config.get('database', 'password')
		dbName = self.config.get('database', 'name')
		self.connection = _mysql.connect(
					host=host,user=user,
					passwd=password,db=dbName
				)
		return self.connection()


	def __disconnect(self):
		if self.connection:
			self.connection.close()
		self.connection = None


	def save_changes(self):
		if not self.connection:
			return False
		self.connection.commit()
		self.__disconnect()
		self.__connect()
		return True


	def __del__(self):
		self.__disconnect()


	def make_request(self, request, save=False, expectResult=True):
		if not self.connection:
			self.__connect()
		cursor = self.connection.cursor()
		state = cursor.execute(request)
		if not state:
			cursor.close()
			return None
		if expectResult:
			result = cursor.fetchall()
		if not result:
			result = []
		cursor.close()
		if save:
			self.save_changes()
		return result


	@property
	def tableName(self):
		return self.config.get('database', 'tablename')

	@property
	def primaryKey(self):
		return self.config.get('database', 'pkey')

	@property
	def types(self):
		return self.config.get('database', 'coltypes').split(',')

	@property
	def columns(self):
		return self.config.get('database', 'columns').split(',')


	def create_table(self):
		values = []
		for i, eachColumn in enumerate(self.columns):
			value = '%s %s '%(eachColumn, self.types[i])
			if eachColumn == self.primaryKey:
				value += 'AUTO_INCRECEMENT PRIMARY_KEY'
			values.append(value)
		
		sql = ''' CREATE TABLE %s (%s) ''' % (self.tableName, ', '.join(values))
		# remove the following prints
		print sql
		return self.make_request(sql, save=True)


	def get_all_values(self):
		sql = '''SELECT * FROM %s ''' % self.tableName
		# remove the following prints
		print sql
		return self.make_request(sql)


	def add_entry(self, username, value):
		timestamp = repr(time.strftime('%Y-%m-%d %H:%M:%S'))
		cols = self.columns
		vals = [username, value]
		if cols.count(self.primaryKey):
			cols.remove(self.primaryKey)
		if 'timestamp' in cols:
			vals.insert(cols.index('timestamp'), timestamp)
		sql = '''INSERT INTO %s (%s) VALUES (%s) '''%(self.tableName, ', '.join(cols[:len(vals)]), ', '.join(vals))
		# remove the following prints
		print sql
		self.make_request(sql, save=True)



