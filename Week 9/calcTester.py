#import the unit test library
import unittest

#input the calculator class
import calcclass as cc

#class that will include our test cases and inherit the unit test test case
#functionality from the unittest library
class calcTester(unittest.TestCase):
    testCaseNumber = 1
    myCalc = cc.Calculator()

    #Providing code to setup our test cases
    def setUp(self):
        print("Starting test case ", calcTester.testCaseNumber, ".")

    #Providing code to wrap up a test case
    def tearDown(self):
        print("Completed executing test case ", self.testCaseNumber, ".\n")
        calcTester.testCaseNumber = calcTester.testCaseNumber + 1

    #Writing a normal test scenario of 1 plus 1
    def test_OnePlusOneTestCase(self):
        self.myCalc.addNumbers(1, 1)
        self.assertEqual(self.myCalc.getResult(), 2)
        print(" I am in test case ", calcTester.testCaseNumber)
        self.assertEqual(self.myCalc.getResult(), 1)

    #Define a error test case raises DivideByZeroError
    def test_DivideByZero(self):
        with self.assertRaises(cc.DivideByZeroError): #ZeroDivisionError):
            self.myCalc.divNumbers(1, 0)

#Calling unittest.main runs our unit testing
if __name__ == "__main__":
    unittest.main()