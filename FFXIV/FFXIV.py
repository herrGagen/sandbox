import win32con
import win32gui
import win32process

class FFXIV:

    def __init__(self):
        self.pid = self.find_pid()
        self.device_context = win32gui.GetWindowDC(self.pid)

    @staticmethod
    def find_pid(name = "FINAL FANTASY XIV"):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if name == win32gui.GetWindowText(hwnd):
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        if hwnds.__len__() > 0:
            return hwnds[0]
        else:
            raise IndexError("%s window not found" % name)

    def get_pixel(self,x, y):
        long_color = win32gui.GetPixel(self.device_context, x, y)
        i_color = int(long_color)
        return (i_color & 0xff), \
            ((i_color >> 8) & 0xff), \
            ((i_color >> 16) & 0xff)

    @staticmethod
    def _get_modifier(x):
        return {
            '^': win32con.VK_CONTROL,
            '!': win32con.VK_MENU,
            '+': win32con.VK_SHIFT
        }.get(x,[])

    def send_key(self, key, hold_secs = 0.1):
        """
        Sends letters and numbers to ff handle.

        Can modify press with:
         ^ ctrl
         ! alt
         + shift

        :param key:
        Alphanumeric key to press.  Can also be modified i.e. '^a', '!2'

        :param hold_secs:
        Seconds to hold key before releasing. Default 0.1
        """
        if key.__len__() > 1:
            mod = FFXIV._get_modifier(key[0])
            code = key[1]
        else:
            mod = []
            code = key[0]
        assert code.isalnum()

        if mod != []:
            win32api.SendMessage(ff_handle, win32con.WM_KEYDOWN, mod, 0)

        win32api.SendMessage(ff_handle, win32con.WM_KEYDOWN, ord(code), 0)
        time.sleep(hold_secs)
        win32api.SendMessage(ff_handle, win32con.WM_KEYUP, ord(code), 0)

        if mod != []:
            win32api.SendMessage(ff_handle, win32con.WM_KEYUP, mod, 0)


if __name__ == '__main__':
    import win32api
    import time
    import win32com
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")

    ff = FFXIV()
    ff_handle = ff.find_pid()
    print ff_handle, "=>", win32gui.GetWindowText(ff_handle)

    time.sleep(4)
    for x in range(1,10):
        print("Pressing 1")
        ff.send_key('1',0.2)
        time.sleep(4)
        print("Pressing Ctrl+1")
        ff.send_key('^1',0.2)
        time.sleep(4)

