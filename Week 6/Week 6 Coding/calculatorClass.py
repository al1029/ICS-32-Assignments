#Creating a class for a simple/basic calculator
class Calculator():
    #define my class variables
    __calcResult__ = 0

    #define my constructor for my calculator class
    def __init__(self):
        #initialize my class variables as part of my constructor
        self.__calcResult__ = 0

    #define getter/accessor method for getting the result value
    def getResult(self):
        return self.__calcResult__
    
    #define setter/mutator method for setting the result value
    def setResult(self, result):
        self.__calcResult__ = result

    #define the method that performs addition
    def addNumbers(self, num1, num2):
        self.setResult(num1 + num2)

    #define the method that performs the subtraction
    def subNumbers(self, num1, num2):
        self.setResult(num1 - num2)

    #define the method that performs the multiplication
    def mulNumber(self, num1, num2):
        self.setResult(num1 * num2)

    #define the method that performs devision operation
    def divNumbers(self, num1, num2):
        self.setResult(num1 / num2)

    #define the method that perfroms the correct operation
    def checkOperation(self, operation, num1, num2):
        if(operation == "+"):
            self.addNumbers(num1, num2)
        elif(operation == "-"):
            self.subNumbers(num1, num2)
        elif(operation == "*"):
            self.mulNumber(num1, num2)
        elif(operation == "//"):
            self.divNumbers(num1, num2)
        else:
            pass

#Adding a if block to test my class
if __name__ == "__main__":
    #create a calculator object instance
    testCalc = Calculator()

    #confirm the class variables initialized
    print(testCalc.getResult()) 

    #test the plus operation and print results
    testCalc.checkOperation("+", 5, 3)
    print(testCalc.getResult())

    #test the plus operation and print results
    testCalc.checkOperation("-", 5, 3)
    print(testCalc.getResult())

    #test the plus operation and print results
    testCalc.checkOperation("*", 5, 3)
    print(testCalc.getResult())

    #test the plus operation and print results
    testCalc.checkOperation("/", 5, 3)
    print(testCalc.getResult())