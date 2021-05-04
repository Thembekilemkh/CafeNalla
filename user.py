import pickle
import os

class User():
	def __init__(self):
		try:
			# Open the user pickle
			user = {}

			if os.path.getsize("bin\\user.pickle") > 0:
				with open("bin\\user.pickle", "rb") as pickle_in:
					user = pickle.load(pickle_in)
					print(user)
					
				self.user_id = user["user_id"]
				self.logged_on = user["logged_on"]
				self.first_name = user["first_name"]
				self.last_name = user["last_name"]
				self.email = user["email"]
				self.password = user["password"]
				self.admin = user['admin']
				self.loyalty_points = user["loyalty_points"]
				self.regular_drink = user["regular_drink"]

			else:
				print("The file is empty")

				# THE USER DICTIONARY
				user = {
					"user_id":None,
					"first_name":None,
					"last_name":None,
					"email":None,
					"password": None,
					"logged_on":None,
					"loyalty_points":None,
					"regular_drink":None,
					"admin":None}
				 
				with open("bin\\user.pickle", "wb") as pickle_out:
					pickle.dump(user, pickle_out)

				self.user_id = user["user_id"]
				self.logged_on = user["logged_on"]
				self.first_name = user["first_name"]
				self.last_name = user["last_name"]
				self.email = user["email"]
				self.password = user["password"]
				self.loyalty_points = user["loyalty_points"]
				self.regular_drink = user["regular_drink"]
				self.admin = user['admin']

		except Exception as e:
			print("Either something went wrong when loading the bot or we don't any saved bots: ", e)

			# THE USER DICTIONARY
			user = {
					"user_id":None,
					"first_name":None,
					"last_name":None,
					"email":None,
					"password": None,
					"logged_on":None,
					"loyalty_points":None,
					"regular_drink":None,
					"admin":None}
			 
			with open("bin\\user.pickle", "wb") as pickle_out:
				pickle.dump(user, pickle_out)

			self.user_id = user["user_id"]
			self.logged_on = user["logged_on"]
			self.first_name = user["first_name"]
			self.last_name = user["last_name"]
			self.email = user["email"]
			self.admin = user['admin']
			self.password = user["password"]
			self.loyalty_points = user["loyalty_points"]
			self.regular_drink = user["regular_drink"]


	def cache_user(self, user1):
		new_user = {}
		new_user["user_id"] = user1.user_id
		new_user["logged_on"] = user1.logged_on
		new_user["first_name"] = user1.first_name
		new_user["last_name"] = user1.last_name
		new_user["email"] = user1.email
		new_user["password"] = user1.password
		new_user["loyalty_points"] = user1.loyalty_points
		new_user["regular_drink"] = user1.regular_drink
		new_user["admin"] = user1.admin

		with open("bin\\user.pickle", "wb") as pickle_out:
			pickle.dump(new_user, pickle_out)