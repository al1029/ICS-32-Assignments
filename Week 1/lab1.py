
"""
Name: Alex Gonzalez
UCINetID: 61761325
"""

class NoStaircaseSizeException(Exception):
    pass

class IntegerOutOfRangeException(Exception):
    pass

class EndProgram(Exception):
    pass

''' This functions asks the user for the number of steps
they want to climb, gets the value provided by the user
and returns it to the calling function. This function will
raise any exceptions related to none integer user inputs.'''
def getUserInput():
    user_input = input("Please input your staircase size:")
    if user_input == "DONE":
        raise EndProgram
    return int(user_input)

''' This function takes the number of steps as an input parameter,
creates a string that contains the entire steps based on the user input
and returns the steps string to the calling function. This function will raise
any exceptions resulting from invalid integer values.
'''
def createSteps(stepCount):
    num_step = stepCount
    staircase = ""
    check = False
    if num_step == 0:
        raise NoStaircaseSizeException
    elif num_step < 0 or num_step >= 1000:
        raise IntegerOutOfRangeException
    else:
        check = True

    if check:
        iterated_steps = num_step
        staircase += " " * calcSpaces(iterated_steps)
        staircase += "+-+\n"
        staircase += " " * calcSpaces(iterated_steps)
        staircase += "| |\n"
        iterated_steps -= 1
    
        while True:
            if iterated_steps == 0:
                staircase += "+-+"
                break
            num_spaces = calcSpaces(iterated_steps)
            staircase += " " * num_spaces
            staircase += "+-+-+\n"
            staircase += " " * num_spaces
            staircase += "| |\n"
            iterated_steps -= 1
        return staircase
    
"""This function calculates the number of spaces needed to align the staircase"""
def calcSpaces(steps):
    return (steps * 2) - 2

'''This function kicks off the running of your program. Once it starts
it will continuously run your program until the user explicitly chooses to
end the running of the program based on the requirements. This function returns
the string "Done Executing" when it ends. Additionally, all exceptions will be
handled (caught) within this function.'''
def runProgram():
    while True:
        try:
            createSteps(getUserInput())
        except NoStaircaseSizeException:
            print("I cannot draw a staircase with no steps.")
        except IntegerOutOfRangeException:
            print("That staircase size is out of range.")
        except ValueError:
            print("Invalid staircase value entered.")
        except EndProgram:
            return "Done Executing"
    
'''Within this condition statement you are to write the code that kicks off
your program. When testing your code the code below this
should be the only code not in a function and must be within the if
statement. I will explain this if statement later in the course.'''
if __name__ == "__main__": 
    runProgram()