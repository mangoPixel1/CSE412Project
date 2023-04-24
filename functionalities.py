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
        print("(3) Show Potential Friends")
        print("(4) Delete Friend")
        print("(b) Go back")
        selectedOption = input("Select an option: ")

        match selectedOption:
            case "1":
                # print friends list of {userID}
                mycursor.execute(f"select u.fName, u.lName, u.email, f.friendshipDate \
                                 from Users u \
                                 join Friends f on u.userID = f.friendID\
                                 where f.userID = {userID}")
                rows = mycursor.fetchall()
                print(f"List of friends ({len(rows)}):")
                for row in rows:
                    print(f"{row[0]} {row[1]} {row[2]} {row[3]}")
            
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
            case "3":
                # print list of users who are not friends with {userID}
                mycursor.execute(f"select email, fName, lName \
                                    from Users u \
                                    where u.userID not in (select friendID \
                                                            from Friends \
                                                            where userID = {userID})\
                                                            limit 10")
                rows = mycursor.fetchall()
                print(f"List of potential friends ({len(rows)}):")
                for row in rows:
                    print(f"{row[0]} {row[1]} {row[2]}")

            case "4":
                # delete friend from {userID}'s friends list
                mycursor.execute(f"select friendID, fName, lName \
                                    from Users u \
                                    join Friends f on u.userID = f.friendID\
                                    where f.userID = {userID}")
                rows = mycursor.fetchall()
                print(f"List of friends ({len(rows)}):")
                for row in rows:
                    print(f"{row[0]} {row[1]}")
                enteredID = input("Enter the ID of the user you wish to delete: ")
                mycursor.execute(f"DELETE FROM Friends WHERE (userID = {userID} AND friendID = {enteredID});") # Delete friend
                print("Successfully deleted User from friends list")
                
            case "b":
                active = False

    mycursor.close()
    mydb.commit()
    mydb.close()
        
