from concurrent.futures import thread
import threading
from turtle import Turtle
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

url = input("URL: ")
threads = input("Number of Threads [5]: ")
if threads == "":
    threads = 5
else:
    threads = int(threads)

show_200_code = input("Verbose-Mode for 200-Code(y/N)?")
if show_200_code == "" or show_200_code == "n" or show_200_code == "N":
    show_200_code = False
else:
    show_200_code = True

def attack(line_to_start, number_of_lines, thread_number):
    print(f"{bcolors.OKCYAN}[*] Starting Thread No.{thread_number}")
    with open("user-agents/user-agents.txt") as agents:

        d = 0
        actual_line = 0
        
        for agent in agents:
            if actual_line < line_to_start:
                actual_line += 1
            
            elif actual_line >= line_to_start+number_of_lines:
                print(f"{bcolors.OKCYAN}[*] Exiting Thread No.{thread_number}. Finished.")
                exit()
            else:
                agent.strip()
                agent = agent.split("\n")[0]
                user_agent = {'User-agent': agent}
                try:
                    response  = requests.get(url, headers = user_agent)
                    code = response.status_code
                    if code - 200 < 100 and code-200 >= 0:
                        col = bcolors.OKCYAN
                        print(f"{bcolors.ENDC}Agent accepted - Code: {col}{response.status_code} - Agent: {agent}")
                        if show_200_code == False:
                            print(LINE_UP,end=LINE_CLEAR)

                    elif code - 400 < 100 and code-400 >= 0:
                        col = bcolors.WARNING
                        print(f"{bcolors.FAIL}Agent Error - Code: {col}{response.status_code} - Agent: {agent}")

                    elif code - 500 < 100 and code-500 >= 0:
                        col = bcolors.FAIL
                        print(f"{bcolors.FAIL}Server Error - Code: {col}{response.status_code} - Agent: {agent}")

                    actual_line += 1
                except Exception as f:
                    print("{}Exception: {}".format(bcolors.FAIL, f))
                    d += 1
                    if d >= 3:
                        print(f"{bcolors.FAIL}Too many errors, exiting...")
                        exit()



def get_number_of_lines():
    file = open("user-agents/user-agents.txt", "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count

def main():
    number_of_lines = get_number_of_lines()//threads
    for i in range(threads):
        x = threading.Thread(target=attack, args=(i*number_of_lines, number_of_lines, i, ))
        x.start()
        #x.join()

if __name__ == "__main__":
    main()