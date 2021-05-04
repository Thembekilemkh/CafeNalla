import pickle
import datetime
import os
'''
orders = []


#UNMUTE TO CREATE UPDATE MENU
with open('orders.pickle', 'wb') as pickle_out:
	pickle.dump(orders, pickle_out)
	print("Dumped")

'''

with open('orders.pickle', 'rb') as pickle_in:
	myOrders = pickle.load(pickle_in)
	print('Orders: ', myOrders)
