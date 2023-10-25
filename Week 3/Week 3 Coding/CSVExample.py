#Import my csv library for use
import csv
def writingToCSV():
    #Create a file object to connect to our CSV file
    with open("StudentList.csv", "w", newline="") as myCSVFile:
        #Creates writeTOMy CSV object to connect to my file object
        writeToMyCSV = csv.writer(myCSVFile)
        #This statement uses my writeToMyCSV object to write to myCSVFile
        #Writing column headers - note you don't need to add column headers
        writeToMyCSV.writerow(["Student Name", "Student ID", "Major"])

        #Write Data into my csv file
        writeToMyCSV.writerow(["John Doe", "12341234", "CS"])
        writeToMyCSV.writerow(["Jane Doe", "43214321", "CS"])
        writeToMyCSV.writerow(["Jon Doe", "12344321", "CS"])

def readingFromCSV():
    #Create a list to hold my student data
    StudentData = []

    #Create a file object to connect to our CSV file
    with open("StudentList.csv", "r", newline="") as myCSVFile:
        #Create a read stream connection to my file object
        readCSVData = csv.reader(myCSVFile)

        #Write a for loop to real all the data from the file
        #and put into my StudentList data structure
        for row in readCSVData:
            #Adds the row of data into my Student data list
            StudentData.append(row)

    StudentData.sort()
    #Returns the list that contains the read data
    return StudentData

#Calls the function to create/write to my csv file
writingToCSV()
#Calls the function to read the content of my csv file
print(readingFromCSV())