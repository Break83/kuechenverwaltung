import re
import socket
from config import Parser

from usbDriver import USBScaleSingleton
from db import MySQLDataBase


class Server(object):

	__maxListen = 1
	__runServer = None

	@property
	def serverShouldRun(self):
		if self.__runServer == None:
			self.__runServer = True
		return self.__runServer

	def stop_server(self):
		self.__runServer = False
		return self.serverShouldRun


	def __init__(self):
		self.config = Parser()
		self.scale = USBScaleSingleton()
		self.db = MySQLDataBase()


	def get_weight(self):
		return self.scale.get_weight(self.scale.DATA_MODE_GRAMS)


	@property
	def host(self):
		return self.config.get('server', 'host')


	@property
	def port(self):
		return int(self.config.get('server', 'port'))


	def handle_request(self, request):
		rVal = ''
		if request == 'close server':
			self.stop_server()
			rVal = 'server about to stop..'
		elif request == 'get weight':
			rVal = str(self.get_weight())
		elif request.startswith('store weight'):
			args = re.split('\s+', request.replace('store result', ''))
			if args == ['']:
				args = ()
			self.store_value(*args)
		elif request == 'get all':
			self.db.get_all_values()
		else:
			rVal = 'request unknown.'
		return rVal


	def do_server_loop(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setblocking(1)
		self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.socket.bind( (self.host, self.port) )
		self.socket.listen(self.__maxListen)
		while self.serverShouldRun:
			try:
				request = ''
				response = ''
				clientsocket, address = self.socket.accept()
				clientsocket.setblocking(1)
				request = clientsocket.recv(4096)
				try:
					response = self.handle_request(request)
				except Exception, e:
					response = e
				clientsocket.send(str(response))
				clientsocket.close()
			except socket.error as e:
				print(
						'server closed with error:\n\t'+\
						'current request was: {0}\n\t'+\
						'current requestor was:{1}\n\t'+\
						'error was:{2}'.format(
								request,
								clientsocket,
								e
							)
					)
				break
		self.socket.close()


	def store_value(self, *args):
		value = self.get_weight()
		name = 'unknown'
		for eachArg in args:
			if re.match('^[0-9]*\.[0-9FE^]+$', eachArg, re.IGNORECASE):
				value = eachArg
			else:
				name = repr(eachArg)
		id = self.db.add_entry(name, value)
		return id


	def get_stored_values(self):
		return self.db.get_all_values()



