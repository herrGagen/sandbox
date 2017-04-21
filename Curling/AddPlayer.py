# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 14:37:28 2016

@author: johngalt
"""

import web
import urllib

import numpy as np
import pandas as pd

from jellyfish import damerau_levenshtein_distance as dldist

from curling_data import read_roster, read_ratings, read_sheet_count
from curling_data import write_roster, write_ratings, write_sheet_count

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
                            'Last Name': last}, index=[0])
        for cname in roster.columns[2:]:
            row[cname] = 1
        roster = roster.append(row, ignore_index=True)
        write_roster(roster)
        return True

    def _add_player_to_ratings(self, first, last, experience):
        ratings = read_ratings()
        if self._has_player(ratings, first, last):
            return False
        player = self._make_rating(first, last, experience)
        print player
        ratings = ratings.append(player, ignore_index=True)
        write_ratings(ratings)
        return True

    def _add_player_to_sheet_count(self, first, last):
        sheet_count = read_sheet_count()
        if self._has_player(sheet_count, first, last):
            return False
        row = pd.DataFrame({'First Name': first,
                            'Last Name': last}, index=[0])
        for cname in sheet_count.columns[2:]:
            row[cname] = 0
        sheet_count = sheet_count.append(row, ignore_index=True)
        write_sheet_count(sheet_count)
        return True

    def GET(self):
        data = web.input()
        if 'First' not in data:
            data['First'] = u''
        if 'Last' not in data:
            data['Last'] = u''
        items = [web.form.Textbox('First', value=data['First']),
                 web.form.Textbox('Last', value=data['Last']),
                 web.form.Dropdown('Years Played', ['0', '1', '2', '3+'])]
        if 'SimilarName' in data:
            name = urllib.unquote_plus(data['SimilarName'])
            suggest = web.form.Textarea('Did you mean: %s' % name)
            verify = web.form.Checkbox(id='verify',
                                       name='I meant what I typed.')
            items = [suggest] + items + [verify]
        new_player = web.form.Form(*items)
        return render.add_player(new_player)

    def find_similar_name(self, first, last):
        """
        If a similar name exists in the roster or ratings list, returns
        that name.
        """
        first = unicode(first)
        last = unicode(last)

        def dist_to(name):
            d_first = dldist(unicode(first), unicode(name[0]))
            d_last = dldist(unicode(last), unicode(name[1]))
            return d_first + d_last
        similar_name = None
        for df in [read_roster(), read_ratings()]:
            name_list = zip(df['First Name'], df['Last Name'])
            dists = map(dist_to, name_list)
            ind = np.argmin(dists)
            if dists[ind] != 0 and dists[ind] < len(first + last) / 5:
                similar_name = map(str, name_list[ind])
        try:
            return (similar_name[0], similar_name[1])
        except:
            return None

    def POST(self, arg=[]):
        player = web.input()
        first = player['First'].capitalize()
        last = player['Last'].capitalize()
        similar_name = self.find_similar_name(first, last)
        if similar_name:
            print player
            print all(['Did you mean:' not in x for x in player.keys()])
            if 'SimilarName' not in player:
                url = '/addPlayer?SimilarName={}&First={}&Last={}'
                raise web.seeother(url.format(similar_name, first, last))
            elif all(['Did you mean:' not in x for x in player.keys()]):
                raise web.seeother('/addPlayer')
        self._add_player_to_roster(first, last)
        self._add_player_to_ratings(first, last, player['Years Played'])
        self._add_player_to_sheet_count(first, last)
        return """<html><body>
        <a href="addPlayer">Add another player.</a>
        <a href="curling">Take attendance.</a>
        </body></html> """

if __name__ == "__main__":
    from jellyfish import damerau_levenshtein_distance as dldist
