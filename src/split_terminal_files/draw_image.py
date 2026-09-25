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
    #first argument is the image path
    image_path = sys.argv[2]
    #second is the resolution
    resolution = int(sys.argv[3])
    #third is full_color
    full_color = bool(int(sys.argv[4]))
    #forth is monochrome
    monochrome = bool(int(sys.argv[5]))

    #now drawing centered
    image = terminal.image_to_ascii(image_path, columns=resolution, full_color = full_color, monochrome=monochrome)
    terminal.print_centered(image)


    #now checking if the file exists:
    while 1:

        if tail in os.listdir(head):
            break

    os.remove(termination_filename)
