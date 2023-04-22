import sys
import mysql.connector

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
        print("(1) My Friends")
        print("(2) Add a Friend")
        print("(b) Go back")
        selectedOption = input("Select an option: ")

        match selectedOption:
            case "1":
                # print friends list of {userID}
                print("List of friends:")
                mycursor.execute(f"select fName, lName \
                                 from Users u \
                                 join Friends f on u.userID = f.friendID \
                                 where f.userID = {userID}")
                rows = mycursor.fetchall()
                for row in rows:
                    print(row)
            case "2":
                # prompt for email of user to add as friend
                print("Enter the email address of the user you wish to add: ")
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