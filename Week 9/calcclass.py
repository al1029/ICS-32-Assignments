class DivideByZeroError(Exception):
    pass

class Calculator():
    __calcResult__ = 0

    def __init__(self):
        self.__calcResult__ = 0

    def getResult(self):
        return self.__calcResult__
    
    def setResult(self, result):
        self.__calcResult__ = result
    
    def addNumbers(self, num1, num2):
        self.setResult(num1 + num2)

    def subNumbers(self, num1, num2):
        self.setResult(num1 - num2)

    def mulNumbers(self,num1,num2):
        self.setResult(num1 * num2)

    def divNumbers(self, num1, num2):
        if num2 == 0:
            raise DivideByZeroError
        else:
            self.setResult(num1 / num2)