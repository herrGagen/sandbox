import Tkinter
import ctypes
from ctypes import wintypes
import win32con

user32 = ctypes.windll.user32
byref = ctypes.byref

def hotkey_handler(root):
    msg = wintypes.MSG()
    if user32.GetMessageA(byref(msg), None, 0, 0) != 0:
        if msg.message == win32con.WM_HOTKEY:
            if msg.wParam == 1:
                print("hotkey pressed")
    user32.TranslateMessage(byref(msg))
    user32.DispatchMessageA(byref(msg))
    root.after(1, hotkey_handler, root)

if __name__=="__main__":
    root = Tkinter.Tk()

    if user32.RegisterHotKey(None, 1, win32con.MOD_CONTROL, win32con.VK_F1) != 0:
        print("--Hotkey registered!")

    root.after(1, hotkey_handler, root)

    root.mainloop()