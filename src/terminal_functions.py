"""
Various Terminal functions
"""

from ascii_magic import AsciiArt
import ascii_magic

import ctypes
from ctypes import wintypes
import time
import os
import shutil
import re
import time
import subprocess
import sys
import colorsys
import msvcrt
import numpy as np

from wcwidth import wcswidth, wcwidth, center
import pyfiglet
import pyautogui
import cv2

import threading
import global_context
import keyboard
import constants
from logic import Stack
from states import SplitscreenState

import multiprocessing
import queue



user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32



VK_CONTROL = 0x11
VK_ADD = 0x6B
VK_SUBTRACT = 0x6D

KEYEVENTF_KEYUP = 0x0002
VK_CONTROL = 0x11
VK_SHIFT = 0x10
VK_UP = 0x26
VK_DOWN = 0x28
VK_PRIOR = 0x21      # Page Up
VK_NEXT = 0x22       # Page Down
VK_0 = 0x30
VK_ADD = 0x6B
VK_SUBTRACT = 0x6D

VK_L = 0x4C

BUFFER_TIME = 0.01
FIRST_PRINTED_LINE = None

TERMINAL_ID = 1
HANDLES = {}

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

text_rgb_string = lambda r, g, b: f"\033[38;2;{r};{g};{b}m"
background_rgb_string = lambda r, g, b: f"\033[48;2;{r};{g};{b}m"
color_reset_string = lambda: "\033[0m"

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

class COORD(ctypes.Structure):
    _fields_ = [
        ("X", ctypes.c_short),
        ("Y", ctypes.c_short),
    ]


class SMALL_RECT(ctypes.Structure):
    _fields_ = [
        ("Left", ctypes.c_short),
        ("Top", ctypes.c_short),
        ("Right", ctypes.c_short),
        ("Bottom", ctypes.c_short),
    ]


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD),
    ]




class ExitSignal:

    def __init__(self):
        exit = False

class KeyCallback:

    def __init__(self):

        #entries of form: key: [is_pressed, callback_function]
        self.keys_callback = {}

    def register_key(self, key, callback):

        self.keys_callback[key] = [keyboard.is_pressed(key), callback]

    def unregister_key(self, key):

        if key in self.keys_callback:
            del self.keys_callback[key]

    def change_callback(self, key, callback):

        if key in self.keys_callback:
            self.keys_callback[key][1] = callback

    def check_presses(self, args):

        for key in self.keys_callback:
            if keyboard.is_pressed(key) and not self.keys_callback[key][0]:
                self.keys_callback[key][0] = True
                self.keys_callback[key][1](key, args)

            elif not keyboard.is_pressed(key) and self.keys_callback[key][0]:
                self.keys_callback[key][0] = False

def prepare_for_fullscreen(image, scale=1.0, background_color=(0, 0, 0),
                                    fixed=None):


    user32 = ctypes.windll.user32

    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    h, w = image.shape[:2]

    new_width = int(w * scale)
    new_height = int(h * scale)

    if fixed is not None:

        new_width = fixed[0]
        new_height = fixed[1]

    image = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_NEAREST
    )

    # Fullscreen canvas
    canvas = np.full(
        (screen_height, screen_width, 3),
        background_color,
        dtype=np.uint8
    )

    # Center image
    x = (screen_width - new_width) // 2
    y = (screen_height - new_height) // 2

    canvas[y:y + new_height, x:x + new_width] = image

    return canvas

def show_real_image(path, scale=1.0, background_color=(0, 0, 0), fixed=(1024, 1024)):
    name = constants.CV2_WINDOW_NAME

    user32 = ctypes.windll.user32

    # Remember whatever window currently has focus
    original_hwnd = user32.GetForegroundWindow()

    image = cv2.imread(path)

    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")

    image = prepare_for_fullscreen(image, scale=scale, background_color=background_color, fixed=fixed)

    cv2.namedWindow(name, cv2.WINDOW_NORMAL)

    cv2.setWindowProperty(
        name,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )

    cv2.imshow(name, image)

    # Let OpenCV actually create/render the native window
    cv2.waitKey(1)

    # Find the OpenCV window
    cv2_hwnd = user32.FindWindowW(None, name)

    if cv2_hwnd:
        # Make sure it is shown and bring it to the foreground
        user32.ShowWindow(cv2_hwnd, 5)  # SW_SHOW
        user32.SetForegroundWindow(cv2_hwnd)

    # Wait for a key
    cv2.waitKey(0)

    # Close OpenCV window
    try:
        cv2.destroyWindow(name)
        cv2.waitKey(1)
    except cv2.error:
        pass

    # Return focus to the original window
    if original_hwnd:
        user32.ShowWindow(original_hwnd, 5)  # SW_SHOW
        user32.SetForegroundWindow(original_hwnd)

    time.sleep(0.4)