# Photo and album browsing
def show_my_photos_menu(userID):
    userID = userID
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
        print("(3) Delete photo")
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
                            show_single_album(rows[int(selectedOption2)][0], rows[int(selectedOption2)][1], userID)
                        else:
                            print("Invalid index")
                    
                        
                print()
            case "2": # View my photos
                active2 = True
                while active2:
                    mycursor.execute(f"select data, caption, photoID from Photos where ownerID = {userID}")
                    rows = mycursor.fetchall()
                    hasPhotos = False
                    if len(rows) > 0: # if user has photos
                        hasPhotos = True
                        print("\n")
                        print(f"Photos ({len(rows)}):")
                        index = 0
                        for row in rows:
                            print(f"({index}): {row[0]}")
                            print(f"Caption: {row[1]}")
                            print("\n")
                            index += 1
                    else:
                        print("You have not uploaded any photos")
                    
                    print("(b) Go back")
                    selectedOption2 = input("Select an option: ")
                    if selectedOption2 == "b":
                        active2 = False
                    elif selectedOption2.isnumeric and hasPhotos == True:
                        print(f"You selected {selectedOption2}")
                        if int(selectedOption2) >= 0 and int(selectedOption2) < len(rows):
                            show_single_photo(rows[int(selectedOption2)][2], userID)
                        else:
                            print("Invalid index")
            
            case "3": # Delete a photo
                active2 = True
                while active2:
                    mycursor.execute(f"select data, caption, photoID from Photos where ownerID = {userID}")
                    rows = mycursor.fetchall()
                    hasPhotos = False
                    if len(rows) > 0: # if user has photos
                        hasPhotos = True
                        print(f"Photos ({len(rows)}):")
                        index = 0
                        for row in rows:
                            print(f"({index}): {row[0]}")
                            print(f"Caption: {row[1]}")
                            print("\n")
                            index += 1
                    else:
                        print("You have not uploaded any photos")
                    
                    print("(b) Go back")
                    selectedOption2 = input("Select an option: ")
                    if selectedOption2 == "b":
                        active2 = False
                    elif selectedOption2.isnumeric and hasPhotos == True:
                        print(f"You selected {selectedOption2}")
                        if int(selectedOption2) >= 0 and int(selectedOption2) < len(rows):
                            photoID = rows[int(selectedOption2)][2]
                            try:
                                # Delete associated likes
                                mycursor.execute(f"delete from Likes where photoID = {photoID}")
                                # Delete associated comments
                                mycursor.execute(f"delete from Comments where photoID = {photoID}")
                                # Delete associated phototags
                                mycursor.execute(f"delete from PhotoTags where photoID = {photoID}")
                                # Delete associated photo
                                mycursor.execute(f"delete from Photos where photoID = {photoID}")
                                print(f"Photo with ID {photoID} deleted successfully")
                                mydb.commit()
                            except mysql.connector.errors.IntegrityError:
                                print("Unable to delete photo with ID {photoID} due to foreign key constraint")
                        else:
                            print("Invalid index")

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
        print("(1) Show friends' photos")
        print("(2) Show recommended")
        print("(3) Photos liked and commented")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        match selectedOption:
            case "1":
                # show only photos of friends
                mycursor.execute(f"select p.data, p.caption, p.photoID \
                                 from Users u \
                                 join Friends f on u.userID = f.friendID \
                                 join Photos p on f.friendID = p.ownerID\
                                 where f.userID = {userID}")
                rows = mycursor.fetchall()
                hasPhotos = False
                if len(rows) > 0: # if user has photos
                    hasPhotos = True
                    print(f"Photos ({len(rows)}):")
                    index = 0
                    for row in rows:
                        print(f"({index}): {row[0]}")
                        print(f"Caption: {row[1]}")
                        print("\n")
                        index += 1
                else:
                    print("No photos")
                
                print("(b) Go back")
                selectedOption2 = input("Select an option: ")
                if selectedOption2 == "b":
                    active2 = False
                elif selectedOption2.isnumeric and hasPhotos == True:
                    print(f"You selected {selectedOption2}")
                    if int(selectedOption2) >= 0 and int(selectedOption2) < len(rows):
                        show_single_photo(rows[int(selectedOption2)][2], userID)
                    else:
                        print("Invalid index")
                    
                    
            case "2":
                # show photos that haven't been seen
                offset = 0
                while True:
                    mycursor.execute(f"select p.data, p.caption, p.photoID \
                                    from Photos p \
                                    left join Friends f on p.ownerID = f.friendID and f.userID = {userID} \
                                    left join Likes l on p.photoID = l.photoID and l.userID = {userID} \
                                    left join Comments c on p.photoID = c.photoID and c.ownerID = {userID} \
                                    where f.friendshipID is null and l.userID is null and c.commentID is null \
                                    limit 5 offset {offset}")
                    rows = mycursor.fetchall()
                    hasPhotos = False
                    if len(rows) > 0: # if user has photos
                        hasPhotos = True
                        print(f"Photos ({len(rows)}):")
                        index = 0
                        for row in rows:
                            print(f"({index}): {row[0]}")
                            print(f"Caption: {row[1]}")
                            print("\n")
                            index += 1
                        if len(rows) == 5:
                            print("(n) Next")
                    else:
                        print("No photos")
                    
                    print("(b) Go back")
                    selectedOption2 = input("Select an option: ")
                    if selectedOption2 == "b":
                        active2 = False
                        break
                    elif selectedOption2 == "n" and hasPhotos == True and len(rows) == 5:
                        offset += 5
                    elif selectedOption2.isnumeric and hasPhotos == True:
                        print(f"You selected {selectedOption2}")
                        if int(selectedOption2) >= 0 and int(selectedOption2) < len(rows):
                            show_single_photo(rows[int(selectedOption2)][2], userID)
                        else:
                            print("Invalid index")
            
            case "3":
                # show photos with likes or comments from the user
                mycursor.execute(f"select p.data, p.caption, p.photoID \
                                    from Photos p \
                                    left join Likes l on p.photoID = l.photoID \
                                    left join Comments c on p.photoID = c.photoID \
                                    where p.ownerID != {userID} \
                                        and (l.userID = {userID} or c.ownerID = {userID}) \
                                        and (l.userID is not null or c.ownerID is not null) \
                                    group by p.photoID")
                rows = mycursor.fetchall()
                hasPhotos = False
                if len(rows) > 0:
                    hasPhotos = True
                    print(f"Photos ({len(rows)}):")
                    index = 0
                    for row in rows:
                        print(f"({index}): {row[0]}")
                        print(f"Caption: {row[1]}")
                        print("\n")
                        index += 1
                else:
                    print("No photos")
                    
                print("(b) Go back")
                selectedOption2 = input("Select an option: ")
                if selectedOption2 == "b":
                    active2 = False
                elif selectedOption2.isnumeric and hasPhotos == True:
                    print(f"You selected {selectedOption2}")
                    if int(selectedOption2) >= 0 and int(selectedOption2) < len(rows):
                        show_single_photo(rows[int(selectedOption2)][2], userID)
                    else:
                        print("Invalid index")

            case "b":
                active = False

    mycursor.close()
    mydb.close()

