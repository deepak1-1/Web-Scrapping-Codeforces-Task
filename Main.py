# importing requests to generate request to server
import requests

# importing BeautifulSoup just to traverse over the data 
# which is fetched using requests module 
from bs4 import BeautifulSoup

# os.startfile is used to run a file and os.system to do operations on cmd like clear screen
# we are going to use it for viewing csv file which we will generate later
from os import startfile,system

# importing exit just to terminate our program or stop it to be further executed
from sys import exit

# It is used to create a csv file to store that particular information
import csv

#It will be used to work with date's for submissions
from datetime import datetime,timedelta

#for working with command line argument
import argparse



#Class Created for handle all submission data
class SubmissionsData:

    #for writing a csv file only for accepted
    csvMainList = ["Question","Accepted","Runtime","Wrong","Time",
                        "Compilation","lastDate","lastTime"
                      ]

    # For writing First row in csv file
    csvMainDict = {"Question":"Question's Name",
                    "Accepted":"Accepted",
                    "Runtime":"Runtime Error",
                    "Wrong": "Wrong On test cases",
                    "Time":"Time Limit Exceed",
                    "Compilation" : "Compilation Error",
                    "lastDate" : "Changed on Last Date",
                    "lastTime": "Changed on Last time"
                    }


    # just a constructor function 
    def __init__(self,handle_name):

        self.handle_name = handle_name

        #set a basic url which will direct us towards user submission if exists
        self.url = f"https://codeforces.com/submissions/{handle_name}"

        # initializing a basic dict which will store our data
        self.dataDict = {}


    # fetching all user submission data
    def fetchSubmissionData(self):

        # var will help us in moving in pages upto we want
        var = 1

        # variable to help in breaking while loop if it repeats
        start = 0

        # looping to fetch all pages data of users submissions
        while True:

            #creating a simple request to server and fetching it's text part
            response = requests.get(self.url+f"/page/{var}").text

            traverseElement = BeautifulSoup( response, "html.parser" )

            #moving towards main data table through Traversing upper created soup
            mainContent = traverseElement.find("table",{"class":"status-frame-datatable"})

            # just to check a condition so that we can stop our while loop if it repeats
            flag = 0

            #looping inside main content and fetching more detail and storing them
            for submissions in mainContent.findAll("tr"):

                content = submissions.findAll("td")

                #list for storing data of particular td
                dataList = []

                #looping to main data to store them
                for items in content:
                    #appending each item in data after stripping it 
                    dataList.append(items.text.strip())

                #checking if list is empty or not so that we can perform operations
                if dataList:
                    #just breaking condition if it repeats
                    if start != 0 and flag == 0:
                        if uniqueCode == dataList[0]:
                            break    

                    #for storing first #code of submission so that we can break while loop
                    if flag == 0:
                        uniqueCode = dataList[0]
                        start = 1
                        flag = 1


                    # now storing it in main dict
                    if dataList[3] not in self.dataDict.keys():

                        #creating and inserting sub dict and using key as questions name we fetched
                        self.dataDict[f"{dataList[3]}"] = {
                                                            "Question":dataList[3],
                                                            "Accepted":0,
                                                            "Runtime":0,
                                                            "Wrong":0,
                                                            "Time":0,
                                                            "Compilation":0,
                                                            "lastDate":None,
                                                            "lastTime":None
                                                            # "#code": []
                                                            }

                    #checking for sub keys in dataDict if it doesn't exists then adding it

                    if dataList[5].split()[0] not in self.dataDict[f"{dataList[3]}"].keys():
                        self.dataDict[f"{dataList[3]}"].update({ dataList[5].split()[0] : 0})

                    # Checking element for list if don't exists then adding it 
                    if dataList[5].split()[0] not in self.csvMainList:
                        self.csvMainList.append(dataList[5].split()[0])
                        self.csvMainDict[f"{dataList[5].split()[0]}"] : f"{dataList[5].split()[0]}"
                    else:
                        self.dataDict[f"{dataList[3]}"][dataList[5].split()[0]] += 1

                    # Setting last date of changes done in submissions for particular questions and time too
                    self.dataDict[f"{dataList[3]}"]["lastDate"] = dataList[1].split()[0]
                    self.dataDict[f"{dataList[3]}"]["lastTime"] = dataList[1].split()[1]

                    #Storing #code of each solution
                    # self.dataDict[f"{dataList[3]}"]["#code"].append(dataList[0])


            #just breaking condition if it repeats
            if start != 0 and flag == 0:
                if dataList:
                    if uniqueCode == dataList[0]:
                        break

            print(f"\tFetched {var} pages and no of questions - {len(self.dataDict)}")
            #increasing variable var so that we can move to next page
            var += 1                

    #It will print all data in Dict to cmd panel or where you executed it            
    def printingDictElement(self):
        for i in self.dataDict:
            print(f"{self.dataDict[i]}")

        print(len(self.dataDict))


    #It will print all accepted question to a csv file Created on the basis of handle name
    def acceptedCsv(self):

        #it is creating a new file if don't exists before using handle name
        with open(f"{self.handle_name}'s Accepted.csv","w",newline='',encoding="utf-8") as csvfile:
            
            # again creating a writer object but this time it is dictwriter so that 
            # we have ease of writing our dict details to it
            csvwriter = csv.DictWriter(csvfile,self.csvMainList)
            csvwriter.writerow(self.csvMainDict)
            for items in self.dataDict:
                if self.dataDict[items]["Accepted"] == 1:
                    csvwriter.writerow(self.dataDict[items])

        #this is os module's startfile function which is used to open a particular file 
        startfile(f"{self.handle_name}'s Accepted.csv")


    #It will print not accepted question to a csv file Created on the basis of handle name
    def notAcceptedCsv(self):

        #it is creating a new file if don't exists before using handle name
        with open(f"{self.handle_name}'s notAccepted.csv","w",newline='',encoding="utf-8") as csvfile:
            
            # again creating a writer object but this time it is dictwriter so that 
            # we have ease of writing our dict details to it
            csvwriter = csv.DictWriter(csvfile,self.csvMainList)
            csvwriter.writerow(self.csvMainDict)
            for items in self.dataDict:
                if self.dataDict[items]["Accepted"] == 0:
                    csvwriter.writerow(self.dataDict[items])

        #this is os module's startfile function which is used to open a particular file 
        startfile(f"{self.handle_name}'s notAccepted.csv")        


    #it will print all submission to csv file
    def allSubmissionsCsv(self):
        #it is creating a new file if don't exists before using handle name
        with open(f"{self.handle_name}'s submissions.csv","w",newline='',encoding="utf-8") as csvfile:
            
            # again creating a writer object but this time it is dictwriter so that 
            # we have ease of writing our dict details to it
            csvwriter = csv.DictWriter(csvfile,self.csvMainList)
            csvwriter.writerow(self.csvMainDict)

            #this loop will allow every submission to be written in csv file
            for items in self.dataDict:
                csvwriter.writerow(self.dataDict[items])

        #this is os module's startfile function which is used to open a particular file 
        startfile(f"{self.handle_name}'s submissions.csv")  


    #it will print all submissions which was done before n days to till now
    def aboutnDaysAgo(self):

        while True:
            # clearing cmd screen
            system('cls')

            #handling this try except block just to check a user enter only integer value not others
            try:
                n = int(input("\n\n\n\t\tEnter days(positive) you want to start from: "))
                #handling this try except block just to check user enter a positive integer only
                if n<0:
                    #this will genrate an exception of negative error
                    raise Exception("NegativeError")

            except ValueError:
                print("\n\t\tPlease enter a integer!")
                ans = input("\n\t\tDo you want to go back(y/n)? ")
                if ans.upper() == "Y":
                    return
                #it will continue the loop if user want to try more
                continue
                
            except Exception as e:
                #this will print a simple msg and ask if user want to go back
                print("\n\t\tPlease Enter a positive integer!")
                ans = input("\n\t\tDo you want to go back(y/n)? ")
                if ans.upper() == "Y":
                    return
                #it will continue the loop if user want to try more
                continue
            
            else:
                break
        #this is datetime object having values of date and time when it is executed
        todayDateTime = datetime.now()
        #again datetime object and used delta function to find back date so that we can work further
        nDaysAgoDate = (todayDateTime - timedelta( n )).date()

        with open(f"{self.handle_name} {n} days Ago till now.csv","w",newline='',encoding="utf-8") as csvfile:
            
            # again creating a writer object but this time it is dictwriter so that 
            # we have ease of writing our dict details to it
            csvwriter = csv.DictWriter(csvfile,self.csvMainList)
            csvwriter.writerow(self.csvMainDict)

            for element in self.dataDict:

                #creating digit combination through month name using strptime function of datetime module
                submissionLastDate = datetime.strptime(
                                                self.dataDict[element]["lastDate"],
                                                "%b/%d/%Y"
                                                ).date()
                # comparing each lastsubmission date of a question to nDaysAgoDate for writing in a csv file
                if submissionLastDate > nDaysAgoDate:
                    csvwriter.writerow(self.dataDict[element])
        #just Starting a csvfile
        startfile(f"{self.handle_name} {n} days Ago till now.csv")

    #It will print all solution after that date user will provide and check validation of date too
    def afterTheDate(self):
        #just starting while so that we can take input again if user wants
        while True:
            # clearing cmd screen
            system('cls')
            userDate = input("\n\n\n\t\tDate(dd/mm/yyyy) you want to start: ")

            # validating date provided by user through ValueError in try except block
            try:
                userDate = datetime.strptime(userDate,"%d/%m/%Y").date()
            except ValueError:
                print("\n\t\tThe date provided by you is not correct")
                ans = input("\t\tyou want to go back(y/n)? ")
                if ans.upper() == "Y":
                    return
            except Exception as e:
                print(f"\n\t\tSome other issue({e})")
                return
            else:
                break


        with open(f"{self.handle_name}'s submissions after {userDate}.csv"
                            ,"w",newline='',encoding="utf-8") as csvfile:
            
            # again creating a writer object but this time it is dictwriter so that 
            # we have ease of writing our dict details to it
            csvwriter = csv.DictWriter(csvfile,self.csvMainList)
            csvwriter.writerow(self.csvMainDict)

            # Traversing thorugh dataDict elements and comparing it with userDate
            for element in self.dataDict:

                #creating digit combination through month name using strptime function of datetime module
                submissionLastDate = datetime.strptime(
                                                self.dataDict[element]["lastDate"],
                                                "%b/%d/%Y"
                                                ).date()
                if submissionLastDate > userDate:
                    csvwriter.writerow(self.dataDict[element])

        # starting a csv file having data
        startfile(f"{self.handle_name}'s submissions after {userDate}.csv")

