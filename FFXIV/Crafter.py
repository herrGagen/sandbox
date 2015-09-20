from FFXIV import *
from CraftReader import *

class Crafter:

    def __init__(self, cp = 360):
        self.max_cp = cp
        self.reader = CraftReader()
        self.next_craft()

    @staticmethod
    def keymap(x):
        return {
            "Manipulation": '1',
            "Comfort Zone": '2',
            "Steady Hands II": '3',
            "Waste Not II": '4',
            "Great Strides": '5',
            "Masters Mend": '6',
            "Masters Mend II": '7',
            "Tricks of the Trade": '8',
            "Inner Quiet": '9',
            "Careful Synth II": '^1',
            "Rapid Synth": '^2',
            "Hasty Touch": '^3',
            "Byregot Blessing": '^4'
        }.get(x,[])


    def next_craft(self):
        self.cp = self.max_cp
        self.manip_turns = 0
        self.waste_turns = 0
        self.steady_turns = 0
        self.inno_turns = 0
        self.stride_turns = 0
        self.iq_stacks = -1
        self.czone_turns = 0
        self.spent_dur = 0.0
        self.progress, self.quality = self.reader.progress



    def _advance_turn(self):
        if self.manip_turns > 0:
            self.manip_turns -= 1
            self.mend(1)

        if self.czone_turns > 0:
            self.czone_turns -= 1
            self._inc_cp(8)

        if self.waste_turns > 0:
            self.waste_turns -= 1

        if self.steady_turns > 0:
            self.steady_turns -= 1

        if self.stride_turns > 0:
            self.stride_turns -= 1

        if self.inno_turns > 0:
            self.inno_turns -= 1

    def _mend(self, amount):
        self.spent_dur -= amount
        if self.spent_dur < 0:
            self.spent_dur = 0

    def _inc_cp(self, amt):
        self.cp += amt
        if self.cp > self.max_cp:
            self.cp = self.max_cp

    def use_manipulation(self):
        if self.cp >= 88:
            self._advance_turn()
            self.manip_turns = 3
            self.cp -= 88

    def use_great_strides(self):
        if self.cp >= 32:
            self._advance_turn()
            self.stride_turns = 3
            self.cp -= 32

    def use_masters_mend(self):
        if self.cp >= 92:
            self.advance_turn()
            self.mend(3)
            self.cp -= 92

    def use_masters_mend_2(self):
        if self.cp >= 160:
            self.advance_turn()
            self.mend(6)
            self.cp -= 160

    def use_steady_hand_2(self):
        if self.cp > 25:
            self.advance_turn()
            self.steady_turns = 3;
            self.cp -= 25

    def use_tricks(self):
        if( self.reader.condition == Condition.Good
            or self.reader.condition == Condition.Excellent):
            self._advance_turn()
            self._inc_cp(20)

    def use_inner_quiet(self):
        if self.cp > 18:
            self._advance_turn()
            self.cp -= 18
            self.iq_stacks = 0

    def _update_pq(self):
        self.progress, self.quality = self.reader.progress

    def _use_durability(self):
        cost = 1
        if self.waste_turns > 0:
            cost = 0.5
        self.spent_dur += cost
        self._advance_turn()
        self._update_pq

    def _use_touch(self, inc = 1):
        old_qual = self.quality
        self._use_durability()
        if self.quality > old_qual and self.iq_stacks >=0:
            self.iq_stacks += inc

    def use_careful_synth_2(self):
        """100% chance of 120% progress"""
        self._use_durability()

    def use_rapid_synth(self):
        """ 50% chance of 250% progress """
        self._use_durability()

    def use_hasty_touch(self):
        """ 50% chance of 100% quality"""
        self._use_touch()

    def use_bblessing(self):
        """ 90% chance, 100+20%/stack quality"""
        if self.cp > 24:
            self._use_touch()
            self.iq_stacks = -1
            self.cp -= 24






