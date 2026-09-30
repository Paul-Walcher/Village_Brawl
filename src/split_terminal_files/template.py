import sys
from pathlib import Path

#adding path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import terminal_functions as terminal
import time
import os


if __name__ == "__main__":

    #first comes the exit signal
    termination_filename = sys.argv[1]
    head, tail = os.path.split(termination_filename)



    #now checking if the file exists:
    while 1:

        if tail in os.listdir(head):
            break

    os.remove(termination_filename)
