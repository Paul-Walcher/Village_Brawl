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
    data_transmission_filename = sys.argv[2]

    transmitted_data = []

    while 1:

        data = []

        if termination_filename in os.listdir(constants.SPLIT_TERMINAL_FILEPATH):
            break

        try:

            with open(data_transmission_filename, "r") as f:
                data = f.read().splitlines()
            with open(data_transmission_filename, "w"):
                pass

        except:
            pass

        if data:
            print(data[0])


    removed = False
    while not removed:
        try:
            os.remove(termination_filename)
            removed = True

        except:
            pass
    removed = False

    while not removed:
        try:
            os.remove(data_transmission_filename)
            removed = True

        except:
            pass
