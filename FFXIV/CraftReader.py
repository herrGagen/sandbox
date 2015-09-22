from FFXIV import FFXIV
from OnTopTextBox import OnTopTextBox
from enum import Enum


class Condition(Enum):
    Normal = 1
    Good = 2
    Excellent = 3
    Poor = 4
    READ_ERROR = 5


class CraftReader:

    ff = FFXIV()

    THRESH = 500
    """ Threshold for pixel sums being white"""

    text_y = 291

    norm_pix = (88, 104, 108, 136)
    good_pix = (94, 101, 120, 129)
    exel_pix = (82, 90, 128, 141)
    poor_pix = (102, 107, 112, 121)

    def __init__(self):
        self.blank_color = (40, 39, 40)
        self.prog_y = 222
        self.qual_y = 262
        self.left = 184
        self.right = 414
        self.open_left = 280
        self.open_right = 318
        self.open_y = 208

    @property
    def is_crafting(self):
        """Is the character currently crafting?"""
        ff = CraftReader.ff
        y = self.open_y
        for x in range(self.open_left, self.open_right, 5):
            sm = sum(ff.get_pixel(x, y))
            if sm > 180 or sm < 155:
                return False
        return True

    @property
    def condition(self):
        """Returns Condition enum"""
        if self._check_pix(CraftReader.norm_pix):
            return Condition.Normal
        if self._check_pix(CraftReader.good_pix):
            return Condition.Good
        if self._check_pix(CraftReader.exel_pix):
            return Condition.Excellent
        if self._check_pix(CraftReader.poor_pix):
            return Condition.Poor
        return Condition.READ_ERROR

    @staticmethod
    def _check_pix(pix):
        THRESH = CraftReader.THRESH
        ff = CraftReader.ff
        y = CraftReader.text_y
        count = 0
        for x in pix:
            if sum(ff.get_pixel(x, y)) >= THRESH:
                count += 1
        if count == 4:
            return True
        return False

    @property
    def progress(self):
        """Pixel scan bars to figure out how much progress / quality we have made
        :return: (progress fraction, quality fraction)
        """
        ff = CraftReader.ff
        prog_r = -1
        qual_r = -1
        STEP = 5
        for x in range(self.left+STEP, self.right, STEP):
            if prog_r == -1:
                ppix = ff.get_pixel(x, self.prog_y)
                if ppix == self.blank_color:
                    prog_r = x - STEP
            if qual_r == -1:
                qpix = ff.get_pixel(x, self.qual_y)
                if qpix == self.blank_color:
                    qual_r = x - STEP

        width = float(self.right - self.left)
        prog_frac = (prog_r - self.left) / width if prog_r > 0 else 1
        qual_frac = (qual_r - self.left) / width if qual_r > 0 else 1
        return (prog_frac, qual_frac)


