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


user32 = ctypes.windll.user32

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

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def image_to_ascii(path, columns, width_ratio=2.2, full_color=False):
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

    return "\n".join(lines)

def press_key(vk):
    user32.keybd_event(vk, 0, 0, 0)
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)


def zoom_in(n):
    for i in range(n):
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        press_key(VK_ADD)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)


def zoom_out(n):
    for i in range(n):
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        press_key(VK_SUBTRACT)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

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




def visible_length(text):
    """Return the number of visible terminal characters."""
    return len(ANSI_ESCAPE.sub('', text))


def print_centered(text, full=False):
    terminal_width = shutil.get_terminal_size().columns

    lines = text.splitlines()

    # Find the visible width of the widest line
    max_width = max(
        (visible_length(line) for line in lines),
        default=0
    )

    # Center the whole block
    left_padding = max(
        0,
        (terminal_width - max_width) // 2
    )

    for line in lines:
        line_width = visible_length(line)

        # Keep all lines aligned with the widest line
        right_padding = max_width - line_width

        output = (
            " " * left_padding
            + line
            + " " * right_padding
        )

        # Fill the remainder of the terminal if requested
        if full:
            output += " " * max(
                0,
                terminal_width - left_padding - max_width
            )

        print(output)

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
