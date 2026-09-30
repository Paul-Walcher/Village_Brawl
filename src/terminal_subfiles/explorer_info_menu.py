import sys
from pathlib import Path

#adding path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import terminal_functions as terminal
import constants
import time
import os


if __name__ == "__main__":

    #first comes the exit signal
    termination_filename = sys.argv[1]



    #now checking if the file exists:
    while 1:

        if termination_filename in os.listdir(constants.SPLIT_TERMINAL_FILEPATH):
            break

    removed = False

    while not removed:
        try:
            os.remove(termination_filename)
            removed = True

        except:
            pass
