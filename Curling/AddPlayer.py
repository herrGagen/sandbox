# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 14:37:28 2016

@author: johngalt
"""

import web
import pandas as pd

from curling_data import read_roster, read_ratings
from curling_data import write_roster, write_ratings

render = web.template.render('templates/')


class AddPlayer:

    def _has_player(self, df, first, last):
        test = df[(df['First Name'] == first) & (df['Last Name'] == last)]
        if len(test) > 0:
            print "Player already exists."
            return True
        return False

    def _make_rating(self, first, last, experience):
        row_dict = {'First Name': first,
                    'Last Name': last}
        if experience == '0':
            row_dict.update({'Lead': 2,
                             'Second': 1,
                             'Vice': 0,
                             'Skip': None})
        elif experience == '1':
            row_dict.update({'Lead': 4,
                             'Second': 2,
                             'Vice': 1,
                             'Skip': None})
        elif experience == '2':
            row_dict.update({'Lead': 7,
                             'Second': 7,
                             'Vice': 5,
                             'Skip': 3})
        else:
            row_dict.update({'Lead': 8,
                             'Second': 8,
                             'Vice': 6,
                             'Skip': 4})
        return pd.DataFrame(row_dict, index=[0])

    def _add_player_to_roster(self, first, last):
        roster = read_roster()
        if self._has_player(roster, first, last):
            return False
        row = pd.DataFrame({'First Name': first,
                            'Last Name': last},index=[0])
        for cname in roster.columns[2:]:
            row[cname] = 1
        roster = roster.append(row, ignore_index=True)
        write_roster(roster)
        return True

    def _add_player_to_ratings(self, first, last, experience):
        ratings = read_ratings()
        if self._has_player(ratings, first, last):
            return
        player = self._make_rating(first, last, experience)
        print player
        ratings = ratings.append(player, ignore_index = True)
        write_ratings(ratings)

    def GET(self, arg=[]):
        new_player = web.form.Form(
            web.form.Textbox('First'),
            web.form.Textbox('Last'),
            web.form.Dropdown('Years Played', ['0', '1', '2', '3+'])
        )
        return render.form(new_player)

    def POST(self, arg=[]):
        player = web.input()
        first = player['First']
        if first == first.lower():
            first = first.capitalize()
        last = player['Last'].capitalize()
        if last == last.lower():
            last = last.capitalize()
        experience = player['Years Played']
        self._add_player_to_roster(first, last)
        self._add_player_to_ratings(first, last, experience)
        return """<html><body>
        <a href="addPlayer">Add another player.</a>
        <a href="curling">Take attendance.</a>
        </body></html> """