def mainCmdWindow(handle):

    # just checking if handle was through command line object or not and working accordingly
    if handle:
        #creating an object of class
        handleData = SubmissionsData(handle)

        # just checking whether handle name exists on code forces or not 
        try:
            handleData.fetchSubmissionData()
        except AttributeError:
            print("\n\t\tHandle name you provided in command line doesn't exists!")
            return
        else:
            #this will create a csv file and start it 
            handleData.allSubmissionsCsv()
    #when user have not provided any handle name so it will start
    else:

        while True:

            system("cls")

            #getting input to check whether the given user exists or not
            handle_name = input("\n\n\n\t\tEnter Handle name of which you want to fetch details: ")

            #creating an object of class
            handleData = SubmissionsData(handle_name)

            # just checking whether handle name exists on code forces or not 
            try:
                handleData.fetchSubmissionData()
            except AttributeError:
                print("\n\t\tHandle name you provided in command line doesn't exists!")
                ans = input("\n\t\tDo you want exit(y/n)? ")
                if ans.upper() == "Y":
                    return
                continue
            else:
                #this is just while to perform different task over same object 
                while True:

                    system("cls")

                    print("\n\n\n\t\t\tPlease Choose your option")
                    print("\n\t\t1.Only create Csv file for accepted questions")
                    print("\t\t2.Only create Csv File for not accepted questions")
                    print("\t\t3.for All Submission in csv File")
                    print("\t\t4.Start before n days till now")
                    print("\t\t5.Start from Date to till now")
                    print("\t\t6.Want to go back to change handle name")
                    print("\t\t7.Exit")
                    

                    ans = int(input("\n\t\tInput: "))

                    if ans == 1:
                        handleData.acceptedCsv()
                    elif ans == 2:
                        handleData.notAcceptedCsv()
                    elif ans == 3:
                        handleData.allSubmissionsCsv()
                    elif ans == 4:
                        handleData.aboutnDaysAgo()
                    elif ans == 5:
                        handleData.afterTheDate()
                    elif ans == 6:
                        break
                    elif ans == 7:
                        exit()
                    else:
                        print("\n\t\tPlease Enter a valid choice!")




            system("cls")
            ans = input("\n\n\n\t\tDo you want to exit(y/n)? ")
            if ans.upper() == "Y":
                exit()#

        
        

if __name__ == "__main__":
    # taking command line argument if user provided 
    parser = argparse.ArgumentParser()

    # setting handle as an command line argument
    parser.add_argument("--handle",type=str,help="Handle Name to work with")
    # fetching provided arguments
    args = parser.parse_args()
    
    # Calling our main cmd window by passing handle as argument to it 
    mainCmdWindow(args.handle)
    

