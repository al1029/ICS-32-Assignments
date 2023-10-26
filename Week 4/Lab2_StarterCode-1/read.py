from pathlib import Path
import os
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
                if row[0] != "City" or row[1] != "Team Name" or row[2] != "Sport":
                    raise ValueError
            else:
                data.append(row[0] + row[1] + row[2])
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
    good_files = []
    sports_list = []
    current_dir = os.path.dirname(__file__)
    p = Path(current_dir)
    for file in p.glob('*.csv'):
        try:
            temp = readFile(file)
        except ValueError:
            bad_files.append(os.path.basename(file) + "\n")
        except IndexError:
            bad_files.append(os.path.basename(file)+ "\n")
        else:
            #TODO
            pass
    with open(os.path.join(current_dir, "error_log.txt"), "w") as txt_file:
        txt_file.writelines(bad_files)

    return []  # erase this


if __name__ == "__main__":
   """ FOR TESTING PURPOSES

   files = ["what\n", "is\n", "going\n", "on\n"]
    current_dir = os.path.dirname(__file__)
    p = Path(current_dir)
    print(p)
    for path in p.glob('*.py'):
        print(os.path.basename(path))
    with open(os.path.join(current_dir,"temp_file.txt"), "w") as txt_file:
        txt_file.writelines(files)"""