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
        print("My Photos")
        print("(1) View my albums")
        print("(2) View my photos")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        match selectedOption:
            case "1": # View my albums
                active2 = True
                while active2:
                    print()
                    mycursor.execute(f"select albumID, name from Albums where ownerID = {userID}")
                    rows = mycursor.fetchall()
                    hasAlbums = False
                    if len(rows) > 0: # if user has albums
                        hasAlbums = True
                        print("My albums:")
                        index = 0
                        for row in rows:
                            print(f"({index}) {row[1]}")
                            index += 1
                    else:
                        print("You have no albums")

                    print("(b) Go back")
                    selectedOption2 = input("Select an option: ")
                    if selectedOption2 == "b":
                        active2 = False
                    elif selectedOption2.isnumeric and hasAlbums == True:
                        if int(selectedOption2) >= 0 and int(selectedOption2) < len(rows):
                            show_single_album(rows[int(selectedOption)][0])
                        else:
                            print("Invalid input")
                    
                        
                print()
            case "2": # View my photos
                mycursor.execute(f"select data from Photos where ownerID = {userID}")
                rows = mycursor.fetchall()
                if len(rows) < 1:
                    print("You have not uploaded any photos")
                else:
                    print(f"Photos ({len(rows)}):")
                    for row in rows:
                        print(row[0])
            case "b":
                active = False
    mycursor.close()
    mydb.close()

def show_browse_photos_menu(userID):
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

    mycursor.close()
    mydb.close()

def show_single_photo(photoID):
    mydb = mysql.connector.connect(
        host="photosharedb.c4csvx1ggxlz.us-east-2.rds.amazonaws.com",
        user="admin",
        password="password",
        database="photoshareDB"
    )
    mycursor = mydb.cursor()
    
    active = True
    while active:
        mycursor.execute(f"select caption, data from Photos where photoID = {photoID}")
        row = mycursor.fetchone()

        print()
        print(f"Caption: {row[0]}")
        print(f"URL: {row[1]}")

        print("(1) Like")
        print("(2) Comment")
        print("(3) Read comments")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        match selectedOption:
            case "1":
                print("Liked photo")
            case "2":
                print("Write comment: ")
            case "3":
                print("SHOW COMMENTS HERE")
            case "b":
                active = False

    mycursor.close()
    mydb.close()

def show_single_album(albumID):
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
        mycursor.execute(f"select photoID, data from Photos where albumID = {albumID}")
        rows = mycursor.fetchall()
        hasPhotos = False
        if len(rows) > 0: # if album has photos
            hasPhotos = True
            index = 0
            for row in rows:
                print(f"({index}) URL: {row[0]}")
                index += 1
        else:
            print("This album has no photos")
        print("(b) Go back")
        
        selectedOption = input("Select an option: ")
        if selectedOption.isnumeric and hasPhotos == True:
            if int(selectedOption) >= 0 and int(selectedOption) < len(rows)-1:
                show_single_photo(rows[int(selectedOption)][0])
        elif selectedOption == "b":
            active = False
    mycursor.close()
    mydb.close()

def show_browse_tags_menu(userID):
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

    mycursor.close()
    mydb.close()

# Photo and album creating

# Commenting on photos