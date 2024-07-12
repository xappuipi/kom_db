

import mysql.connector

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="kom"
)

table = "users"

# Create a cursor object to execute SQL queries

cursor = db.cursor()
while True:
    # Insert a record into the table
    query = "INSERT INTO users (login, pass) VALUES (%s, %s)"

    user = input("Podaj użytkownika: ")
    password = input("Podaj hasło: ")

    check = f"SELECT * FROM users WHERE login=\"{user}\" and pass=\"{password}\""
    cursor.execute(check)
    results = cursor.fetchall()

    if len(results) > 0:
        print("Taki użytkownik już istnieje")
        continue

    if user == "" or password == "":
        break

    values = (user, password)
    cursor.execute(query, values)

# Commit the changes and close the connection
db.commit()
db.close()
