'''*****************************************************************************
Problem 1 Requirements:
Create a function called jump_game that takes a list of positive whole numbers.
Starting at the first index in the array, the integer value at any given index
is the maximum number of spots that you can jump forward within the array.
Return true if you can get to the last index position in the array and false if
you can never reach the final index position in the array.

Create a seperate Unit Test Module call jump_game_unit_test.py that tests a
happy path and failed test case.
*****************************************************************************'''
#***************Write Your Solution to Problem 1 below this line****************

def jumpgame(nums: list[int])-> bool:
    """Checks if you can reach the last index position of a list of whole numbers.

    The function checks each index and changes the value of reach if the index number plus the index is greater than
    the number in reach. Reach is the number of indices reachable in the list starting from index 1.
    If at any point the index is greater than the reach before arriving at the last index, false is
    returned because it implies that the last index is unreachable. If the function reaches the end of
    the list or reach is greater than the length of the list, True is returned.

    Args:
        nums: a positive list of whole numbers

    Returns:
        True or False
    """

    reach = 0
    for index in range(len(nums)):
        if reach >= len(nums) - 1:
            return True
        elif index > reach:
            return False
        #changes reach to the maximum value between the variable reach and the index plus the index number
        reach = max(reach, index + nums[index])
    return True









