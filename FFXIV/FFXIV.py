import win32con
import win32gui
import win32process

class FFXIV:

    def __init__(self):
        self.pid = self.find_pid()
        self.device_context = win32gui.GetWindowDC(self.pid)

    @staticmethod
    def find_pid():
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if "FINAL FANTASY XIV" == win32gui.GetWindowText(hwnd):
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        if(hwnds.__len__() > 0):
            return hwnds[0]
        else:
            raise IndexError("FFXIV window not found")


    def get_pixel(self,x, y):
        long_color = win32gui.GetPixel(self.device_context, x, y)
        i_color = int(long_color)
        return (i_color & 0xff), ((i_color >> 8) & 0xff), ((i_color >> 16) & 0xff)

if __name__ == '__main__':

    ff = FFXIV()
    ff_handle = ff.find_pid()

    print ff_handle, "=>", win32gui.GetWindowText(ff_handle)
    diff_pixels = []
    for i in range(1320,1500):
        p300 = ff.get_pixel(i,230)
        p301 = ff.get_pixel(i,231)
        if p300 != p301:
            diff_pixels.append(i)
            t300 = "(%d, %d, %d)" % (p300[0], p300[1], p300[2])
            t301 = "(%d, %d, %d)" % (p301[0], p301[1], p301[2])
            print "%s\t%s\t%d" % (t300,t301,diff_pixels.__len__())

    print "There were %d differeing pixels" % diff_pixels.__len__()



