import sys
from pathlib import Path

#adding path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import terminal_functions as terminal
import graphics
import constants
import time
import os


if __name__ == "__main__":

    #first comes the exit signal
    termination_filename = sys.argv[1]
    data_transmission_filename = sys.argv[2]

    transmitted_data = []

    terminal.hide_cursor_no_context()
    terminal.clear()

    while 1:

        data = []

        if termination_filename in os.listdir(constants.SPLIT_TERMINAL_FILEPATH):
            break

        try:

            with open(data_transmission_filename, "r") as f:
                data = f.read()
            with open(data_transmission_filename, "w"):
                pass

            time.sleep(0.1)

        except:
            pass

        if data:

            text = ""

            lines = data.splitlines()

            for line in lines:

                codec_res = terminal.process_codec(line)
                line_text = codec_res[0]
                func = codec_res[1]

                text += line_text + "\n"
                func()


            with graphics.NewPage():
                print(text)


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