def wait_for_key(key):
    #waiting function
    while 1:
        if keyboard.is_pressed(key):
            break

def clear_keyboard_buffer():
    handle = kernel32.GetStdHandle(-10)  # STD_INPUT_HANDLE
    kernel32.FlushConsoleInputBuffer(handle)

def clear_terminal_subfolder():

    folder = constants.SPLIT_TERMINAL_FILEPATH
    files = os.listdir(folder)

    for file in files:

        if file.endswith(".txt"):
            os.remove(os.path.join(constants.SPLIT_TERMINAL_FILEPATH, file))

def split_horizontally(script, args=None):
    """
    Will be executed from this folders parentfolder
    """
    global TERMINAL_ID
    global HANDLES

    if args is None:
        args = []
    stop_script_file = str(TERMINAL_ID) + ".txt"
    stop_script = stop_script_file
    data_transmission_file = str(TERMINAL_ID) + "data.txt"

    with open(os.path.join(constants.SPLIT_TERMINAL_FILEPATH, data_transmission_file), "w") as f:
        pass

    subprocess.Popen([
        "wt",
        "-w", "0",
        "split-pane",
        "-V",
        "-d", constants.SPLIT_TERMINAL_FILEPATH,
        "python",
        script,
        stop_script,
        data_transmission_file,
        *args
    ])

    HANDLES[TERMINAL_ID] = [
                    os.path.join(constants.SPLIT_TERMINAL_FILEPATH, stop_script),
                    os.path.join(constants.SPLIT_TERMINAL_FILEPATH, data_transmission_file)
                    ]

    handle = TERMINAL_ID
    TERMINAL_ID += 1

    return handle

def send_over(handle, text):

    global HANDLES

    ref = HANDLES[handle]
    stop_script = ref[0]
    data_transmission_file = ref[1]

    opened = False

    while not opened:
        try:
            with open(data_transmission_file, "a") as f:
                f.write(text)
                f.write("\n")
            opened = True
        except:
            pass

def close(handle):

    global HANDLES

    ref = HANDLES[handle]
    stop_script = ref[0]
    data_transmission_file = ref[1]
    opened = False

    while not opened:
        try:
            with open(stop_script, "w"):
                pass
            opened = True
        except:
            pass
#
    del HANDLES[handle]

def focus_prev(context):
    subprocess.run([
        "wt",
        "-w", "0",
        "move-focus",
        "previousInOrder"
        ])

def focus_next(context):
    subprocess.run([
        "wt",
        "-w", "0",
        "move-focus",
        "nextInOrder"
    ])


def disable_scrollback():
    """Enter the alternate screen buffer, which has no scrollback."""
    sys.stdout.write("\x1b[?1049h")
    sys.stdout.flush()


def enable_scrollback():
    """Leave the alternate screen buffer and return to the normal terminal."""
    sys.stdout.write("\x1b[?1049l")
    sys.stdout.flush()

class ScrollEnable:

    def __init__(self):
        pass

    def __enter__(self):
        enable_scrollback()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        disable_scrollback()
        return False

def image_to_ascii(path, columns, width_ratio=2.2, full_color=False, monochrome=False):
    art = ascii_magic.from_image(path)

    characters = art.to_character_list(
        columns=columns,
        width_ratio=width_ratio,
        full_color=full_color
    )

    lines = []

    for row in characters:
        line = ""

        for item in row:
            char = item["character"]

            if full_color:
                hex_color = item["full-hex-color"]

                r = int(hex_color[1:3], 16)
                g = int(hex_color[3:5], 16)
                b = int(hex_color[5:7], 16)

                line += f"\033[38;2;{r};{g};{b}m{char}"
            else:
                line += item["terminal-color"] + char

        line += "\033[0m"
        lines.append(line)

    text = "\n".join(lines)
    if monochrome:
        text = ANSI_ESCAPE.sub('', text)
    return text

