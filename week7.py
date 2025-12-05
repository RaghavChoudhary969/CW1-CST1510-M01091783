
import bcrypt
import os

# The file which we will store user data 

USER_DATA_FILE = "users.txt"



#HASHING FUNCTION.



def hash_password(plain_text_password):
    # Encode the password into bytes
    password_bytes = plain_text_password.encode('utf-8')

    # Generate a unique salt
    salt = bcrypt.gensalt()

    # Hash the password using the salt
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Convert hashed bytes to a string for storage
    return hashed.decode('utf-8')



#PASSWORD AUTHENTICATION FUNCTION


def verify_password(plain_text_password, hashed_password):
    # Convert both the plain password and the stored hash into bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Compare the entered password with the stored hashed password
    return bcrypt.checkpw(password_bytes, hashed_bytes)



# Creating a file

USER_DATA_FILE = "users.txt"

# Check for the username that it aalready exists or not

def user_exists(username):
    # Check if the user data file exists
    if not os.path.exists(USER_DATA_FILE):
        return False  
    
    # Open the file and look through each line
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.split(",")[0]  # Get the username part
            if stored_username == username:
                # Found a match, user exists
                return True  # Found a match, user exists

   
    return False

#Check if username already exists or not

def user_exists(username):
    # Check if the user data file exists
    if not os.path.exists(USER_DATA_FILE):
        return False  
    # Open the file and look through each line
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username = line.split(",")[0]  
            if stored_username == username:
                #if user exists it returns true
                return True  

    # If found nothing in whole file
    return False

# register a user

def register_user(username, password):
    # Stop if the username is already in use
    if user_exists(username):
        print("Error: This username is already taken.")
        return False

    # Hash the password before storing it
    hashed_password = hash_password(password)

    # Append the username and hashed password to the data file
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed_password}\n")

    print(f"User '{username}' has been registered successfully!")
    return True

#login


def login_user(username, password):
    # Check if any users are registered
    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    # Open the file and check each stored user
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            stored_username, stored_hash = line.strip().split(",")

            # If username matches, verify the password
            if stored_username == username:
                if verify_password(password, stored_hash):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    # Username not found in file
    print("Error: Username not found.")
    return False

#User Menu

def display_menu():
    print("\nPlease choose an option:")
    print("1. Register a new account")
    print("2. Login to your account")
    print("3. Exit the program")

#Main program

def main():
    while True:
        display_menu()
        choice = input("Please select an option: ").strip()

        if choice == "1":
            # Register a new user
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            confirm = input("Confirm your password: ").strip()

            if password != confirm:
                print("Error: Passwords do not match.")
                continue

            register_user(username, password)

        elif choice == "2":
            # Login with existing account
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            login_user(username, password)

        elif choice == "3":
            # Exit the program
            print("Goodbye!")
            break

        else:
            print("Error: Invalid choice. Please try again.")