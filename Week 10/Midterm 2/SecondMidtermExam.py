'''*****************************************************************************
Problem 1 Requirements:
A committee is setting up a tournament, the committee will only know the number
of players who will be playing against each other once registration for the
tournament has closed. The winner of each games moves to the next round while
losers go home. If there is an extra person registered (I.e. An odd number of
players), a randomly selected person will automatically move to the next
round. If there are no players registered then the tournament will be cancelled
without playing any games. You should assume that the number of players is
positive, even if the number of registered players given to you is negative.
Given this situation, write a function "number_of_games" that takes the number of registered
players as an argument and returns the number of games that will need to be
played before we have a winner.
*****************************************************************************'''
#***************Write Your Solution to Problem 1 below this line****************
def number_of_games(num):
    if num == 0:
        return 0
    return abs(num) - 1













'''*****************************************************************************
Problem 2 Requirements:
Write a recursive function called "character_count" that will count the number
of times a character will occur in a string. The function will have the string
and the character to count and return the number of times it occured.
*****************************************************************************'''
#***************Write Your Solution to Problem 2 below this line****************
def character_count(string, char):
    if not string:
        return 0
    
    if string[0] == char:
        count = 1
    else:
        count = 0

    return count + character_count(string[1:], char)




if __name__ == "__main__":
    print(character_count("hello", "l"))