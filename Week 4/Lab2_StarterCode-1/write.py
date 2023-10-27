import csv
from sportclub import SportClub
from typing import List, Iterable
from itertools import groupby


def separateSports(all_clubs: List[SportClub]) -> Iterable[List[SportClub]]:
    """Separate a list of SportClubs into their own sports

    For example, given the list [SportClub("LA", "Lakers", "NBA"), SportClub("Houston", "Rockets", "NBA"), SportClub("LA", "Angels", "MLB")],
    return the iterable [[SportClub("LA", "Lakers", "NBA"), SportClub("Houston", "Rockets", "NBA")], [SportClub("LA", "Angels", "MLB")]]

    Args:
        all_clubs: A list of SportClubs that contain SportClubs of 1 or more sports.

    Returns:
        An iterable of lists of sportclubs that only contain clubs playing the same sport. 
    """
    sorted_clubs = all_clubs
    sorted_clubs.sort(key=lambda x: x.getSport())
    sorted_clubs = [list(i) for j, i in groupby(sorted_clubs, lambda a: a.getSport())]
    return sorted_clubs


def sortSport(sport: List[SportClub]) -> List[SportClub]:
    """Sort a list of SportClubs by the inverse of their count and their name

    For example, given the list [SportClub("Houston", "Rockets", "NBA", 80), SportClub("LA", "Warriors", "NBA", 130), SportClub("LA", "Lakers", "NBA", 130)] 
    return the list [SportClub("LA", "Lakers", "NBA", 130), SportClub("LA", "Warriors", "NBA", 130), SportClub("Houston", "Rockets", "NBA", 80)]

    Args:
        sport: A list of SportClubs that only contain clubs playing the same sport

    Returns:
        A sorted list of the SportClubs  
    """
    # hint: check documentation for sorting lists 
    # ( https://docs.python.org/3/library/functions.html#sorted , https://docs.python.org/3/howto/sorting.html#sortinghowto )
    sorted_list = sport
    sorted_list.sort(key=lambda x:(-x.getCount(), x.getName()))
    return sorted_list


def outputSports(sorted_sports: Iterable[List[SportClub]]) -> None:
    """Create the output csv given an iterable of list of sorted clubs

    Create the csv "survey_database.csv" in the current working directory, and output the information:
    "City,Team Name,Sport,Number of Times Picked" for the top 3 teams in each sport.

    Args:
        sorted_sports: an Iterable of different sports, each already sorted correctly
    """
    """for i in sorted_sports:
        temp_list = []
        for index, sport in enumerate(i):
            if index > 2:
                break
            else:
                temp_list.append(sport.getCity(), sport.getName(), sport.getSport(), sport.getCount())
        rankings.append(temp_list)
    rankings.sort(key=lambda x: x[0].getCount())"""
    
        


    with open("survey_database.csv", "w", newline="") as f:
        csv_writer = csv.writer(f)

        csv_writer.writerow(["City", "Team Name", "Sport", "Number of Times Picked"])
        for sport in sorted_sports:
            temp_list = []
            sport_number = 0
            for i in sport:
                if sport_number > 2:
                    break
                else:
                    temp_list = [i.getCity(), i.getName(), i.getSport(), i.getCount()]
                    csv_writer.writerow(temp_list)
                    sport_number += 1
                    temp_list = []

if __name__ == "__main__":
    """sorted_list = [SportClub("Washington","Nationals","MLB",1), SportClub("Toronto","Raptors","NBA",3), SportClub("Kansas City","Chiefs","NFL",1), SportClub("Tampa Bay", "Lightning", "NHL",1)]
    sorted_list.sort(key=lambda x:(-x.getCount(), x.getName()))
    for sport in sorted_list:
        print(sport.__str__())"""