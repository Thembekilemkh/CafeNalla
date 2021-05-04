import pymysql
import mysql.connector
from mysql.connector import Error
import threading
from kivy.clock import Clock, mainthread
from user import User
from queue import Queue

class SendOrder():
	def __init__(self, **kwargs):
		super(SendOrder, self).__init__()
		conQ = kwargs['conQ']
		try:
			#self.db = pymysql.connect(host="mysql-10652-0.cloudclusters.net" ,user="ThembekileCEO", password="==h2e=lnm=Fh" , database="llenobacktester_db2", port=10652)
			self.db = mysql.connector.connect(host="localhost", user="thembekile", password="LlenoCEO#5", database="cafenalla", port="33162")
			print("connected!!")           
			conQ.put(True)

			self.cursor = self.db.cursor()

			#Getting our tables
			self.user_table = "user"
			self.orders_table = "orders"

		except Exception as e:
			if isinstance(e, pymysql.err.OperationalError):
				print(f'This baby operational: {e}')
				conQ.put(False)
			else:
				print(f'This baby not operational: {e}')
				conQ.put(False)

	def send_order(self, **kwargs):
		orders=kwargs['order']
		progress=kwargs['progress']
		pb=kwargs['pb']
		user=kwargs['user']
		date=kwargs['date']
		time=kwargs['time']
		update_pb = kwargs['update_pb']
		proQue = kwargs['progressQ']
		home_float=kwargs['home_float']; sentQ = kwargs['sentQ']

		user_id = user.user_id
		orders_sent = []

		proQue.put(progress+10)
		progress = progress+10
		update_pb(pb, proQue)

		pb_increment = 70/len(orders)
		for o in range(len(orders)):
			order = orders[o]
			for meal_group, val in order.items():
				if meal_group == 'Breakfast' or meal_group == 'Salads':
					sent_order = {meal_group:{'Meal':{},
												'Add_ons':{},
												'Status':{}}}
					meal_ = orders[o][meal_group]['Meal']
					add_ons_ = orders[o][meal_group]['Add_ons']
					status_ = orders[o][meal_group]['Status']

					sent_order[meal_group]['Meal'] = meal_
					sent_order[meal_group]['Add_ons'] = add_ons_
					sent_order[meal_group]['Status'] = 'Sent'

					price = 0
					ingredients = ''
					meal_name = ''
					for key, val in meal_.items():
						meal_name = key
						price = meal_[key]['price']
						ingredients = meal_[key]['ingredients']

					add_ons_price = 0
					add_on = ''
					if len(list(add_ons_.keys())) > 0:
						for key, val in add_ons_.items():
							if key == list(add_ons_.keys())[-1]:
								add_on = add_on+key
								add_ons_price = add_ons_price+val
							else:
								add_on = add_on + key +", "
								add_ons_price = add_ons_price+val
					else:
						add_on = 'None'

					# Insert order to DB
					insert_order_to_db = f"""INSERT INTO {self.orders_table}(
										user_id, Meal_Name, Meal_Group, Ingredients,
										Status, Meal_Price, Addon_Name, Addon_Price, 
										collection_date, order_date)
										VALUES({user_id}, '{meal_name}', '{meal_group}',
										'{ingredients}', 'None', {str(price)}, '{add_on}',
										{add_ons_price}, '{str(date)} {str(time)}', now());
										"""
					try:
						self.cursor.execute(insert_order_to_db)

						self.db.commit()
						orders_sent.append(sent_order)

					except Exception as e:
						print(f'Failed to upload Breakfast and salads: {e}')
						self.db.rollback()

				elif meal_group == 'Meals':
					sent_order = {}

					sent_order = {meal_group:{'Add_ons':{},
												'Status':{}}}
					mealType = orders[o][meal_group]
					add_ons_ = orders[o][meal_group]['Add_ons']
					status_ = orders[o][meal_group]['Status']
					orders[o][meal_group].pop('Add_ons', None)
					orders[o][meal_group].pop('Status', None)

					sent_order[meal_group]['Add_ons'] = add_ons_
					sent_order[meal_group]['Status'] = 'Sent'

					price = 0
					ingredients = ''
					meal_name = ''
					meal_type = ''
					for meal_type, val in mealType.items():
						sent_order[meal_group][meal_type] = {'Meal':{}}
						meal_type = meal_type
						for k, v in mealType[meal_type]['Meal'].items():
							meal_name = k
							price = mealType[meal_type]['Meal'][k]['price']
							ingredients = mealType[meal_type]['Meal'][k]['ingredients']
							
							sent_order[meal_group][meal_type]['Meal'][k] = mealType[meal_type]['Meal'][k]

					add_ons_price = 0
					add_on = ''
					if len(list(add_ons_.keys())) > 0:
						for key, val in add_ons_.items():
							if key == list(add_ons_.keys())[-1]:
								add_on = add_on+key
								add_ons_price = add_ons_price+val
							else:
								add_on = add_on + key +", "
								add_ons_price = add_ons_price+val
					else:
						add_on = 'None'
					
					# Insert order to DB
					insert_order_to_db = f"""INSERT INTO {self.orders_table}(
										user_id, Meal_Name, Meal_Group, Meal_Type, Ingredients,
										Status, Meal_Price, Addon_Name, Addon_Price, 
										collection_date, order_date)
										VALUES({user_id}, '{meal_name}', '{meal_group}','{meal_type.replace("'", "^")}',
										'{ingredients}', 'None', {str(price)}, '{add_on}',
										{add_ons_price}, '{str(date)} {str(time)}', now());
										"""
					try:
						print(insert_order_to_db)
						self.cursor.execute(insert_order_to_db)

						self.db.commit()

						# Get order id
						get_order_id = f"""SELECT id FROM {self.orders_table} WHERE CAST(order_date AS TIME) >= SUBTIME(CURRENT_TIME, '00:00:45')
										AND CAST(order_date AS TIME) <= CURRENT_TIME
										AND user_id = '{user_id}'; """
						try:
							self.cursor.execute(get_order_id)

							for row in self.cursor:
								order_id =row[0]

							sent_order['order_id'] = order_id
							print('order id: ', str(order_id))
							orders_sent.append(sent_order)

						except Exception as e:
							print(f'Failed to find order id: {e}')
							self.db.rollback()

					except Exception as e:
						print(f'Failed to upload Meals: {e}')
						self.db.rollback()

				elif meal_group == 'Smoothies' or meal_group == 'Shakes' or meal_group == 'Something_cold':
					sent_order = {}
					meal_ = orders[o][meal_group]
					status_ = orders[o][meal_group]['Status']
					meal_.pop('Status', None)

					sent_order[meal_group]['Status'] = 'Sent'

					price = 0
					ingredients = ''
					meal_name = ''
					add_ons_price = 0
					add_on = ''
					print(meal_)
					for key, val in meal_.items():
						if key != 'Status':
							meal_name = key
							price = meal_[meal_name]['price']
							ingredients = meal_[meal_name]['ingredients']
							sent_order[meal_group][meal_name] = meal_[meal_name]
							sent_order[meal_group]['Extras'] = meal_[key]['Extras']

							if len(list(meal_[key]['Extras'].keys())) > 0:
								for vey, val in add_ons_.items():
									if vey == list(meal_[key]['Extras'].keys())[-1]:
										add_on = add_on+vey
										add_ons_price = add_ons_price+val
									else:
										add_on = add_on + vey +", "
										add_ons_price = add_ons_price+val
							else:
								add_on = 'None'

					# Insert order to DB
					insert_order_to_db = f"""INSERT INTO {self.orders_table}(
										user_id, Meal_Name, Meal_Group, Ingredients,
										Status, Meal_Price, Addon_Name, Addon_Price, 
										collection_date, order_date)
										VALUES({user_id}, "{meal_name}", '{meal_group}',
										'{ingredients}', 'None', {str(price)}, '{add_on}',
										{add_ons_price}, '{str(date)} {str(time)}', now());
										"""
					try:
						self.cursor.execute(insert_order_to_db)

						self.db.commit()
						orders_sent.append(sent_order)

					except:
						print(f'Failed to upload drinks: {e}')
						self.db.rollback()

			proQue.put(progress+pb_increment)
			progress = progress+pb_increment
			update_pb(pb, proQue)

		home_float.remove_widget(pb)
		self.db.close()

		sentQ.put(orders_sent)