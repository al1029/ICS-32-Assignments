from pathlib import Path
import csv
from sportclub import SportClub
from typing import List, Tuple


def readFile(file: Path) -> List[Tuple[str, str, str]]:
    """Read a CSV file and return its content

    A good CSV file will have the header "City,Team Name,Sport" and appropriate content.

    Args:
        file: a path to the file to be read

    Returns:
        a list of tuples that each contain (city, name, sport) of the SportClub

    Raises:
        ValueError: if the reading csv has missing data (empty fields)  
    """
    data = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                if row[0] != "City" or row[1] != "Team Name" or row[2] != "Sport" or len(row) > 3:
                    raise ValueError
                else:
                    line_count += 1
            else:
                temp_tuple = (row[0], row[1], row[2])
                data.append(temp_tuple)
                line_count += 1
    return tuple(data)


def readAllFiles() -> List[SportClub]:
    """Read all the csv files in the current working directory to create a list of SportClubs that contain unique SportClubs with their corresponding counts

    Take all the csv files in the current working directory, calls readFile(file) on each of them, and accumulates the data gathered into a list of SportClubs.
    Create a new file called "report.txt" in the current working directory containing the number of good files and good lines read. 
    Create a new file called "error_log.txt" in the current working directory containing the name of the error/bad files read.

    Returns:
        a list of unique SportClub objects with their respective counts
    """
    bad_files = []
    good_files = 0
    lines_read = 0
    sports_list = []
    new_sports_list = []

    #current_dir = os.path.dirname(__file__)
    p = Path(".")
    for file in p.glob('*.csv'):
        try:
            data = readFile(file)
            for i in data:
                sports_list.append(SportClub(i[0], i[1], i[2]))
            lines_read += file_lines(file)
            print(str(file))
            good_files += 1
        except ValueError:
            if str(file) != "survey_database.csv":
                bad_files.append(str(file) + "\n")
        except IndexError:
            if str(file) != "survey_database.csv":
                bad_files.append(str(file) + "\n")

    #creates a new sports list with the number of times picked added
    index = 0
    while index < len(sports_list):
        if index == 0:
            sports_list[index].incrementCount()
            new_sports_list.append(sports_list[index])
            index += 1
        elif any(x == sports_list[index] for x in new_sports_list):
            for i in new_sports_list:
                if i == sports_list[index]:
                    i.incrementCount()
            index += 1
        else:
            sports_list[index].incrementCount()
            new_sports_list.append(sports_list[index])
            index += 1

    #creates an error log file to store bad files
    with open("error_log.txt", "w") as txt_file:
        txt_file.writelines(bad_files)

    #creates a report text file to store the number of good files and lines read
    with open("report.txt", "w") as txt_file:
        txt_file.writelines("Number of files read: " + str(good_files) + "\n" + "Number of lines read: " + str(lines_read) + "\n")

    return new_sports_list


def file_lines(file):
#counts the number of lines in a file
    with open(file) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


if __name__ == "__main__":
    """data = []
    sports_list = []
    new_sports_list = []
    current_dir = os.path.dirname(__file__)
    p = Path(os.path.join(current_dir, "testcsvfile.csv"))
    with open(p) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                if row[0] != "City" or row[1] != "Team Name" or row[2] != "Sport":
                    raise ValueError
                else:
                    line_count += 1
            else:
                temp_tuple = (row[0], row[1], row[2])
                data.append(temp_tuple)
                line_count += 1
    for i in data:
        sports_list.append(SportClub(i[0], i[1], i[2]))

    
    index = 0
    while index < len(sports_list):
        if index == 0:
            sports_list[index].incrementCount()
            new_sports_list.append(sports_list[index])
            index += 1
        elif any(x == sports_list[index] for x in new_sports_list):
            for i in new_sports_list:
                if i == sports_list[index]:
                    i.incrementCount()
            index += 1
        else:
            sports_list[index].incrementCount()
            new_sports_list.append(sports_list[index])
            index += 1
    print(str(index))
    for i in new_sports_list:
        print(i.__str__())"""



        #[SportClub("Houston", "Rockets", "NBA", 80), SportClub("LA", "Warriors", "NBA", 130), SportClub("LA", "Lakers", "NBA", 130)] 