def show_single_photo(photoID, userID):
    mydb = mysql.connector.connect(
        host="photosharedb.c4csvx1ggxlz.us-east-2.rds.amazonaws.com",
        user="admin",
        password="password",
        database="photoshareDB"
    )
    mycursor = mydb.cursor()
    
    active = True
    while active:
        # select photos
        mycursor.execute(f"select caption, data from Photos where photoID = {photoID}")
        row = mycursor.fetchone()

        print()
        print(f"Caption: {row[0]}")
        print(f"URL: {row[1]}")

        # show likes
        mycursor.execute(f"select count(photoID) from Likes where photoID = {photoID}")
        row = mycursor.fetchone()
        print(f"Likes: {row[0]}")

        # select tags
        mycursor.execute(f"select tagData \
                         from Tags t\
                         join PhotoTags pt on pt.tagID = t.tagID\
                         where pt.photoID = {photoID}")
        tags = mycursor.fetchall()
        if len(tags) > 0:
            print("Tags: ", end="")
            for i in range(len(tags)):
                if i != len(tags) - 1:
                    print(f"{tags[i][0]}, ", end="")
                else:
                    print(f"{tags[i][0]}")
        else:
            print("No tags for this photo")

        # Show options
        print("(1) Like")
        print("(2) Comment")
        print("(3) Read comments")
        print("(b) Go back")
        selectedOption = input("Select an option: ")

        # Handle option
        match selectedOption:
            case "1":
                # Add like to Likes table
                try:
                    mycursor.execute(f"insert into Likes values('{userID}','{photoID}')")
                    mydb.commit()
                    print("Liked photo")
                except mysql.connector.errors.IntegrityError:
                    print("Error: You have already liked this photo")
            case "2":
                # Get comment from user and add to Comments table
                comment = input("Write comment: ")
                mycursor.execute(f"insert into Comments (ownerID, photoID, text) values ({userID}, {photoID}, '{comment}')")
                mydb.commit()
                print("Added comment")
            case "3":
                # Get comments for photo and print them
                mycursor.execute(f"select c.text, u.fName, u.lName from Comments c join Users u on c.ownerID = u.userID where c.photoID = {photoID}")
                comments = mycursor.fetchall()
                if len(comments) > 0:
                    print(f"Comments ({len(comments)}):")
                    for comment in comments:
                        print(f"{comment[1]} {comment[2]}: {comment[0]}")
                else:
                    print("No comments for this photo")
            case "b":
                active = False

    mycursor.close()
    mydb.close()

