import os
import pickle
import pymysql
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

class UpdateDB():
	def __init__(self, **kwargs):
		conQ = kwargs['conQ']
		try:
			#self.db = pymysql.connect(host="mysql-10652-0.cloudclusters.net" ,user="ThembekileCEO", password="==h2e=lnm=Fh" , database="llenobacktester_db2", port="10652")
			self.db = mysql.connector.connect(host="localhost", user="thembekile", password="LlenoCEO#5", database="cafenalla", port="33162")
			conQ.put(True)

			self.cursor = self.db.cursor()

			#Getting our tables
			self.user_table = "user"
			self.orders_tables = 'orders'
			self.stats_table = "stats"

		except pymysql.err.OperationalError:
			print("Failed network connection")
			conQ.put(False)

	def update_status(self, **kwargs):
		user=kwargs['user']
		new_status=kwargs['new_status']
		id_=['id_']

		update_query = f"""UPDATE {self.orders_tables} SET Status = {new_status} WHERE id = {id_};"""

		try:
			self.cursor.execute(update_query)
			self.db.commit()

			return True

		except Exception as e:
			print(f'Failed to find order ids: {e}')

		return False

