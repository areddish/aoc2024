import requests
import datetime
import os

def get_input():
    year = datetime.datetime.now().year
    day = datetime.datetime.now().day
    SESSION = os.environ["AOC_SESSION"]
    req = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={ "session": SESSION})
    if req.status_code == 200:
        with open(f"day{day}.txt", "wt") as file:
            file.write(req.text) 
        print(f"Success! Day {day} of {year}")
    else:
        print("Failed to get input!")

if __name__ == "__main__":
    get_input()