def image_to_background_ascii(
    path,
    columns,
    width_ratio=1.8,
    saturation=1.8,
    contrast=1.6,
    brightness=0.9,
    black_threshold=10,
):
    art = ascii_magic.from_image(path)

    characters = art.to_character_list(
        columns=columns,
        width_ratio=width_ratio,
        full_color=True
    )

    lines = []

    for row in characters:
        line = ""

        for item in row:

            if item["character"] == " ":
                line += "\033[49m "
                continue

            hex_color = item["full-hex-color"]

            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)

            # Very dark pixels become the terminal background color
            if max(r, g, b) < black_threshold:
                r = g = b = 12
            else:
                # RGB -> HSV
                h, s, v = colorsys.rgb_to_hsv(
                    r / 255,
                    g / 255,
                    b / 255
                )

                # Make colors more vivid
                s = min(1.0, s * saturation)

                # Brighten using gamma correction
                # brightness < 1.0 = brighter
                v = v ** brightness

                # Increase contrast around the middle brightness
                v = (v - 0.5) * contrast + 0.5
                v = max(0.0, min(1.0, v))

                # HSV -> RGB
                r, g, b = colorsys.hsv_to_rgb(h, s, v)

                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)

            line += f"\033[48;2;{r};{g};{b}m "

        # Restore terminal background
        line += "\033[49m "
        lines.append(line)

    return "\033[49m " + "\n".join(lines) + "\033[0m"

def image_to_ascii_from_context(path, columns, context, width_ratio=2.2):

    if context.settings.ascii_art:
        return image_to_ascii(path, columns,
                                full_color=context.settings.full_color, monochrome=context.settings.monochrome_assets,
                                width_ratio=width_ratio)

    else:
        return image_to_background_ascii(path, columns, width_ratio)


def render_text(font, text):

    figlet = pyfiglet.Figlet()
    figlet.setFont(font=font)
    return figlet.renderText(text)

def toggle_terminal_size():
    pyautogui.press("f11")

def terminal_is_maximized():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()

    # Normal Windows maximize
    if user32.IsZoomed(hwnd):
        return True

    # F11 fullscreen
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))

    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    return (
        rect.left == 0 and
        rect.top == 0 and
        rect.right == screen_width and
        rect.bottom == screen_height
    )

def wait_for_terminal_change(old_dimensions, timeout=0.5, poll_interval=0.01):
    deadline = time.perf_counter() + timeout

    while time.perf_counter() < deadline:
        new_dimensions = terminal_dimensions()

        if new_dimensions != old_dimensions:
            return new_dimensions

        time.sleep(poll_interval)

    return terminal_dimensions()

def press_key(vk):
    user32.keybd_event(vk, 0, 0, 0)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)

def press_ctrl_key(vk, delay=0.05):
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    press_key(vk)
    user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

    time.sleep(delay)

def press_zoom_key(key, hold_time=0.02, after_time=0.15):
    keyboard.press("ctrl")
    time.sleep(hold_time)

    keyboard.press(key)
    time.sleep(hold_time)

    keyboard.release(key)
    time.sleep(hold_time)

    keyboard.release("ctrl")
    time.sleep(after_time)

def zoom_in_no_context(n, buffer_time=0.15):
    for _ in range(n):
        press_zoom_key("+", after_time=buffer_time)

def zoom_out_no_context(n, buffer_time=0.15):
    for _ in range(n):
        press_zoom_key("-", after_time=buffer_time)

def reset_zoom_no_context(buffer_time=0.5):
    keyboard.press_and_release("ctrl+0")
    time.sleep(buffer_time)


def zoom_to_no_context(prev_zoom, zoom, buffer_t=0.05):

    zoom = zoom - prev_zoom

    if zoom > 0:
        zoom_in(context, zoom, buffer_time)

    elif zoom < 0:
        zoom_out(context, -zoom, buffer_time)


def zoom_in(context, n, buffer_time=0.15):
    for _ in range(n):
        press_zoom_key("+", after_time=buffer_time)

    context.current_zoom += n


def zoom_out(context, n, buffer_time=0.15):
    for _ in range(n):
        press_zoom_key("-", after_time=buffer_time)

    context.current_zoom -= n

def reset_zoom(context, buffer_time=0.5):
    keyboard.press_and_release("ctrl+0")
    time.sleep(buffer_time)

    context.current_zoom = 0


