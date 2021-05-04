import pickle
import datetime
import os

'''
Status DB values

None = Just sent to the DB
Preparing = Order has been seen and is being prepared
Ready = Order is prepared and ready for collection
Collected = Order has been collected and transaction is succesfull

  
sent = []
  
# Instance the Fernet class with the key
with open("sentorders.pickle", "wb") as pickle_out:
	pickle.dump(sent, pickle_out)
'''  
# Open user pickle
if os.path.getsize("sentorders.pickle") > 0:
	with open("sentorders.pickle", "rb") as pickle_in:
		sentorders = pickle.load(pickle_in)
		print(sentorders)
else:
	print("The file is empty")