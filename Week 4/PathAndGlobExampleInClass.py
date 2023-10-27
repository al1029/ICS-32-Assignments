from pathlib import Path
#This function takes in the path as a parameter
def userGivenPath(userPath):

    #Uses the string passed into the functino to create my path object
    p = Path(userPath)

    #Returns the created path
    return p

#This function will take a hardcoded/static path to use
def staticPath():
    #Create my path object p using Path
    #For Mac users to hardcode a directory it would be:
    #P = Path("C:/Users/m_ibr/OneDrive/Desktop/Lectures/Week 3/")
    p = Path("C:\\Users\\m_ibr\\OneDrive\\Desktop\\Lectures\\Week 3")

    #returns my path object to the calling function
    return p

#This function performs the file and path example
def fileAndPaths(myReturnedPathObject):
    #Create a new combined path object that adds a file to my original path
    #Change the filename to noe that does't exist and then check if it exists.
    myFilePath = myReturnedPathObject/Path("StudentList.csv")

    #Check is the path the path object is point exists
    print("\nDoes this path exist? ",myFilePath.exists())

    #Check if the path is a directory
    print("\nIs this path a directory? ", myFilePath.is_dir())

    if (myFilePath.is_file() == True):
        #Creates a file object that points to the file myFilePath is pointing
        myFile = myFilePath.open("r")
        print(myFile.readlines())

#This function performs the file and path example
def checkMyPathObject(myReturnedPathObject):
    #Prints the value of the stored path
    print("This my user given path:\n", myReturnedPathObject)

    #Check is the path the path object is point exists
    print("\nDoes this path exist? ",myReturnedPathObject.exists())

    #Check if the path is a directory
    print("\nIs this path a directory? ", myReturnedPathObject.is_dir())

    #Check if the path is a file
    print("\nIs this path a file? ", myReturnedPathObject.is_file())

#A function that uses the glob function on a path object
def myGlobAndPath(myReturnedPathObject):
    #Use the glob to filter
    globbedPath = myReturnedPathObject.glob("*.csv")
    for files in globbedPath:
        print(files)

#Condtional statement to only run the below code when this is the main module
if __name__ == "__main__":
    #Calls the static path function and prints the returned path object
    print("This is my path object:\n",type(staticPath()))

    #Calls the userGivenPath function and stores the returned path in a local var
    myReturnedPathObject = staticPath()

    checkMyPathObject(myReturnedPathObject)
    fileAndPaths(myReturnedPathObject)
    myGlobAndPath(myReturnedPathObject)