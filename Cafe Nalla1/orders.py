import pickle
import os

class Orders():
	def __init__(self):
		self.orders = []
		try:
			# Open the menu pickle
			if os.path.getsize('bin\\orders.pickle')>0:
				with open('bin\\orders.pickle', 'rb') as pickle_in:
					self.orders = pickle.load(pickle_in)
					
		except Exception as e:
			pass

	def save_new_orders(self, orders):
		with open('bin\\orders.pickle', 'wb') as pickle_out:
			pickle.dump(orders, pickle_out)

