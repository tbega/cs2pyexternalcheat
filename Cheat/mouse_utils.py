import ctypes
import time


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    class _INPUT_UNION(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong), ("u", _INPUT_UNION)]

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def move_mouse_relative_sendinput(dx, dy):
    extra = ctypes.c_ulong(0)
    ii_ = INPUT._INPUT_UNION()
    ii_.mi = MOUSEINPUT(int(dx), int(dy), 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    command = INPUT(INPUT_MOUSE, ii_)
    ctypes.windll.user32.SendInput(1, ctypes.byref(command), ctypes.sizeof(command))

def mouse_click_sendinput():
    extra = ctypes.c_ulong(0)
    ii_ = INPUT._INPUT_UNION()
    ii_.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra))
    command_down = INPUT(INPUT_MOUSE, ii_)
    ctypes.windll.user32.SendInput(1, ctypes.byref(command_down), ctypes.sizeof(command_down))
    time.sleep(0.01)
    ii_.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra))
    command_up = INPUT(INPUT_MOUSE, ii_)
    ctypes.windll.user32.SendInput(1, ctypes.byref(command_up), ctypes.sizeof(command_up))
