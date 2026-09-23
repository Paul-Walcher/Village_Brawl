"""
Various Terminal functions
"""

from ascii_magic import AsciiArt

import ctypes
import time
import os


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


def image_to_ascii(path, columns, width_ratio=2.2):
    art = AsciiArt.from_image(path)

    ascii_text = art.to_ascii(
        columns=columns,
        width_ratio=width_ratio
    )

    return ascii_text

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

def clear():
    os.system("cls")
