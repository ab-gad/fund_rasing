import json
import re
from itertools import count
from datetime import *

class User:
    def __init__(self, firstName, lastName, email, password, phone, projects=[]):
        self.firstName = firstName
        self.lastName  = lastName
        self.email     = email
        self.password  = password
        self.phone     = phone
        self.projects  = projects

lastID = ""
with open("projectsCounter.txt", "r") as f:
    lastID = int(f.read())

class Project:
    _ids = count(lastID+1)
    def __init__(self, owner, title, details, target, startDate, endDate):
        self.owner     = owner
        self.title     = title
        self.details   = details
        self.target    = target
        self.startDate = startDate
        self.endDate   = endDate
        self.id        = next(self._ids)

def registeration():
    firstName = nameValidation("First")
    lastName  = nameValidation("Last")
    email     = emailValidation()
    password  = passwordValidation()
    phone     = phoneValidation()

    newUser = User(firstName, lastName, email, password, phone)
    newUser_dict = newUser.__dict__

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


def updateData(instance_identifier, instance_dict):
    data = {}
    with open("data.json","r") as f:
        oldData = json.load(f)

        oldData[instance_identifier] = instance_dict
        data=oldData

    with open("data.json", "w") as f:
        json.dump(data, f)

# ______________________________________________

def login():
    print("\n--------------------Login Page-----------------")
    data = {}

    with open("data.json", "r") as f:
        data = json.load(f)

    email = input("Please Enter Your Email : ")
    try:
        userData = data[email]
        while True:
            userPassword = input("Enter your password : ")
            if userData["password"] == userPassword:
                welcome(userData)
                break
            else:
                print("Wrong Password .. try again")
    except KeyError:
        print('Email Not Found')
        while True:
            option = input("    1) For Registeration type '1' \n    2) To Login again type '2'\n    3) Main Menu '3'\n : ")
            if option == "1":
                registeration()
            elif option == "2":
                login()
            elif option == "3":
                break
            else:
                print("Wrong Choice")

def welcome(user_dic):
    print("\n------------------------------------------------------\n")
    print(f"Welcome {user_dic['firstName']} {user_dic['lastName']}")
    ownerName = f"{user_dic['firstName']} {user_dic['lastName']}"
    while True:
        option = input("1) View All Projects\n2) Create a Project\n3) Edit Your Projects\n4) Sign out\n : ")
        if option == "1":
            viewAllProjects()
        elif option == "2":
            createProject(ownerName, user_dic)
        elif option == "3":
            editProjects(user_dic)
        elif option == "4":
            break
        else:
            print("Wrong Options")

def viewAllProjects():
    with open("projects.json", "r") as f:
        projectData = json.load(f)
        for i in projectData :
            projectView = f"Project Title: {projectData[i]['title']} \n" \
                          f"Created by: {projectData[i]['owner']} \n" \
                          f"Target : {projectData[i]['target']}$ \n" \
                          f"From {projectData[i]['startDate']} to {projectData[i]['endDate']}$ \n" \
                          f"Details: {projectData[i]['details']}\n" \
                          f"-----------------------------------------------"

            print(projectView)


def createProject(owner, user_dict):
    title     = projectTitleValidation()
    details   = input("Type some details : ")
    target    = projectTargetValidation()
    startDate = ""
    endDate   = ""
    while True:
        startDate = dateValidation("Start")
        endDate   = dateValidation("End")
        if startDate < endDate:
            break
        else:
            print("Wrong Date (End Date Must be After The Start One), pleas Try Again")

    newProject = Project(owner, title, details, target, str(startDate), str(endDate))
    newProject_dict = newProject.__dict__
    print(newProject_dict)

    updateProjectsData(newProject_dict["id"], newProject_dict)
    updateUserData(newProject_dict["id"], user_dict)

    with open("projectsCounter.txt", "w") as f:
        f.write(str(newProject_dict["id"]))

def projectTitleValidation():
    title = input("Enter The Ptoject title : ")
    if re.fullmatch(r'[A-Za-z0-9]{2,}', title):
        return title
    else:
        print("Wrong Title make sure u didn' use any specila character")
        return projectTitleValidation()