def show_single_album(albumID, albumName, userID):
    mydb = mysql.connector.connect(
        host="photosharedb.c4csvx1ggxlz.us-east-2.rds.amazonaws.com",
        user="admin",
        password="password",
        database="photoshareDB"
    )
    mycursor = mydb.cursor()
    
    active = True
    while active:
        print("\n")
        print(f"{albumName}:")
        mycursor.execute(f"select photoID, data, caption from Photos where albumID = {albumID}")
        rows = mycursor.fetchall()
        hasPhotos = False
        if len(rows) > 0: # if album has photos
            hasPhotos = True
            index = 0
            for row in rows:
                print(f"({index}) {row[2]}")
                index += 1
        else:
            print("This album has no photos")
        print("(b) Go back")
        
        selectedOption = input("Select an option: ")
        if selectedOption == "b":
            active = False
        elif selectedOption.isnumeric and hasPhotos == True:
            if int(selectedOption) >= 0 and int(selectedOption) < len(rows):
                show_single_photo(rows[int(selectedOption)][0], userID)
            else:
                print("Invalid index")
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
        print("(1) Search tag")
        print("(2) Browse most popular tags")
        print("(b) Go back")
        selectedOption = input("Select an option: ")

        match selectedOption:
            case "1":
                # prompt user for a tag to search
                enteredtag = input("Search tag: ")
                mycursor.execute(f"SELECT data, caption FROM Photos JOIN PhotoTags ON Photos.photoID = PhotoTags.photoID JOIN Tags ON PhotoTags.tagID = Tags.tagID WHERE Tags.tagData = '{enteredtag}'")
                rows = mycursor.fetchall()
                if len(rows) == 0:
                    print("No photos found with that tag")
                else:
                    print(f"{len(rows)} photos found with tag '{enteredtag}':")
                    for row in rows:
                        print(f"Photo ID: {row[0]}")
                        print(f"Caption: {row[2]}")
                        print(f"Data: {row[1][:20]}")
                        print("\n")

                offset = 0
                while True:
                    # prompt user for a tag to search
                    enteredtag = input("Search tag: ")
                    mycursor.execute(f"SELECT p.data, p.caption, p.photoID \
                                    FROM Photos p\
                                    JOIN PhotoTags ON p.photoID = PhotoTags.photoID \
                                    JOIN Tags ON PhotoTags.tagID = Tags.tagID \
                                    WHERE Tags.tagData = '{enteredtag}' \
                                    limit 5 offset {offset}")
                    rows = mycursor.fetchall()
                    hasPhotos = False
                    if len(rows) > 0: # if user has photos
                        hasPhotos = True
                        print(f"Photos ({len(rows)}):")
                        index = 0
                        for row in rows:
                            print(f"({index}): {row[0]}")
                            print(f"Caption: {row[1]}")
                            print("\n")
                            index += 1
                        if len(rows) == 5:
                            print("(n) Next")
                    else:
                        print("No photos")
                    
                    print("(b) Go back")
                    selectedOption2 = input("Select an option: ")
                    if selectedOption2 == "b":
                        active2 = False
                        break
                    elif selectedOption2 == "n" and hasPhotos == True and len(rows) == 5:
                        offset += 5
                    elif selectedOption2.isnumeric and hasPhotos == True:
                        print(f"You selected {selectedOption2}")
                        if int(selectedOption2) >= 0 and int(selectedOption2) < len(rows):
                            show_single_photo(rows[int(selectedOption2)][2], userID)
                        else:
                            print("Invalid index")
            case "2":
                mycursor.execute("SELECT tagData, COUNT(*) AS tagCount FROM Tags \
                    JOIN PhotoTags ON Tags.tagID = PhotoTags.tagID \
                    GROUP BY Tags.tagID \
                    ORDER BY tagCount DESC \
                    LIMIT 10")
                rows = mycursor.fetchall()
                print("Top 10 Tags:")
                for row in rows:
                    print(f"{row[0]} ({row[1]} photos)")
                break

            case "b":
                active = False

                
    mycursor.close()
    mydb.close()

