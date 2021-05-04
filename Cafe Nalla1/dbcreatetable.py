import pymysql
import mysql.connector
from mysql.connector import Error

try:
	# localhost
    db = mysql.connector.connect(host="localhost", user="thembekile", password="LlenoCEO#5", database="cafenalla", port="33162")
    cursor = db.cursor()

    # Creating tables for our data base
    user_table = """CREATE TABLE user(	
                id INT AUTO_INCREMENT,
                First_Name VARCHAR(100),
                Last_Name VARCHAR(100),
                Email VARCHAR(100),
                Password VARCHAR(100),
                Loyalty_Points FLOAT,
                Regular VARCHAR(150),
                admin INT,
                register_date DATETIME,
                PRIMARY KEY(id));"""

    breakfast_table = """CREATE TABLE breakfast(	
                id INT AUTO_INCREMENT,
                Meal_Name VARCHAR(100),
                Ingredients VARCHAR(100),
                Price VARCHAR(100),
                PRIMARY KEY(id));"""

    meals_table = """CREATE TABLE meals(	
                id INT AUTO_INCREMENT,
                Meal_Name VARCHAR(100),
                Ingredients VARCHAR(100),
                Price VARCHAR(100),
                PRIMARY KEY(id));"""

    salads_table = """CREATE TABLE salads(	
                id INT AUTO_INCREMENT,
                Meal_Name VARCHAR(100),
                Ingredients VARCHAR(100),
                Price VARCHAR(100),
                PRIMARY KEY(id));"""

    smoothies_table = """CREATE TABLE smoothies(	
                id INT AUTO_INCREMENT,
                Meal_Name VARCHAR(100),
                Ingredients VARCHAR(100),
                Price VARCHAR(100),
                PRIMARY KEY(id));"""

    shakes_table = """CREATE TABLE shakes(	
                id INT AUTO_INCREMENT,
                Drink_Name VARCHAR(100),
                Ingredients VARCHAR(100),
                Price VARCHAR(100),
                PRIMARY KEY(id));"""

    cold_drink_table = """CREATE TABLE cold_drink(	
                id INT AUTO_INCREMENT,
                Drink_Name VARCHAR(100),
                Ingredients VARCHAR(100),
                Price VARCHAR(100),
                PRIMARY KEY(id));"""

    orders_table = """CREATE TABLE orders(	
                id INT AUTO_INCREMENT,
                user_id INT,
                Meal_Name VARCHAR(100),
                Meal_Group VARCHAR(100),
                Ingredients VARCHAR(200),
                Status VARCHAR(50),
                collection_date DATETIME,
                order_date DATETIME,
                PRIMARY KEY(id),
                FOREIGN KEY(user_id) REFERENCES user(id));"""

    regulars_table = """CREATE TABLE regulars(	
                id INT AUTO_INCREMENT,
                user_id INT,
                Meal_Name VARCHAR(100),
                Meal_Group VARCHAR(100),
                Ingredients VARCHAR(200),
                creation_date DATETIME,
                PRIMARY KEY(id),
                FOREIGN KEY(user_id) REFERENCES user(id));"""

    tables = [user_table, orders_table, breakfast_table, meals_table,
    		 salads_table, smoothies_table, shakes_table,
    		 cold_drink_table]


    cursor.execute(regulars_table)
    db.commit()

    db.close()
except Exception as e:
	print(f'Something went wrong: {e}')