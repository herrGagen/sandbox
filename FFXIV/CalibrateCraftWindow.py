import OnTopTextBox
import win32con
import sys
from CraftReader import CraftReader
from FFXIV import FFXIV

__author__ = 'johngalt'

class Pix:
    def __init__(self):
        self._npix = []
        self._gpix = []
        self._epix = []
        self._ppix = []

    @property
    def npix(self):
        """Pixels above threshold when condition is normal"""
        return self._npix

    @npix.setter
    def npix(self, pix):
        self._npix = pix

    @property
    def gpix(self):
        """Pixels above threshold when condition is good"""
        return self._gpix

    @gpix.setter
    def gpix(self, pix):
        self._gpix = pix

    @property
    def epix(self):
        """Pixels above threshold when condition is excellent"""
        return self._epix

    @epix.setter
    def epix(self, pix):
        self._epix = pix

    @property
    def ppix(self):
        """Pixels above threshold when condition is poor"""
        return self._ppix

    @ppix.setter
    def ppix(self,pix):
        self._ppix = pix

    @property
    def valid(self):
        """Have all 4 conditions been recorded?"""
        if (self._npix == []
                or self._gpix == []
                or self._epix == []
                or self._ppix == []) :
                return False
        return True


class CraftCalibrator:

    def __init__(self):
        """The hard coded left and right search locations should be changed"""
        self.t_height = 291
        self.t_left = 65
        self.t_right = 144
        self.points = Pix()

    def scan_text(self):
        retval = []
        for x in range(self.t_left, self.t_right):
            temp = ff.get_pixel(x, self.t_height)
            if sum(temp) > CraftReader.THRESH:
                retval.append(x)
        return retval

    def normal(self):
        self.points.npix = self.scan_text()
        print(self.points.npix)

    def good(self):
        self.points.gpix = self.scan_text()
        print(self.points.gpix)

    def excellent(self):
        self.points.epix = self.scan_text()
        print(self.points.epix)

    def poor(self):
        self.points.ppix = self.scan_text()
        print(self.points.ppix)

    def find_best(self):
        if not self.points.valid:
            print "Warning: scan all types first"
        n = set(self.points.npix)
        g = set(self.points.gpix)
        e = set(self.points.epix)
        p = set(self.points.ppix)
        best_n = n - g - e - p
        best_g = g - n - e - p
        best_e = e - n - g - p
        best_p = p - n - g - e

        print(n)
        print(self.points.npix)
        print("Best n: %s" % (best_n,))
        print("Best g: %s" % (best_g,))
        print("Best e: %s" % (best_e,))
        print("Best p: %s" % (best_p,))
        print(best_n.union(best_g).union(best_e).union(best_p))

HOTKEYS = {
    1: (win32con.VK_F1, None),
    2: (win32con.VK_F4, None),
    3: (win32con.VK_F5, None),
    4: (win32con.VK_F6, None),
    5: (win32con.VK_F7, None),
    6: (win32con.VK_F8, None),
    7: (win32con.VK_F9, None)
}

cc = CraftCalibrator()
cw = CraftReader()


def handle_f4():
    cw.exit()
    sys.exit()

HOTKEY_ACTIONS = {
    1: cw.get_progress,
    2: handle_f4,
    3: cc.normal,
    4: cc.good,
    5: cc.excellent,
    6: cc.poor,
    7: cc.find_best
}

if __name__=="__main__":
    from hotkey import HotkeyHandler as HH
    tb = OnTopTextBox.OnTopTextBox("F1 to increment counter, F4 to close")
    ff = FFXIV()
    hh = HH(HOTKEYS, HOTKEY_ACTIONS)
