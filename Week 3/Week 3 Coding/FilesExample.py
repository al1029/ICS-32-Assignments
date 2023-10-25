#Create a file object to connect to a file
#inputFileObj = open("SampleInputFile.txt", "r+")

myPath = "C:\\Users\\Alex\\OneDrive\\Desktop\\ICS 32 Assignments\\"

#Create a file object to connect to a file in write mode
inputFileObj = open(myPath+"Files\\SampleInputFile.txt","w")

#Create a file object to connect to a file in append mode
#inputFileObj = open("SampleInputFile.txt", "a")

#Create a file object to connect to a file in read and write mode
#inputFileObj = open("SampleInputFile.txt", "r+")

"""
#Read an dprint a line from the file my object is pointing to up to a newline
#This example reads one line at a time
fileContent = inputFileObj.readline()
print("First Line: ", fileContent)
fileContent = inputFileObj.readline()
print("Second Line: ", fileContent)
fileContent = inputFileObj.readline()
print("Third Line: ", fileContent)
fileContent = inputFileObj.readline()
print("Fourth Line: ", fileContent)
"""

#Write some data to my file.
inputFileObj.write("I am now writing to my file.\n")
#inputFileObj.close() 

#Write a loop to get all the content of the file
"""for nextLine in inputFileObj:
    print(nextLine, end="")
inputFileObj.close()"""

#Using with keyword we can guard our file to ensure its closed
with open("AnotherFileWith.txt","w+") as anotherFileObj:
    anotherFileObj.write("This is the first line in my new file.\n")
    anotherFileObj.write("This is the second line in my new file.\n")