def zoom_to(context, zoom, buffer_time=0.05):

    #reset_zoom(context)

    zoom = zoom - context.current_zoom

    if zoom > 0:
        zoom_in(context, zoom, buffer_time)

    elif zoom < 0:
        zoom_out(context, -zoom, buffer_time)

def key_down(vk):
    user32.keybd_event(vk, 0, 0, 0)


def key_up(vk):
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)


def press(vk):
    key_down(vk)
    key_up(vk)



def scroll_up(n):
    for i in range(n):
        key_down(VK_CONTROL)
        key_down(VK_SHIFT)
        press(VK_UP)
        key_up(VK_SHIFT)
        key_up(VK_CONTROL)



def scroll_down(n):
    for i in range(n):
        key_down(VK_CONTROL)
        key_down(VK_SHIFT)
        press(VK_DOWN)
        key_up(VK_SHIFT)
        key_up(VK_CONTROL)


def scroll_page_up(n):
    for i in range(n):
        key_down(VK_CONTROL)
        key_down(VK_SHIFT)
        press(VK_PRIOR)
        key_up(VK_SHIFT)
        key_up(VK_CONTROL)


def scroll_page_down(n):
    for i in range(n):
        key_down(VK_CONTROL)
        key_down(VK_SHIFT)
        press(VK_NEXT)
        key_up(VK_SHIFT)
        key_up(VK_CONTROL)

def scroll(n):

    if (n < 0):
        scroll_up(abs(n))
    else:
        scroll_down(n)


def visible_length(text):
    text = ANSI_ESCAPE.sub("", text)
    return max(0, wcswidth(text))


def redraw(text):
    sys.stdout.write(
        "\x1b[2J\x1b[H"  # clear screen + move cursor home
        + text
    )
    sys.stdout.flush()

def print_centered(text, full=False, shift=0, text_color=None, background_color=None,
                    prev_text_color=None, prev_background_color=None
                    ):
    time.sleep(BUFFER_TIME)
    terminal_width = shutil.get_terminal_size().columns

    lines = text.splitlines()

    if not lines:
        return

    # Width of the widest visible line
    max_width = max(visible_length(line) for line in lines)

    # Position of the whole block
    block_left = (terminal_width - max_width) // 2 + shift
    block_left = max(0, block_left)

    leading_string = ""

    if text_color:
        leading_string += text_rgb_string(*text_color)
    if background_color:
        leading_string += background_rgb_string(*background_color)

    reset_string = ""

    if prev_text_color:
        reset_string += text_rgb_string(*prev_text_color)
    if prev_background_color:
        reset_string += background_rgb_string(*prev_background_color)

    if not reset_string:
        reset_string = color_reset_string()

    for line in lines:
        line_width = visible_length(line)

        # Center this line inside the block
        line_offset = (max_width - line_width) // 2

        output = (
            " " * (block_left + line_offset)
            + leading_string + line + reset_string
        )

        if full:
            output += " " * max(
                0,
                terminal_width - block_left - line_offset - line_width
            )

        print(output)

def print_figlet(text, font, width=200, centered = True):
    """
    Prints text with figlet fonts
    """
    f = pyfiglet.Figlet(font=font, width=width)

    time.sleep(BUFFER_TIME)
    if centered:
        print(*[x.center(shutil.get_terminal_size().columns) for x in f.renderText(text).split("\n")],sep="\n")
    else:
        print(f.renderText(text))

def text_rgb(r, g, b):
    """Set the text color to RGB."""
    print(f"\033[38;2;{r};{g};{b}m", end="")


def background_rgb(r, g, b):
    """Set the background color to RGB."""
    print(f"\033[48;2;{r};{g};{b}m", end="")


def color_reset():
    """Reset all text formatting and colors to the terminal defaults."""
    print("\033[0m", end="")

def clear():
    os.system("cls")

def hide_cursor(context):
    print("\033[?25l", end="")
    context.cursor_visible = False


def show_cursor(context):
    print("\033[?25h", end="")
    context.cursor_visible = True



def terminal_dimensions():
    handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE

    info = CONSOLE_SCREEN_BUFFER_INFO()

    if not kernel32.GetConsoleScreenBufferInfo(handle, ctypes.byref(info)):
        return None, None

    columns = info.srWindow.Right - info.srWindow.Left + 1
    rows = info.srWindow.Bottom - info.srWindow.Top + 1

    return columns, rows

