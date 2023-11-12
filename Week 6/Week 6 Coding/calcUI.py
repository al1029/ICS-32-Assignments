#import the calculator function from my Calculator class
import calculatorClass as calc

#import tkinter from the standard library
import tkinter as tk

#import the tkk names from tkinter
from tkinter import ttk

#Defining a CalcUI Class for our User INterface
class calcUIPacker():
    #Defining a class variable of Calculator Class type
    myCalc = 0

    #Define class variable to store my tkinter object
    master = 0

    #Define my tkinter class variable
    num1 = 0
    num2 = 0
    operation = 0
    result = 0

    #Define my class contructor
    def __init__(self):
        #initializing my calculator class variable
        self.myCalc = calc.Calculator()

        #call my method to create my canvas and add my widgets
        self.canvasSetup()
        self.initTKVariables()
        self.returnKeyBind()
        self.createNumber1Entry()
        self.createOperationCombobox()
        self.createNumber2Entry()
        self.createResultLabel()
        self.createSubmitButton()
        self.createQuitButton()
        self.runUI()

    #define a method that initializes my tk variables
    def initTKVariables(self):
        self.num1 = tk.IntVar()
        self.num2 = tk.IntVar()
        self.operation = tk.StringVar()
        self.result = tk.IntVar()

    #define a method to setup my canvas
    def canvasSetup(self):
        #initialize my tkinter canvas
        self.master = tk.Tk()
        self.master.title("Basic Calculator") #sets the window title
        self.master.geometry("400x400") #sets the default size of the window
        self.master.configure(background="blue") #sets the background color of the window
        self.master.resizable(0,0)#sets the x(horizontal) and y(verticle) to not be resizable

    #define a method that creates a quit button
    def createQuitButton(self):
        self.quitButton = tk.Button(self.master, text="Quit",command=self.master.destroy).pack()

    #define a method that creates a number entry field
    def createNumber1Entry(self):
        self.num1Entry = tk.Entry(self.master, textvariable = self.num1)
        self.num1Entry.pack()

    #define a method that creates a number entry field
    def createNumber2Entry(self):
        self.num2Entry = tk.Entry(self.master, textvariable = self.num2)
        self.num2Entry.pack()

    #define a method that creates a label for my result
    def createResultLabel(self):
        self.result.set("")
        self.resultLabel = tk.Label(self.master, textvariable=self.result, width=25).pack()

    #define a submit button on the UI
    def createSubmitButton(self):
        self.submitButton = tk.Button(self.master, text="Submit", command=self.calculateResult).pack()

    #define a method that triggers the calculation
    def calculateResult(self, event=None):
        self.myCalc.checkOperation(self.operation.get(), self.num1.get(), self.num2.get())
        self.result.set(self.myCalc.getResult())


    #define a method that creates a combobox with the operation values
    def createOperationCombobox(self):
        operationValues = ["+","-","*","\\"]
        self.operation.set("Please select an option")
        self.opCombobox = ttk.Combobox(self.master, textvariable=self.operation, values=operationValues).pack()
   
    #dfine a method that binds the return/enter key to also calculate the result
    def returnKeyBind(self):
        self.master.bind("<Return>", self.calculateResult)

    #define a method to start UI
    def runUI(self):
        #starts my UI - event handler
        self.master.mainloop()

#If statement for testing
if __name__ == "__main__":
    basicCalc = calcUIPacker()
    #This is to confirm that I have access to the members of the calculator object
    #print(basicCalc.myCalc.getResult())
