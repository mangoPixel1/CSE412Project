import sys
import mysql.connector
from datetime import date

# Adding and listing friends
def show_friends_menu(userID):
    mydb = mysql.connector.connect(
        host="photosharedb.c4csvx1ggxlz.us-east-2.rds.amazonaws.com",
        user="admin",
        password="password",
        database="photoshareDB"
    )
    mycursor = mydb.cursor()
    active = True
    while active:
        print()
        print("(1) Show Friends")
        print("(2) Add a Friend")
        print("(b) Go back")
        selectedOption = input("Select an option: ")

        match selectedOption:
            case "1":
                # print friends list of {userID}
                mycursor.execute(f"select fName, lName \
                                 from Users u \
                                 join Friends f on u.userID = f.friendID \
                                 where f.userID = {userID}")
                rows = mycursor.fetchall()
                print(f"List of friends ({len(rows)}):")
                for row in rows:
                    print(f"{row[0]} {row[1]}")
            
            case "2":
                enteredEmail = input("Enter the email address of the user you wish to add: ")
                mycursor.execute(f"select email, userID, fName, lName from Users") # retrieve all emails
                rows = mycursor.fetchall()
                
                emailFound = False
                email = ""
                friendID = 0
                fName = ""
                lName = ""
                for row in rows: # check if email is in use by another member
                    if row[0] == enteredEmail:
                        emailFound = True
                        email = row[0]
                        friendID = row[1]
                        fName = row[2]
                        lName = row[3]
                 
                if emailFound:
                    mycursor.execute(f"select email, friendID \
                                     from Users u \
                                     join Friends f on u.userID = f.friendID \
                                     where f.userID = {userID}") # retrieves user's friends list
                    rows = mycursor.fetchall()
                    
                    if len(rows) > 0: # if user has at least 1 friend
                        emailFound2 = False
                        for row in rows: # check if users are already friends
                            if row[0] == email:
                                emailFound2 = True
                                #friendID = int(row[1])

                        if emailFound2:
                            print(f"You are already friends with {fName} {lName}")
                        else:
                            mycursor.execute(f"insert into Friends (userID, friendshipDate, friendID) \
                                            values(\"{userID}\", \"{date.today()}\", \"{friendID}\")")
                            mydb.commit()
                            print(f"Added {fName} {lName} to friends list")
                    else: # if user's friend list is empty
                        mycursor.execute(f"insert into Friends (userID, friendshipDate, friendID) \
                                            values(\"{userID}\", \"{date.today()}\", \"{friendID}\")")
                        mydb.commit()
                        print(f"Added {fName} {lName} to friends list")
                        
                else:
                    print("The email you entered is not associated with an existing account")
                
            case "b":
                active = False

    mycursor.close()
    mydb.close()
        

# Photo and album browsing
def show_my_photos_menu(userID):
    active = True
    while active:
        print()
        print("My Photos")
        print("INSERT PHOTOS HERE")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        if selectedOption == "b":
            active = False

def show_browse_photos_menu(userID):
    active = True
    while active:
        print()
        print("Browse Photos")
        print("(1) Show photos")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        match selectedOption:
            case "1":
                # show only photos of friends
                print("SHOW PHOTOS FEED HERE")
            case "b":
                active = False

def show_browse_tags_menu(userID):
    active = True
    while active:
        print()
        print("Browse Tags")
        print("(1) Show tags")
        print("(b) Go back")
        selectedOption = input("Select an option: ")

        match selectedOption:
            case "1":
                # prompt user for a tag to search
                print("SHOW PHOTOS CONTAINING TAG")
            case "b":
                active = False

# Photo and album creating

# Commenting on photos