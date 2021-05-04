import os
import pickle
import pymysql
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

class Login_User():

    def __init__(self, **kwargs):
        conQ = kwargs["conQ"]
        print("In the __init__")
        try:

            #self.db = pymysql.connect(host="mysql-10652-0.cloudclusters.net" ,user="ThembekileCEO", password="==h2e=lnm=Fh" , database="llenobacktester_db2", port="10652")
            self.db = mysql.connector.connect(host="localhost", user="thembekile", password="LlenoCEO#5", database="cafenalla", port="33162")
            conQ.put(True)
            # prepare a cursor object using # prepare a cursor object using cursor() cursor() method method 
            self.cursor = self.db.cursor()

            #Getting our tables
            self.user_table = "user"
            self.bots_table = "bots"
            self.conditions_table = "conditions"
            self.indicators_table = "indicators_config"
            #self.postion_table = "Position"
            #self.stats_table = "Stats"

        except pymysql.err.OperationalError:
            print("Failed network connection")
            conQ.put("Failed to log you in, check your connection")
    
    def encrypt_string(self, string):
        encryped_str = ''
        if os.path.getsize("bin\\key.pickle") > 0:
            with open("bin\\key.pickle", "rb") as pickle_in:
                key = pickle.load(pickle_in)

                fernet = Fernet(key)
                  
                # then use the Fernet class instance 
                # to encrypt the string string must must 
                # be encoded to byte string before encryption
                encryped_str = fernet.encrypt(string.encode())

                encryped_str = encryped_str.replace("'", "^")
                print('')
                print(f'string: {string}\nenc_string: {len(encryped_str)}')
                print('')
                
        return encryped_str

    def decrypt_string(self, encrypted_str):
        decoded_str = ''
        if os.path.getsize("bin\\key.pickle") > 0:
            with open("bin\\key.pickle", "rb") as pickle_in:
                key = pickle.load(pickle_in)

                fernet = Fernet(key)
                  
                # then use the Fernet class instance 
                # to encrypt the string string must must 
                # be encoded to byte string before encryption
                encrypted_str = encrypted_str.replace("^", "'")
                decoded_str = fernet.decrypt(encrypted_str).decode()
        return decoded_str

    # Function to create new users
    def find_user(self, **kwargs):
        def create_user_object(**kwargs):
            #Get our data
            active_user = kwargs["active_user"]
            user_id =kwargs["user_id"]
            first_name = kwargs["first_name"]
            email = kwargs["email"]
            password = kwargs["password"]
            regular=kwargs['regular']
            admin=kwargs['admin']
            last_name=kwargs['last_name']

            update_pickle = False

            # Check if the user was the last logged in user
            if user_id == active_user.user_id:
                if first_name == active_user.first_name:
                    if password == active_user.password:
                        active_user.logged_on = True

                        user = {
                                "user_id":active_user.user_id,
                                "logged_on":True,
                                "first_name":active_user.first_name,
                                "last_name":active_user.first_name,
                                "email": active_user.email,
                                "password":active_user.password,
                                "regular_drink": active_user.regular_drink,
                                "admin":active_user.admin,
                                "loyalty_points":active_user.loyalty_points
                                }

            else: 
                # create a new user pickle
                update_pickle = True
                user = {
                    "user_id":kwargs["user_id"],
                    "logged_on":True,
                    "first_name":kwargs["first_name"],
                    "last_name":kwargs["last_name"],
                    "regular_drink":None,
                    "email": kwargs["email"],
                    "password":kwargs["password"],
                    "admin": kwargs['admin'],
                    "loyalty_points":0
                        }

            #with open("bin\\user.pickle", "wb") as pickle_out:
                #pickle.dump(user, pickle_out)

            return user, update_pickle

        #First collect the data we want to store in our data base
        first_name = kwargs["first_name"]
        first_name = first_name.text
     
        password = kwargs["password"]
        password = password.text
        active_user = kwargs["user"]

        #enc_first_name = self.encrypt_string(first_name)
        #enc_password = self.encrypt_string(password)

        # Find user into data base
        select_user_to_db = f"""SELECT id FROM {self.user_table}
                            WHERE First_Name = '{first_name}' AND Password = '{password}';
                            """
        
        # Execute the database post
        user_found = False
        user_id = 0
        try:
            # Execute SQL command
            self.cursor.execute(select_user_to_db)
            for row in self.cursor:
                user_id = row[0]

        except Exception as e:
            # Rollback in case of any error
            print("Well something failed: ", str(e))
            self.db.rollback()
        
        if user_id > 0:
            # Get the email, user regular order and the user loyalty points
            try:
                # Execute SQL command
                get_user_email  = f""" SELECT Email, Loyalty_Points, Regular, admin, Last_Name FROM { self.user_table} WHERE id = {user_id}; """
                self.cursor.execute(get_user_email)

                for row in self.cursor:
                    email = row[0]
                    Regular = row[1]
                    admin = row[2]
                    last_name = row[3]
                    user_found = True
                    
            except Exception as e:
                print("failed to get user email: ", str(e))
                user_found == False
                
            if user_found == False:
                self.db.close()
                return False
            else:
                #dec_last_name = decrypt_string(password)
                #dec_email = decrypt_string(email)
                user, update_pickle = create_user_object(user_id=user_id, first_name=first_name, email=email, 
                                                      password=password, active_user=active_user, 
                                                      regular=Regular, admin=admin, last_name=last_name)
        else:
            self.db.close()
            return False

        # disconnect from server 
        self.db.close()

        la_user = [True, user]
        return la_user

    def find_email(self, **kwargs):
        email = kwargs["email"]

        user_id = None
        select_user_to_db = f"""SELECT id FROM {self.user_table}
                            WHERE Email = '{email}';
                            """

        try:
            # Execute SQL command
            self.cursor.execute(select_user_to_db)
            for row in self.cursor:
                user_id = row[0]

        except Exception as e:
            # Rollback in case of any error
            print("Well something failed: ", str(e))
            self.db.rollback()
            

        return user_id


    def get_user_info(self, **kwargs):
        user = kwargs["user"]
        user_id = user.user_id

        # USER TABLE

        select_user_name = f"""SELECT First_Name, Last_Name, Email, Regular, admin, Loyalty_Points FROM {self.user_table}
                            WHERE id = {user_id};
                            """
        try:
            # Execute SQL command
            self.cursor.execute(select_user_name)
            for row in self.cursor:
                user_name = row[0]
                last_name = row[1]
                email = row[2]
                regular_drink = row[3]
                admin = row[4]
                loyalty_points = row[5]

        except Exception as e:
            # Rollback in case of any error
            print("Well something failed: ", str(e))
            self.db.rollback()

        # Safe store the name obtained
        user.first_name = user_name
        user.last_name = last_name
        user.email = email
        user.regular_drink = None
        user.admin = admin
        user.loyalty_points = loyalty_points

        # REGULARS TABLE    
        select_regular = f"""SELECT  Meal_Name, Meal_Group, Ingredients FROM {self.regulars_table}
                            WHERE id = {user_id};
                            """
        if regular_drink == 'True':
            try:
                # Execute SQL command
                self.cursor.execute(select_bots)
                for row in self.cursor:
                    meal_name = row[0]
                    meal_group = row[1]
                    ingredients = row[2]

                user.regular_drink = {meal_group:[meal_name, ingredients]}
            except Exception as e:
                # Rollback in case of any error
                print("Well something failed: ", str(e))
                self.db.rollback()
        else: 
            pass

        # update data base password
        new_password = user.password
        self.update_user_password(new_password=new_password, user_id=user_id)

        return user

    def update_user_password(self, **kwargs):
        new_password = kwargs["new_password"]
        user_id = kwargs["user_id"]

        enc_password = self.encrypt_string(new_password)

        update_password = f"""UPDATE {self.user_table} SET Password = '{enc_password}'
                            WHERE id = {user_id};
                            """
        try:
            # Execute SQL command
            self.cursor.execute(update_password)

        except Exception as e:
            # Rollback in case of any error
            print("Well something failed: ", str(e))
            self.db.rollback()


    def int_2_config(self, integer):
        if integer == 0 or integer == 1 or integer == 2 or integer == 3 or integer == 4 or integer == 5:
            return None

        elif integer == 6:
            return "Adx_Period"
        elif integer == 7:
            return "AMA_Period"
        elif integer == 8:
            return "Fast_EMA"
        elif integer == 9:
            return "Slow_EMA"
        elif integer == 10:
            return "AMA_Shift"
        elif integer == 11:
            return "Bands_Period"
        elif integer == 12:
            return "Shift"
        elif integer == 13:
            return "Deviation"
        elif integer == 14:
            return "Apply_To"
        elif integer == 15:
            return "MA_Period"
        elif integer == 16:
            return "MA_Shift"
        elif integer == 17:
            return "MA_Method"
        elif integer == 18:
            return "Tenkan_sen"
        elif integer == 19:
            return "Kijun_sen"
        elif integer == 20:
            return "Senkou_Span_B"
        elif integer == 21:
            return "Step"
        elif integer == 22:
            return "Maximum"
        elif integer == 23:
            return "Period_CMO"
        elif integer == 24:
            return "Period_EMA"
        elif integer == 25:
            return "Volume_Type"
        elif integer == 26:
            return "MACD_SMA"
        elif integer == 27:
            return "Mom_Period"
        elif integer == 28:
            return "K_Period"
        elif integer == 29:
            return "D_Period"
        elif integer == 30:
            return "Slowing"
        elif integer == 31:
            return "Price_Field"
        elif integer == 32:
            return "Jaws_Period"
        elif integer == 33:
            return "Jaws_Shift"
        elif integer == 34:
            return "Teeth_Period"
        elif integer == 35:
            return "Teeth_Shift"
        elif integer == 36:
            return "Lips_Period"
        elif integer == 37:
            return "Lips_Shift"
