import json
import re

class User:
    def __init__(self, firstName, lastName, email, password, phone, projects=[]):
        self.firstName = firstName
        self.lastName  = lastName
        self.email     = email
        self.password  = password
        self.phone     = phone
        self.projects  = projects

with open("projects/project_2_title.txt", "w") as f:
    f.write("Hello world")

class Project:
    def __init__(self, owner, title, details, target, startDate, endDate):
        self.owner     = owner
        self.title     = title
        self.details   = details
        self.target    = target
        self.startDate = startDate
        self.endDate   = endDate

def registeration():
    firstName = nameValidation("First")
    lastName  = nameValidation("Last")
    email     = emailValidation()
    password  = passwordValidation()
    phone     = phoneValidation()

    # print(firstName, lastName, email, password, phone)
    newUser = User(firstName, lastName, email, password, phone)
    newUser_dict = newUser.__dict__
    print(newUser_dict)

    updateData(email,newUser_dict)

def nameValidation(type):
    firstName = input(f"Please Enter Your {type} Name (no numbers and more than 3 characters): ")
    if re.search('[a-zA-Z]{3}', firstName):
        print(firstName)
        return firstName
    else:
        print("Wrong Name (Make sure u entered no numbers and and more than 3 characters)")
        return nameValidation()

def emailValidation():
    email = input("Please Enter Your Email")
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(email_regex, email):
        return email
    else:
        print("Wrong Email, Please Enter a valid Email")
        return emailValidation()

def passwordValidation():
    password = input("Please Enter Your Password : ")
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        while True:
            repeatedPassword = input("Repeat Your Password : ")
            if repeatedPassword == password:
                break
            else:
                print("Psswords don't match .. try again")
        return password
    else:
        print("Wrong Password .. try again")
        return passwordValidation()

def phoneValidation():
    phone = input("Please Enter Your Egyption Phone Number : [+20] ")
    if re.fullmatch(r'[0-9]{10}', phone):
        return phone
    else:
        print("Wrong Phone Number (only 10 numbers without first 0)")
        return phoneValidation()

data["email"] = {userDAta}


def updateData(instance_identifier, instance_dict):
    data = {}
    with open("data.json","r") as f:
        oldData = json.load(f)
        print("old",oldData)

        oldData[instance_identifier] = instance_dict
        print("old After", oldData)
        data=oldData

    with open("data.json", "w") as f:
        json.dump(data, f)

# ______________________________________________

def login():
    data = {}

    with open("data.json", "r") as f:
        data = json.load(f)

    email = input("Please Enter Your Email : ")
    try:
        userData = data[email]
        print(userData)
        print(userData["password"])
        while True:
            userPassword = input("Enter your password : ")
            if userData["password"] == userPassword:
                welcome(userData)
                break
            else:
                print("Wrong Password .. try again")
    except:
        print('Email Not Found')
        while True:
            option = input("    1) For Registeration type '1' \n    2) To Login again type '2'\n : ")
            if option == "1":
                registeration()
            elif option == "2":
                login()
            else:
                print("Wrong Choice")

def welcome(user_dic):
    print(f"Welcome {user_dic['firstName']} {user_dic['lastName']}")

def viewAllProjects():
    pass

def myProjects():
    pass

def createProject(owner):
    title   = input("Enter The Ptoject title")
    details = input("Type some details")


login()
# registeration()
# regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
# x= r/