def show_upload_photos_menu(userID):
    mydb = mysql.connector.connect(
        host="photosharedb.c4csvx1ggxlz.us-east-2.rds.amazonaws.com",
        user="admin",
        password="password",
        database="photoshareDB"
    )
    mycursor = mydb.cursor()

    active = True
    while active:
        print("Upload Photo")
        print("(a) Upload a photo")
        print("(b) Go back")
        print("(c) Add an Album")
        print("(d) Delete an Album")
        selectedOption = input("Select an option: ")
        
        if selectedOption == "a":
            enterPhoto = input("Upload photo url: ")
            enterCaption = input("Enter a caption: ")
            enteredTags = input("Enter tags (comma-separated): ")

            # Display the albums
            select_albums_query = f"SELECT albumID, name FROM Albums where ownerID = {userID}"
            mycursor.execute(select_albums_query)
            albums = mycursor.fetchall()
            print("Albums:")
            for album in albums:
                print(f"{album[0]}: {album[1]}")
                
            # Prompt user to select an album
            albumID = input("Enter albumID: ")

            # Insert photo into Photos table
            insertphoto = f"INSERT INTO Photos (data, caption, albumID, ownerID) VALUES ('{enterPhoto}', '{enterCaption}', {albumID}, {userID})"
            mycursor.execute(insertphoto)
            photoid = mycursor.lastrowid

            # Insert tags into Tags table and PhotoTags table
            tags = enteredTags.split(",")
            for tag in tags:
                # Check if tag already exists in Tags table
                tagQuery = f"SELECT tagID FROM Tags WHERE tagData = '{tag.strip()}'"
                mycursor.execute(tagQuery)
                tagRow = mycursor.fetchone()
                if tagRow is None:
                    # Insert tag into Tags table
                    inserttag = f"INSERT INTO Tags (tagData) VALUES ('{tag.strip()}')"
                    mycursor.execute(inserttag)
                    tagid = mycursor.lastrowid
                else:
                    tagid = tagRow[0]

                # Insert tag into PhotoTags table
                insertphototag = f"INSERT INTO PhotoTags (photoID, tagID) VALUES ({photoid}, {tagid})"
                mycursor.execute(insertphototag)

           # Commit changes to database
            mydb.commit()
            print("Photo uploaded successfully.\n")
        
        if selectedOption == "b":
            print("Going back...\n")
            active = False
        
        if selectedOption == "c":
            enterAlbumName = input("Enter the album name: ")
            mycursor.execute(f"INSERT INTO Albums (name, ownerID) VALUES ('{enterAlbumName}', {userID})")
            print("Album successfully added. \n")
            mydb.commit()

        if selectedOption == "d":
            # Display the albums
            select_albums_query = f"SELECT albumID, name FROM Albums WHERE ownerID = {userID}"
            mycursor.execute(select_albums_query)
            albums = mycursor.fetchall()
            print("Albums:")
            for album in albums:
                print(f"{album[0]}: {album[1]}")
            
            # Prompt user to select an album
            albumID = input("Enter albumID to delete: ")
            
            # Check if the album belongs to the user
            select_album_query = f"SELECT ownerID FROM Albums WHERE albumID = {albumID}"
            mycursor.execute(select_album_query)
            album_owner = mycursor.fetchone()
            if album_owner is None or album_owner[0] != userID:
                print("You do not have permission to delete this album")
                continue
            
            # Select all photos in the album
            select_photos_query = f"SELECT photoID FROM Photos WHERE albumID = {albumID}"
            mycursor.execute(select_photos_query)
            photos = mycursor.fetchall()
            
            try:
                # Delete associated likes, comments, and phototags for each photo in the album
                for photo in photos:
                    mycursor.execute(f"DELETE FROM Likes WHERE photoID = {photo[0]}")
                    mycursor.execute(f"DELETE FROM Comments WHERE photoID = {photo[0]}")
                    mycursor.execute(f"DELETE FROM PhotoTags WHERE photoID = {photo[0]}")
                
                # Delete all photos from the album
                mycursor.execute(f"DELETE FROM Photos WHERE albumID = {albumID}")
                
                # Delete the album itself
                mycursor.execute(f"DELETE FROM Albums WHERE albumID = {albumID}")
                
                print(f"All photos from album with albumID {albumID} deleted successfully")
                mydb.commit()
            except mysql.connector.errors.IntegrityError:
                print(f"Unable to delete photos from album with albumID {albumID} due to foreign key constraint")
            
    mycursor.close()
    mydb.close()
