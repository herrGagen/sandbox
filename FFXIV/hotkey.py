import win32con
import ctypes
from ctypes import wintypes


class HotkeyHandler:

    def __init__(self, HOTKEYS, HOTKEY_ACTIONS):
        user32 = ctypes.windll.user32
        byref = ctypes.byref

        for id, (vk, modifiers) in HOTKEYS.items ():
          print("Registering id", id, "for key", vk)
          if not user32.RegisterHotKey (None, id, modifiers, vk):
            print("Unable to register id %d" % id)

        #
        # Home-grown Windows message loop: does
        #  just enough to handle the WM_HOTKEY
        #  messages and pass everything else along.
        #
        try:
          msg = wintypes.MSG ()
          while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
            if msg.message == win32con.WM_HOTKEY:
              action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
              if action_to_take:
                action_to_take ()

            user32.TranslateMessage (byref (msg))
            user32.DispatchMessageA (byref (msg))

        finally:
          for id in HOTKEYS.keys ():
            user32.UnregisterHotKey (None, id)