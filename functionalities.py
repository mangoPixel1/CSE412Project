import sys
import mysql.connector

# Adding and listing friends
def show_friends_menu(userID):
    active = True
    while active:
        print("(1) My Friends")
        print("(2) Add a Friend")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        if selectedOption == "b":
            active = False

# Logging in/ Logging out

# Photo and album browsing
def show_my_photos_menu(userID):
    active = True
    while active:
        print("My Photos")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        if selectedOption == "b":
            active = False

def show_browse_photos_menu(userID):
    active = True
    while active:
        print("Browse Photos")
        print("(b) Go back")
        selectedOption = input("Select an option: ")
        
        if selectedOption == "b":
            active = False

def show_browse_tags_menu(userID):
    active = True
    while active:
        print("Browse Tags")
        print("(b) Go back")
        selectedOption = input("Select an option: ")

        if selectedOption == "b":
            active = False

# Photo and album creating

# Commening on photos