def projectTargetValidation():
    target = input("Type the Project Targer : ")
    if re.fullmatch(r'[0-9]{2,}', target) and int(target) > 0:
        return target
    else:
        print("Wrong Target Value")
        return projectTargetValidation()

def dateValidation(time):
    dateFromUser = input(f"Please Enter a {time} Date For Your Project")
    date_regex = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
    if re.fullmatch(date_regex, dateFromUser):
        separator = dateFromUser[2]
        d, m, y = [int(x) for x in dateFromUser.split(separator)]
        dateInstance = date(y, m, d)
        return dateInstance
    else:
        print("Wrong Date, Please Enter a valid Date Format dd/mm/yyyy")
        return dateValidation(time)


def updateProjectsData(id , project_dict):
    data = {}
    with open("projects.json", "r") as f:
        oldData = json.load(f)
        oldData[id] = project_dict
        data = oldData

    with open("projects.json", "w") as f:
        json.dump(data, f)

def updateUserData (id, user_dict):
    print("id",id, "dict", user_dict)
    data = {}
    with open("data.json", "r") as f:
        oldData = json.load(f)
        user_dict["projects"].append(id)
        userEmail = user_dict["email"]
        oldData[userEmail] = user_dict
        data = oldData

    with open("data.json", "w") as f:
        json.dump(data, f)

def editProjects(user_dict):
    projectsIDs = user_dict["projects"]
    if len(projectsIDs) == 0:
        print("You Have No Projects")
    else:
        print(f"You have created {len(projectsIDs)} Projects\n")
        option = input("1) View My Projects\n2) Delete Project \n3) Edit a Project\n : ")
        if option == "1":
            viewUserProjects(projectsIDs)
        elif option == "2":
            deleteProject(user_dict)
        elif option == "3":
            editUserProject(user_dict)
        else:
            print("Wrong option")

def viewUserProjects(projectsIDs):
    with open("projects.json", "r") as f:
        projectData = json.load(f)
        for i in projectData :
            if int(i) in projectsIDs:
                projectView = f"Project Id: {projectData[i]['id']} \n" \
                              f"Project Title: {projectData[i]['title']} \n" \
                              f"Created by: {projectData[i]['owner']} \n" \
                              f"Target : {projectData[i]['target']}$ \n" \
                              f"From {projectData[i]['startDate']} to {projectData[i]['endDate']}$ \n" \
                              f"Details: {projectData[i]['details']}\n" \
                              f"-----------------------------------------------"

                print(projectView)

def deleteProject(user_dict):
    id = input("Enter ID of The Project You Want to Delete")
    projectsIDs = user_dict["projects"]

    if int(id) in projectsIDs :
        removeFromProjects(id)
        removeFromUserData(id, user_dict)
        print(f"Your Project of id: {id} was Deleted Successfully")
    else:
        print("Wrong ID")


def removeFromProjects(id):
    data = {}
    with open("projects.json","r") as f:
        oldData = json.load(f)
        del oldData[id]
        data = oldData

    with open("projects.json","w") as f:
        json.dump(data, f)

def removeFromUserData(id, user_dict):
    data = {}
    with open("data.json", "r") as f:
        oldData = json.load(f)
        user_dict["projects"].remove(int(id))

        userEmail = user_dict["email"]
        oldData[userEmail] = user_dict
        data = oldData

    with open("data.json", "w") as f:
        json.dump(data, f)

def editUserProject(user_dict):
    print("Will be Added Soon ISA")
    # userPorjects = user_dict["projects"]
    # id = input("Enter The ID of The Project You want to Edit")
    # data = {}
    # with open("projects.json", "r") as f:
    #     data = json.load(f)
    #
    # if int(id) in userPorjects:
    #     print("Choose Data You Want To Update\n [title, target, details, start]")


def start():
    print("Welcome To My Simple Crow Fund Raising Project\n ----------------------------------------")
    while True:
        option = input("1) Type '1' For Registeration: \n2) or '2' For Login\n3) Exit: \n")
        if option == "1":
            registeration()
        elif option == "2":
            login()
        elif option == "3":
            print("Thanks For Your Time..Good Luck")
            break
        else:
            print('Wrong choice')
            start()

start()