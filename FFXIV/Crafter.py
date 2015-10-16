from FFXIV import *
from CraftReader import *
import math

DEBUG = False

class Crafter:
    @staticmethod
    def keymap(x):
        return {
            "Careful Synth II": '1',
            "Hasty Touch": '2',
            "Manipulation": '3',

            "Comfort Zone": '4',
            "Inner Quiet": '5',
            "Tricks of the Trade": '6',

            "Ingenuity II": '7',
            "Steady Hands II": '8',
            "Great Strides": '9',

            "Innovation": '0',

            "Rapid Synth": '^1',
            "Byregot Blessing": '^2',

            "Waste Not II": '^4',
            "Masters Mend": '5',
            "Masters Mend II": '^6',

            "Basic Touch": '^7',
            "Standard Touch": '^8',
            "Advanced Touch": '^9',

            "Precise Touch": '^0',

            "Makers Mark": "!1",
            "Flawless Synth": "!2"
        }.get(x, [])

    def __init__(self,
                 cp=360,
                 total_dur=40,
                 careful_prog=150,
                 total_prog=1500,
                 num_mark=0,
                 stack_goal=9):
        self.max_cp = cp
        self._reader = CraftReader()
        self._ff = FFXIV()
        self.careful_prog = careful_prog
        self.total_prog = total_prog
        self.total_dur = total_dur
        self.num_mark = num_mark
        self.stack_goal = stack_goal
        self.cp = self.max_cp
        self.manip_turns = 0
        self.waste_turns = 0
        self.steady_turns = 0
        self.inno_turns = 0
        self.ing_turns = 0
        self.stride_turns = 0
        self.iq_stacks = -1
        self.czone_turns = 0
        self.spent_dur = 0.0
        self.progress, self.quality = self._reader.progress
        self.last_quality = self.quality
        self.label = None
        self.mark_turns = 0
        self.next_craft()

    # Auxiliary methods
    def next_craft(self):
        self.cp = self.max_cp
        self.manip_turns = 0
        self.waste_turns = 0
        self.steady_turns = 0
        self.inno_turns = 0
        self.stride_turns = 0
        self.iq_stacks = -1
        self.ing_turns = 0
        self.czone_turns = 0
        self.mark_turns = 0
        self.spent_dur = 0
        self.progress, self.quality = self._reader.progress
        self.last_quality = self.quality

    @property
    def condition(self):
        return self._reader.condition

    @property
    def is_crafting(self):
        return self._reader.is_crafting

    def _calc_remaining_synths(self):
        p, q = self.read_progress()
        if not self.is_crafting:
            return 1
        else:
            progress = p * self.total_prog
            remaining_turns = math.ceil((self.total_prog - progress) / self.careful_prog)
            if(DEBUG):
                print("Remaining touches: ", remaining_turns)
            return remaining_turns

    def display_status(self):
        try:
            self.label.destroy()
        except AttributeError:
            pass
        # self.label = OnTopTextBox("Crafter label")
        self._update_pq()
        text = "Prog %f \t Qual %f\n" % (self.progress, self.quality)
        text += "%d\t Spent durability\n" % self.spent_dur
        if self.manip_turns > 0:
            text += "%d\t Manip turns\n" % self.manip_turns
        if self.czone_turns > 0:
            text += "%d \t Comfort Zone turns\n" % self.czone_turns
        if self.waste_turns > 0:
            text += "%d \tWaste Not turns\n" % self.waste_turns
        if self.iq_stacks > -1:
            text += "%d \tInner Quiet Stacks\n" % self.iq_stacks
        print(text)

    def _advance_turn(self):
        if self.manip_turns > 0:
            self.manip_turns -= 1
            self._mend(10)

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

        if self.ing_turns > 0:
            self.ing_turns -= 1

        if self.mark_turns > 0:
            self.mark_turns -= 1

    def _inc_cp(self, amt):
        self.cp += amt
        if self.cp > self.max_cp:
            self.cp = self.max_cp

    def _mend(self, amount):
        self.spent_dur -= amount
        if self.spent_dur < 0:
            self.spent_dur = 0

    def _send_action(self, action):
        if DEBUG:
            print("Sending %s" % action)
        to_press = Crafter.keymap(action)
        self._ff.send_key(to_press)
        time.sleep(3)

    def accept_collectible(self):
        self._ff.send_key('#0')
        time.sleep(0.5)
        self._ff.send_key('#0')

    ## Durability Skills
    def use_manipulation(self):
        if self.cp >= 88:
            self._send_action("Manipulation")
            self._advance_turn()
            self.manip_turns = 3
            self.cp -= 88

    def use_masters_mend(self):
        if self.cp >= 92:
            self._send_action("Masters Mend")
            self._advance_turn()
            self._mend(30)
            self.cp -= 92

    def use_masters_mend_2(self):
        if self.cp >= 160:
            self._send_action("Masters Mend II")
            self._advance_turn()
            self._mend(60)
            self.cp -= 160

    def use_waste_not_2(self):
        if self.cp >= 98:
            self._send_action("Waste Not II")
            self._advance_turn()
            self.waste_turns = 8
            self.cp -= 98

    ## Buffs
    def use_makers_mark(self, turns):
        """Only works on first turn, makes flawless synth free"""
        if self.cp == self.max_cp:
            self._send_action("Makers Mark")
            self.cp -= 20
            self._advance_turn()
            self.mark_turns = turns

    def use_inner_quiet(self):
        if self.cp >= 18:
            self._send_action("Inner Quiet")
            self._advance_turn()
            self.cp -= 18
            self.iq_stacks = 2  # Reader misses first stack

    def use_great_strides(self):
        if self.cp >= 32:
            self._send_action("Great Strides")
            self._advance_turn()
            self.stride_turns = 3
            self.cp -= 32

    def use_ingenuity_2(self):
        if self.cp >= 32:
            self._send_action("Ingenuity II")
            self._advance_turn()
            self.ing_turns = 5
            self.cp -= 32

    def use_innovation(self):
        if self.cp >= 18:
            self._send_action("Innovation")
            self._advance_turn()
            self.inno_turns = 3
            self.cp -= 18

    def use_steady_hand_2(self):
        if self.cp >= 25:
            self._send_action("Steady Hands II")
            self._advance_turn()
            self.steady_turns = 5
            self.cp -= 25

    ## CP Skills
    def _can_trick(self):
        if (self._reader.condition == Condition.Good
            or self._reader.condition == Condition.Excellent):
            return True
        return False

    def use_tricks(self):
        if self._can_trick():
            self._send_action("Tricks of the Trade")
            self._advance_turn()
            self._inc_cp(20)

    def use_comfort_zone(self):
        if self.cp >= 66:
            self._send_action("Comfort Zone")
            self._advance_turn()
            self.czone_turns = 10
            self.cp -= 66

    ## Progress / touch utils
    def _use_durability(self):
        cost = 10
        if self.waste_turns > 0:
            cost = 5
        self.spent_dur += cost
        self._advance_turn()
        time.sleep(0.5)
        self._update_pq()

    def _update_pq(self):
        (self.progress, self.quality) = self._reader.progress

    def _use_touch(self, inc=1):
        self._use_durability()
        if self.quality > self.last_quality and self.iq_stacks >= 0:
            self.iq_stacks += inc
        self.last_quality = self.quality

    ## Progress actions
    def use_careful_synth_2(self):
        """100% chance of 120% progress"""
        self._send_action("Careful Synth II")
        self._use_durability()

    def use_rapid_synth(self):
        """ 50% chance of 250% progress """
        self._send_action("Rapid Synth")
        self._use_durability()

    def use_flawless_synth(self):
        "90% success, 40 progress, free if makers mark"
        self._send_action("Flawless Synth")
        if self.mark_turns > 0:
            self._advance_turn()
        else:
            self._use_durability()

    ## Touch Actions
    def use_hasty_touch(self):
        """ 50% chance of 100% quality"""
        self._send_action("Hasty Touch")
        self._use_touch()

    def use_bblessing(self):
        """ 90% chance, 100+20%/stack quality"""
        if self.cp >= 24:
            self._send_action("Byregot Blessing")
            self._use_touch()
            self.iq_stacks = -1
            self.cp -= 24

    def use_basic_touch(self):
        """70% Success 100% Quality"""
        if self.cp >= 18:
            self._send_action("Basic Touch")
            self._use_touch()
            self.cp -= 18

    def use_std_touch(self):
        """80% Success 125% Quality"""
        if self.cp >= 32:
            self._send_action("Standard Touch")
            self._use_touch()
            self.cp -= 32

    def use_adv_touch(self):
        """90% Success 150% Quality"""
        if self.cp >= 48:
            self._send_action("Advanced Touch")
            self._use_touch()
            self.cp -= 48

    def use_precise_touch(self):
        """70% Success 100% Quality"""
        if self.cp >= 18 and self._can_trick():
            self._send_action("Precise Touch")
            self._use_touch(2)
            self.cp -= 18

    def start_craft(self):
        for x in range(0, 3):
            self._ff.send_key('#0', 1.0)
            print("Hit 0")
        self.next_craft()

    def read_progress(self):
        return self._reader.progress


if __name__ == "__main__":
    import time

    crafter = Crafter(500)

    time.sleep(4)
    for x in range(1, 4):
        print("Should send 1")
        crafter._send_action("Manipulation")
        time.sleep(5)
