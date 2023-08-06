import win32api
import win32con
import win32gui

from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def mousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x,pt.y]

def hide_from_taskbar(hw):
    try:
        win32gui.ShowWindow(hw, win32con.SW_HIDE)
        win32gui.SetWindowLong(hw, win32con.GWL_EXSTYLE,win32gui.GetWindowLong(hw, win32con.GWL_EXSTYLE)| win32con.WS_EX_TOOLWINDOW);
        win32gui.ShowWindow(hw, win32con.SW_SHOW);
    except win32gui.error:
        print("Error while hiding the window")
        return None

def set_clear(hwnd, transparent_color=None, transparent=False):
    # Set window type as layered window
    if transparent:
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
    else:
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent_color), 0, win32con.LWA_COLORKEY)

def set_topmost(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

def mid_loc(hwnd, ScreenX, ScreenY):
    l,t,r,b = win32gui.GetWindowRect(hwnd)
    appX = r-l
    appY = b-t
    tarX = (ScreenX-appX+1)//2
    tarY = (ScreenY-appY+1)//2
    win32gui.MoveWindow(hwnd, tarX, tarY, appX, appY, True)

def peel(title, hide=True, clear=True, topmost=True):
    hwnd = win32gui.FindWindowEx(None, None, None, title)
    if topmost:
        set_topmost(hwnd)
    if hide:
        hide_from_taskbar(hwnd)
    if clear:
        set_clear(hwnd)

if __name__ == '__main__':
    peel('screen')
