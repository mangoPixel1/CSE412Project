import sys
import mysql.connector
from functionalities import *

mydb = mysql.connector.connect(
  host="photosharedb.c4csvx1ggxlz.us-east-2.rds.amazonaws.com",
  user="admin",
  password="password",
  database="photoshareDB"
)

userLoggedIn = False
userID = 0 # userID of current user that is logged in


print("PhotoShare")

while not userLoggedIn:
    mycursor = mydb.cursor()
    mycursor.execute("select userID, email, password from Users")
    myresult = mycursor.fetchall()
    #for x in myresult:
        #print(x)

    userInput = input("Select an option: (l) Login, (r) Register ")
    if userInput == "l":
        print("Log in as an existing user")
        enteredEmail = input("Enter your email address: ")
        enteredPassword = input("Enter your password: ")
        sqlCommand = f"select password from Users where email = \"{enteredEmail}\""
        mycursor.execute(sqlCommand)

        rows = mycursor.fetchall()

        if len(rows) == 1: # if email is valid
                storedPassword = rows[0][0]
                if enteredPassword == storedPassword: # if email is valid and password is valid
                    print("Login successful")
                    userLoggedIn = True
                    sqlCommand = f"select userID from Users where email = \"{enteredEmail}\""
                    mycursor.execute(sqlCommand)
                    storedUserID = mycursor.fetchone()[0]
                    userID = int(storedUserID)
                else: # if email is valid and password is invalid
                    print("Invalid password")
        else: #if email is invalid
             print("Invalid email")
    
    if userInput == "r":
        print("Register as a new user")
        fName = input("Enter your first name: ")
        lName = input("Enter your last name: ")
        emailAddr = input("Enter your email address: ")
        dob = input("Enter your date of birth (YYYY-MM-DD): ")
        hometown = input("Enter your hometown: ")
        gender = input("Enter your gender (Male/Female): ")
        password = input("Enter a secure password: ")

        sqlCommand = f"insert into Users (fName, lName, email, dateOfBirth, hometown, gender, password) values(\"{fName}\", \"{lName}\", \"{emailAddr}\", \"{dob}\", \"{hometown}\", \"{gender}\", \"{password}\")"
        mycursor.execute(sqlCommand)
        mydb.commit()
        print("User created. Log in to get started.")

# Everything past this point is only accessible to logged in users
while userLoggedIn:
    print("(1) Friends List")
    print("(2) My Photos")
    print("(3) Browse Photos")
    print("(4) Browse Tags")
    print("(5) Log out")
    selectedOption = input("Select an option")

    match selectedOption:
        case "1":
            show_friends_menu(userID)
        case "2":
            show_my_photos_menu(userID)
        case "3":
            show_browse_photos_menu(userID)
        case "4":
            show_browse_tags_menu(userID)
        case "5":
            userLoggedIn = False

print("Logging out...")


mycursor.close()
mydb.close()