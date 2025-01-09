import mysql.connector

mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       password="Tuckerstriker12",
       database="factory_management_db"  # Make sure database exists!
   )

if mydb.is_connected():
       print("Connected to MySQL database!")
else:
       print("Failed to connect to database.")