def visible_width(text):
    """
    Return the number of terminal columns occupied by `text`.

    ANSI escape sequences are ignored.
    """
    text = ANSI_ESCAPE.sub("", text)

    width = wcswidth(text)

    if width < 0:
        width = 0

    return width


def _split_into_units(text):
    """
    Split a line into ANSI sequences, words, and whitespace.

    ANSI sequences are kept as separate zero-width units.
    """
    tokens = re.split(f"({ANSI_ESCAPE.pattern})", text)

    units = []
    current = []
    current_type = None

    for token in tokens:
        if not token:
            continue

        # ANSI sequence
        if ANSI_ESCAPE.fullmatch(token):
            current.append(token)
            continue

        for char in token:
            if char == "\t":
                char = " " * 8

            if char.isspace():
                char_type = "space"
            else:
                char_type = "word"

            if current_type is None:
                current_type = char_type

            elif char_type != current_type:
                units.append("".join(current))
                current = []
                current_type = char_type

            current.append(char)

    if current:
        units.append("".join(current))

    return units


def wrap_text(text, columns):
    """
    Wrap text to `columns` terminal cells using word wrapping.

    If a word does not fit on the current line, the entire word
    is moved to the next line.

    If a single word is longer than `columns`, that word is split.

    Existing newline characters are preserved.

    ANSI escape sequences do not consume terminal columns.
    """
    if columns <= 0:
        return text

    result = []

    for original_line in text.split("\n"):

        units = _split_into_units(original_line)

        current = []
        width = 0

        i = 0

        while i < len(units):
            unit = units[i]

            # ANSI-only unit.
            # Just preserve it.
            if visible_width(unit) == 0 and not unit.strip():
                current.append(unit)
                i += 1
                continue

            unit_width = visible_width(unit)

            # Whitespace
            if unit.isspace():

                # Don't put whitespace at the beginning of a new line.
                if width == 0:
                    i += 1
                    continue

                # Add whitespace only if it fits.
                if width + unit_width <= columns:
                    current.append(unit)
                    width += unit_width

                else:
                    result.append("".join(current))
                    current = []
                    width = 0

                i += 1
                continue

            # Word fits on the current line.
            if width + unit_width <= columns:
                current.append(unit)
                width += unit_width
                i += 1
                continue

            # Word does not fit.
            # Move the whole word to the next line.
            if width > 0:
                result.append("".join(current))
                current = []
                width = 0

                # Don't consume the word yet.
                continue

            # The word itself is longer than the entire line.
            # Split it character-by-character.
            tokens = re.split(
                f"({ANSI_ESCAPE.pattern})",
                unit
            )

            for token in tokens:
                if not token:
                    continue

                # ANSI sequence
                if ANSI_ESCAPE.fullmatch(token):
                    current.append(token)
                    continue

                for char in token:
                    char_width = wcwidth(char)

                    if char_width < 0:
                        char_width = 0

                    if (
                        char_width > 0
                        and width + char_width > columns
                    ):
                        result.append("".join(current))
                        current = []
                        width = 0

                    current.append(char)
                    width += char_width

            i += 1

        result.append("".join(current))

    return "\n".join(result)


def center_terminal_line(line, columns):
    """
    Center a single already-wrapped line within `columns`.
    """
    width = visible_width(line)

    if width >= columns:
        return line

    padding = (columns - width) // 2

    return (" " * padding) + line


def paginate_text(context, texts, bottom_margin=0):
    """
    Takes a list of (text, centered) tuples and converts them
    into terminal-sized pages.

    Each tuple is:

        (text, centered)

    centered=True centers every resulting visual line.

    Returns:
        list[str]
    """
    columns, rows = terminal_dimensions()

    columns = max(1, columns)
    rows = max(1, rows)

    if context.splitscreen_state == SplitscreenState.SPLIT_HORIZONTALLY:

        columns = columns // 2 - 2

    if (bottom_margin > 0 and bottom_margin < rows):
        rows -= bottom_margin

    all_lines = []

    for text, centered in texts:

        wrapped = wrap_text(text, columns)

        for line in wrapped.split("\n"):

            if centered:
                line = center_terminal_line(
                    line,
                    columns
                )

            all_lines.append(line)

    pages = []

    for start in range(0, len(all_lines), rows):
        page_lines = all_lines[start:start + rows]
        pages.append("\n".join(page_lines))

    if not pages:
        pages.append("")

    return pages
"""
ascii fonts
"""
