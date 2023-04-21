import sys
import mysql.connector

mydb = mysql.connector.connect(
  host="photosharedb.c4csvx1ggxlz.us-east-2.rds.amazonaws.com",
  user="admin",
  password="password",
  database="photoshareDB"
)

# userOption = start || login || register
userOption = "start"
userLoggedIn = False

print("PhotoShare")

userEmail = ""
userPassword = ""

while not userLoggedIn:
    userInput = input("Select an option: (l) Login, (r) Register ")
    if userInput == "l":
        print("Log in as an existing user")
        userEmail = input("Enter your email address: ")
        userPassword = input("Enter your password: ")
    
    if userInput == "r":
        print("Register as a new user")
        fName = input("Enter your first name: ")
        lName = input("Enter your last name: ")
        emailAddr = input("Enter your email address: ")
        dob = input("Enter your date of birth (YYYY-MM--DD): ")


mycursor = mydb.cursor()
mycursor.execute("select userID, email, password from Users")
myresult = mycursor.fetchall()
#for x in myresult:
    #print(x)

mydb.close()