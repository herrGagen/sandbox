from Crafter import *
from CraftReader import Condition
import math

innovation_cp = 18
strides_cp = 32
steady_hands_2_cp = 25
bbless_cp = 24
manip_cp = 88
masters_mend_cp = 92
precise_cp = 18

class MythNugg(Crafter):

    def __init__(self, cp = 339, req_synth = 1):
        Crafter.__init__(self,cp, req_synth)

    def craft(self):
        self.start_craft()
        self.use_makers_mark(2)
        for x in range(0,2):
            self.use_flawless_synth()

        synths_used = 0
        if self.req_synth == []:
            self.req_synth = self.estimate_synth_number()
            synths_used = 1

        self.try_tricks()
        self.use_comfort_zone()
        self.try_tricks()
        self.use_inner_quiet()
        while(synths_used < self.req_synth
                and self.is_crafting):
            remaining_turns = (4 - math.ceil(self.spent_dur/10)) + self.manip_turns
            if (remaining_turns > self.req_synth - synths_used
                    and self.quality < 0.95):
                self._increase_quality()
            else:
                self._make_progress()

    def _increase_quality(self):
        cond = self.condition
        if cond == Condition.Good or cond == Condition.Excellent:
            enough_dur = (self.spent_dur < 20 or self.manip_turns > 0)
            if(enough_dur == True
                    and self.steady_turns > 0
                    and self.iq_stacks < 8
                    and self.cp >= precise_cp):
                self.use_precise_touch()
            else:
                self.use_tricks()
            return

        if(self.cp > manip_cp
           and self.spent_dur > 10
           and self.manip_turns == 0):
            self.use_manipulation()
            return

        if(self.cp > steady_hands_2_cp
           and self.steady_turns == 0):
            self.use_steady_hand_2()
            return

        if self.spent_dur >= 30:
            self._restore_durability()

        if self.iq_stacks >= 8:
            self._do_last_touch()
            return

        self.use_hasty_touch()

    def _restore_durability(self):
        if(self.manip_turns > 0
                and self.spent_dur > 20
                and self.cp > innovation_cp):
            self.use_innovation()
        elif((self.cp > manip_cp and self.spent_dur < 30)
             or self.cp >= manip_cp + innovation_cp):
            self.use_manipulation()
        elif self.cp > masters_mend_cp:
            self.use_masters_mend()
        else:
            self._make_progress()

    def _do_last_touch(self):
        cp_in_1 = self.cp
        cp_in_2 = self.cp + 8*min(1,self.czone_turns)
        cp_in_3 = self.cp + 8*min(2,self.czone_turns)
        cp_in_4 = self.cp + 8*min(3,self.czone_turns)

        if self.steady_turns >= 3:
            if cp_in_3 > (bbless_cp+innovation_cp+strides_cp):
                self.use_innovation()
                self.use_great_strides()
                self.use_bblessing()
            elif cp_in_2 > (bbless_cp+strides_cp):
                self.use_great_strides()
                self.use_bblessing()
            elif cp_in_2 > (bbless_cp+innovation_cp):
                self.use_innovation()
                self.use_bblessing()
            elif cp_in_1 > bbless_cp:
                self.use_bblessing()
            else:
                self.use_hasty_touch()
            return

        if cp_in_4 > (steady_hands_2_cp + bbless_cp + innovation_cp + strides_cp):
            self.use_innovation()
            self.use_steady_hand_2()
            self.use_great_strides()
            self.use_bblessing()
        elif cp_in_3 > (steady_hands_2_cp + strides_cp + bbless_cp):
            self.use_steady_hand_2()
            self.use_great_strides()
            self.use_bblessing()
        elif cp_in_3 > (steady_hands_2_cp + innovation_cp + bbless_cp):
            self.use_steady_hand_2()
            self.use_innovation()
            self.use_bblessing()
        elif cp_in_2 > (steady_hands_2_cp + strides_cp):
            self.use_steady_hand_2()
            self.use_bblessing()
        elif cp_in_2 > (bbless_cp + innovation_cp):
            self.use_innovation()
            self.use_bblessing()
        elif cp_in_1 > bbless_cp:
            self.use_bblessing()
        else:
            self.use_hasty_touch()
        return

    def try_tricks(self):
        cond = self.condition
        if cond == Condition.Good or cond == Condition.Excellent:
            self.use_tricks()
            return True
        return False

    def _make_progress(self):
        if self.try_tricks():
            return

        if(self.cp > manip_cp
           and self.spent_dur > 10
           and self.manip_turns == 0):
            self.use_manipulation()
            return

        self.use_careful_synth_2()
        return


if __name__=="__main__":
    mn = MythNugg()
    for x in range(0,46):
        mn.craft()
        time.sleep(5)

