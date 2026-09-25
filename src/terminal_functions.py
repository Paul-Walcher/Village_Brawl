"""
Various Terminal functions
"""

from ascii_magic import AsciiArt
import ascii_magic

import ctypes
import time
import os
import shutil
import re
import time
import subprocess


from wcwidth import wcswidth, center
import pyfiglet
import pyautogui
import global_context
import keyboard
import constants


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

VK_L = 0x4C

BUFFER_TIME = 0.01
FIRST_PRINTED_LINE = None

TERMINAL_ID = 1

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

def wait_for_key(key):
    #waiting function
    while 1:
        if keyboard.is_pressed(key):
            break

def clear_keyboard_buffer():
    handle = kernel32.GetStdHandle(-10)  # STD_INPUT_HANDLE
    kernel32.FlushConsoleInputBuffer(handle)

def split_horizontally(context, script, args=None):
    """
    Will be executed from this folders parentfolder
    """
    global TERMINAL_ID

    if args is None:
        args = []
    stop_script_file = str(TERMINAL_ID) + ".txt"
    stop_script = os.path.join("terminal_subfiles", stop_script_file)

    subprocess.Popen([
        "wt",
        "-w", "0",
        "split-pane",
        "-V",
        "-d", constants.SCRIPT_DIR(),
        "python",
        script,
        stop_script,
        *args
    ])

    context.terminal_handles[TERMINAL_ID] = stop_script
    handle = TERMINAL_ID
    TERMINAL_ID += 1

    return handle

def close(context, handle):

    stop_script = context.terminal_handles[handle]

    with open(stop_script, "w"):
        pass

    del context.terminal_handles[handle]

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



def image_to_ascii_from_context(path, columns, context):
    return image_to_ascii(path, columns,
                            full_color=context.settings.full_color, monochrome=context.settings.monochrome_assets)




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

def press_key(vk):
    user32.keybd_event(vk, 0, 0, 0)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)

def zoom_in_no_context(n, buffer_time=BUFFER_TIME):
    for i in range(n):
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        press_key(VK_ADD)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(buffer_time)

def zoom_out_no_context(n, buffer_time=BUFFER_TIME):
    for i in range(n):
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        press_key(VK_SUBTRACT)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(buffer_time)

def reset_zoom_no_context():
    keyboard.press_and_release("ctrl+0")
    context.current_zoom = 0
    time.sleep(0.1)



def zoom_in(context, n, buffer_time=BUFFER_TIME):
    for i in range(n):
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        press_key(VK_ADD)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(buffer_time)

    context.current_zoom += n

def zoom_to_no_context(prev_zoom, zoom, buffer_t=0.01):

    diff = zoom - prev_zoom

    if (diff > 0):
        zoom_in_no_context(diff, buffer_time=buffer_t)
    if (diff < 0):
        zoom_out_no_context(abs(diff), buffer_time=buffer_t)


def zoom_out(context, n, buffer_time=BUFFER_TIME):
    for i in range(n):
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        press_key(VK_SUBTRACT)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(buffer_time)

    context.current_zoom -= n


def reset_zoom(context):
    keyboard.press_and_release("ctrl+0")
    context.current_zoom = 0
    time.sleep(0.1)

def zoom_to(context, zoom, buffer_t=0.01):

    diff = zoom - context.current_zoom

    if (diff > 0):
        zoom_in(context, diff, buffer_time=buffer_t)
    if (diff < 0):
        zoom_out(context, abs(diff), buffer_time=buffer_t)


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


def reset_scroll():

    scroll = get_scroll_position()
    scroll_up(scroll)

def visible_length(text):
    text = ANSI_ESCAPE.sub("", text)
    return max(0, wcswidth(text))

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

"""
ascii fonts
"""
