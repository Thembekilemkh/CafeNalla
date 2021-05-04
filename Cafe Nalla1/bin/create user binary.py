import pickle
import datetime
import os

'''
#THE USER DICTIONARY
# Create user

user = {
	"user_id":4,
	"first_name":"Thembekile",
	"last_name":"Mkhombo",
	"email": "thembekile47@gmail.com",
	"password": "p@$$w0rd",
	"logged_on":True,
	"loyalty_points":0,
	"regular_drink":None, 
	"admin":2
}


user = {
	"user_id":None,
	"first_name":None,
	"last_name":None,
	"email": None,
	"password": None,
	"logged_on":False,
	"loyalty_points":None,
	"regular_drink":None, 
	"admin":0
}
'''
# ONLY UNMUTE IF YOU WANT TO MAKE CHANGE TO THE USER OBECT
with open("user.pickle", "wb") as pickle_out:
	pickle.dump(user, pickle_out)
	print(f'user: {user}')

'''
# Open user pickle
if os.path.getsize("user.pickle") > 0:
	with open("user.pickle", "rb") as pickle_in:
		myUser = pickle.load(pickle_in)
else:
	print("The file is empty")

'''
