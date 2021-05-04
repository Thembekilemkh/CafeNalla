import pymysql
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet
import pickle
import datetime
import os 

class Enquiry():

	def __init__(self,*arg,**kwargs):
		conQ = kwargs['conQ']
		self.heading = kwargs['heading_lbl']
		self.bigPoppa = kwargs['bigPoppa']

		print("In the __init__")
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
			conQ.put("Failed to create account, check your connection")


	def incoming_enquiries(self, **kwargs):
		# Find all orders associated with this user
		user = kwargs['user']

		found_orders = False
		got_orders = False

		user_id = user.user_id
		order_ids = []

		if user_id >= 1:
			find_orders = f"""SELECT id FROM {self.orders_tables} WHERE 
							  Status = 'None' OR Status = 'Preparing'
						  	  OR Status = 'Ready'"""

			try:
				self.cursor.execute(find_orders)

				for row in self.cursor:
					order_ids.append(row[0])
					found_orders = True

			except Exception as e:
				print(f'Failed to find order ids: {e}')

			if found_orders == True:
				sent_orders = []
				for id_ in order_ids:
					sent_order = {}
					get_order = f"""SELECT Meal_Group, Meal_Name, Meal_Price, Ingredients,
									Addon_Name, Addon_Price, Status, Meal_Type,
									collection_date, order_date FROM {self.orders_tables}
									WHERE id ={str(id_)}"""


					try:
						self.cursor.execute(get_order)

						for row in self.cursor:
							order_ = {'Meal_Group':row[0],
									  'Meal_Name':row[1],
									  'Meal_Price':row[2],
									  'Ingredients':row[3],
									  'Addon_Name':row[4],
									  'Addon_Price':row[5],
									  'Status':row[6],
									  'Meal_Type':row[7],
									  'collection_date':row[8],
									  'order_date':row[9]}

							if order_['Meal_Group'] == 'Breakfast' or order_['Meal_Group']=='Salads':
								meal_group = order_['Meal_Group']
								meal = order_['Meal_Name']
								addon_name = order_['Addon_Name']
								addon_price = order_['Addon_Price']
								meal_price = order_['Meal_Price']
								ingredients = order_['Ingredients']

								sent_order[meal_group] = {}
								sent_order[meal_group][meal] = {}
								sent_order[meal_group]['Add_ons'] = {addon_name:addon_price}
								sent_order[meal_group]['Status'] = order_['Status']
								sent_order[meal_group]['collection_date'] = order_['collection_date']
								sent_order[meal_group]['order_date'] = order_['order_date']
								sent_order[meal_group]['id'] = id_

								sent_order[meal_group][meal]['price'] = meal_price
								sent_order[meal_group][meal]['ingredients'] = ingredients

							elif order_['Meal_Group'] == 'Meals':
								meal_group = order_['Meal_Group']
								meal_type = order_['Meal_Type']
								addon_name = order_['Addon_Name']
								addon_price = order_['Addon_Price']
								meal = order_['Meal_Name']
								meal_price = order_['Meal_Price']
								ingredients = order_["Ingredients"]

								sent_order[meal_group] = {}
								sent_order[meal_group][meal_type] = {}
								sent_order[meal_group]['Add_ons'] = {addon_name:addon_price}
								sent_order[meal_group]['Status'] = order_['Status']
								sent_order[meal_group]['collection_date']= order_['collection_date']
								sent_order[meal_group]['order_date'] = order_['order_date']
								sent_order[meal_group]['id'] = id_

								sent_order[meal_group][meal_type][meal] = {'price':meal_price,
																		   'ingredients':ingredients}

							elif order_['Meal_Group'] == 'Smoothies' or order_['Meal_Group'] == 'Shakes' or order_['Meal_Group'] == 'Something_cold':
								meal_group = order_['Meal_Group']
								sent_order[order_['Meal_Group']] = {}
								sent_order[order_['Meal_Group']]['Status'] = order_['Status']
								sent_order[order_['Meal_Group']]['Extras'] = {order_['Addon_Name']: order_['Addon_Price']}

								meal = order_['Meal_Name']
								ingredients = order_['Ingredients']
								price = order_['Meal_Price']
								sent_order[order_['Meal_Group']][meal] = {}
								sent_order[meal_group]['Status'] = order_['Status']
								sent_order[meal_group]['collection_date']= order_['collection_date']
								sent_order[meal_group]['order_date'] = order_['order_date']
								sent_order[meal_group]['id'] = id_
								sent_order[order_['Meal_Group']][meal]['price'] = price
								sent_order[order_['Meal_Group']][meal]['ingredients'] = ingredients

							sent_orders.append(sent_order)
					except Exception as e:
						print(f'Failed to obtain orders: {e}')
				got_orders = True
				return sent_orders
				
		else:
			return 'Access Denied'

	def user_creation(self,** kwargs):
		pass

	def order_enquiries(self, **kwargs):
		# Find all orders associated with this user
		user = kwargs['user']

		found_orders = False
		got_orders = False

		user_id = user.user_id
		order_ids = []
		find_orders = f"""SELECT id FROM {self.orders_tables} WHERE
						  user_id = {user_id} AND Status = 'None' OR Status = 'Preparing'
						  OR Status = 'Ready'"""

		try:
			self.cursor.execute(find_orders)

			for row in self.cursor:
				order_ids.append(row[0])
				found_orders = True

		except Exception as e:
			print(f'Failed to find order ids: {e}')

		if found_orders == True:
			sent_orders = []
			for id_ in order_ids:
				sent_order = {}
				get_order = f"""SELECT Meal_Group, Meal_Name, Meal_Price, Ingredients,
								Addon_Name, Addon_Price, Status, Meal_Type,
								collection_date, order_date FROM {self.orders_tables}
								WHERE id ={str(id_)}"""


				try:
					self.cursor.execute(get_order)

					for row in self.cursor:
						order_ = {'Meal_Group':row[0],
								  'Meal_Name':row[1],
								  'Meal_Price':row[2],
								  'Ingredients':row[3],
								  'Addon_Name':row[4],
								  'Addon_Price':row[5],
								  'Status':row[6],
								  'Meal_Type':row[7],
								  'collection_date':row[8],
								  'order_date':row[9]}

						if order_['Meal_Group'] == 'Breakfast' or order_['Meal_Group']=='Salads':
							meal_group = order_['Meal_Group']
							meal = order_['Meal_Name']
							addon_name = order_['Addon_Name']
							addon_price = order_['Addon_Price']
							meal_price = order_['Meal_Price']
							ingredients = order_['Ingredients']

							sent_order[meal_group] = {}
							sent_order[meal_group][meal] = {}
							sent_order[meal_group]['Add_ons'] = {addon_name:addon_price}
							sent_order[meal_group]['Status'] = order_['Status']
							sent_order[meal_group]['collection_date'] = order_['collection_date']
							sent_order[meal_group]['order_date'] = order_['order_date']
							sent_order[meal_group]['id'] = id_


							sent_order[meal_group][meal]['price'] = meal_price
							sent_order[meal_group][meal]['ingredients'] = ingredients

						elif order_['Meal_Group'] == 'Meals':
							meal_group = order_['Meal_Group']
							meal_type = order_['Meal_Type']
							addon_name = order_['Addon_Name']
							addon_price = order_['Addon_Price']
							meal = order_['Meal_Name']
							meal_price = order_['Meal_Price']
							ingredients = order_["Ingredients"]

							sent_order[meal_group] = {}
							sent_order[meal_group][meal_type] = {}
							sent_order[meal_group]['Add_ons'] = {addon_name:addon_price}
							sent_order[meal_group]['Status'] = order_['Status']
							sent_order[meal_group]['collection_date']= order_['collection_date']
							sent_order[meal_group]['order_date'] = order_['order_date']
							sent_order[meal_group]['id'] = id_

							sent_order[meal_group][meal_type][meal] = {'price':meal_price,
																	   'ingredients':ingredients}

						elif order_['Meal_Group'] == 'Smoothies' or order_['Meal_Group'] == 'Shakes' or order_['Meal_Group'] == 'Something_cold':
							meal_group = order_['Meal_Group']
							sent_order[order_['Meal_Group']] = {}
							sent_order[order_['Meal_Group']]['Status'] = order_['Status']
							sent_order[order_['Meal_Group']]['Extras'] = {order_['Addon_Name']: order_['Addon_Price']}

							meal = order_['Meal_Name']
							ingredients = order_['Ingredients']
							price = order_['Meal_Price']
							sent_order[order_['Meal_Group']][meal] = {}
							sent_order[meal_group]['Status'] = order_['Status']
							sent_order[meal_group]['collection_date']= order_['collection_date']
							sent_order[meal_group]['order_date'] = order_['order_date']
							sent_order[meal_group]['id'] = id_
							sent_order[order_['Meal_Group']][meal]['price'] = price
							sent_order[order_['Meal_Group']][meal]['ingredients'] = ingredients

						sent_orders.append(sent_order)
				except Exception as e:
					print(f'Failed to obtain orders: {e}')
			got_orders = True
			return sent_orders
		return got_orders