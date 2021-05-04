import pickle
import datetime
import os

'''
Status DB values

None = Just sent to the DB
Preparing = Order has been seen and is being prepared
Ready = Order is prepared and ready for collection
Collected = Order has been collected and transaction is succesfull'''

  
incomingorders = []
  
# Instance the Fernet class with the key
with open("incomingorders.pickle", "wb") as pickle_out:
	pickle.dump(incomingorders, pickle_out)
'''  
# Open user pickle
if os.path.getsize("incomingorders.pickle") > 0:
	with open("incomingorders.pickle", "rb") as pickle_in:
		incomingorders = pickle.load(pickle_in)
		print(incomingorders)
else:
	print("The file is empty")

'''