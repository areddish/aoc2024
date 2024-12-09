import requests
import datetime

def get_input():
    year = datetime.datetime.now().year
    day = datetime.datetime.now().day

    SESSION = "53616c7465645f5f00a35709f77f555119209457f207cf88e20ec0cfe5295fa5fd42fc3658d2289879f1f2e2d12ef683d71b2dc0db1b291ae75262f264782273"
    req = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={ "session": SESSION})
    if req.status_code == 200:
        with open(f"day{day}.txt", "wt") as file:
            file.write(req.text) 
        print(f"Success! Day {day} of {year}")
    else:
        print("Failed to get input!")

if __name__ == "__main__":
    get_input()