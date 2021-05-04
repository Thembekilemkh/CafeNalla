import pymysql
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet
import pickle
import datetime
import os 

class Create_User():

    def __init__(self,*arg,**kwargs):
        conQ = kwargs["conQ"]
        user_created = kwargs["user_created"]
        user = kwargs["user"]
        userQ = kwargs["userQ"]

        kwargs.pop("conQ")
        kwargs.pop("user_created")
        kwargs.pop("user")
        kwargs.pop("userQ")

        print("In the __init__")
        try:
            #self.db = pymysql.connect(host="mysql-10652-0.cloudclusters.net" ,user="ThembekileCEO", password="==h2e=lnm=Fh" , database="llenobacktester_db2", port="10652")
            self.db = mysql.connector.connect(host="localhost", user="thembekile", password="LlenoCEO#5", database="cafenalla", port="33162")
            conQ.put(True)

            # prepare a cursor object using # prepare a cursor object using cursor() cursor() method method 
            self.cursor = self.db.cursor()

            #Getting our tables
            self.user_table = "user"
            self.stats_table = "stats"

            try:
                user = self.create_new_user(first_name = kwargs["first_name"], last_name = kwargs["last_name"],
                                    email = kwargs["email"], password = kwargs["password"], user=user, admin=kwargs['admin'])
                user_created.put(True)
                userQ.put(user)
            except Exception as e:
                print("Failed to create user: ", str(e))
                user_created.put(False)

        except pymysql.err.OperationalError:
            print("Failed network connection")
            conQ.put("Failed to create account, check your connection")

    # Function to create new users
    def create_new_user(self, **kwargs):
        user = kwargs["user"]

        #First collect the data we want to store in our data base
        first_name = kwargs["first_name"]
        first_name = first_name.text
        
        last_name = kwargs["last_name"]
        last_name= last_name.text
        
        email = kwargs["email"]
        email = email.text
        
        password = kwargs["password"]
        password = password.text

        admin = kwargs['admin']

        def create_user_object(**kwargs):
            #Get our data
            user = kwargs["user"]
            user_id =kwargs["user_id"]
            logged_on = kwargs["logged_on"]
            first_name = kwargs["first_name"]
            email = kwargs["email"]
            password = kwargs["password"]
            admin = kwargs['admin']
            last_name = kwargs['last_name']

            user.user_id = user_id
            user.logged_on = True
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.password = password
            user.Regular = None
            user.Loyalty_Points = 0
            user.admin = admin

            return user
        # Insert user into data base
        # An admin of 2 make you admin one of 1 makes you an employee and 0 make you a user
        ##enc_first_name = self.encrypt_string(first_name)
        #enc_last_name = self.encrypt_string(last_name)
        #enc_email = self.encrypt_string(email)
        #enc_password = self.encrypt_string(password)

        insert_user_to_db = f"""INSERT INTO {self.user_table}(
                            First_Name, Last_Name, Email, Password, register_date, Loyalty_Points, admin)
                            VALUES("{first_name}", "{last_name}", "{email}",
                            "{password}", now(), 0, {str(admin)});
                            """
        user_inserted = False       
        # Execute the database post
        try:
            # Execute SQL command
            print(insert_user_to_db)
            self.cursor.execute(insert_user_to_db)

            # Commit changes in the database
            self.db.commit()
            user_inserted = True

        except Exception as e:
                # Rollback in case of any error
                print("Failed to insert user to user table: ", str(e))

        if user_inserted == True:
            get_user_id  = f""" SELECT id FROM {self.user_table} WHERE Email = "{email}" AND First_Name = '{first_name}'; """

            try:
                # If successfull want to create a file in the users desktop that saves the id and password for later use
                self.cursor.execute(get_user_id)
           
                for row in self.cursor:
                    user_id = row[0]

                user = create_user_object(user_id=user_id, logged_on=1, first_name=first_name, 
                                       email=email, password=password, user=user,
                                       last_name=last_name, admin=admin)
                self.db.close()
                return user

            except Exception as e:
                print("Falied to retrieve the user id from the data base: ", str(e))
                
            
                self.db.rollback()
            
        # disconnect from server 
        self.db.close()

        return None

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

                #encryped_str = encryped_str.replace("'", "^")
                print('')
                print(f'string: {string}\nenc_string: {encryped_str}')
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