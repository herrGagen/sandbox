# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 13:58:17 2016

@author: johngalt
"""
import pandas as pd
import numpy as np


def calc_n_teams(n):
    """
    Calculates the number of sheets we can use, and number of 4 person teams
    on them.

    Note: 17 people can't play on any number of sheets with 3 and 4
    person teams.  They can do, at best, (3v3 3v3 3v2)

    n: Number of players.

    Returns: Number of sheets, how many teams are full
    """
    n_sheets = int(np.ceil(n / 8.0))
    n_full = int(n - 6 * n_sheets)
    return(n_sheets, n_full)


def sheet_score(player):
    return player.bad_sheet**2 \
        + player.okay_sheet \
        - 2*player.best_sheet


def make_matching_teams(roster, ratings, sheet_count, week):
    here = roster[roster.iloc[:, 2 + week] == 2]
    df = pd.merge(here[['First Name', 'Last Name']],
                  ratings,
                  on=['First Name','Last Name'])
    df = df.merge(sheet_count, on=['First Name', 'Last Name'])
    df.fillna(0, inplace=True)

    all_skips = df.sort_values(by='Skip', ascending=False)

    n_players = len(df)
    n_sheets, n_full = calc_n_teams(n_players)
    n_teams = 2*n_sheets
    skips = all_skips.iloc[range(n_teams), :]
    players = df[~df.isin(skips)].copy()
    players.dropna(inplace=True)

    # Round 1 draft: randomly order skips
    skips = skips.reindex(np.random.permutation(skips.index))
    day_teams = []
    for ind, player in skips.iterrows():
        name = player['First Name'] + ' ' + player['Last Name']
        rating = player['Skip']
        sheet_value = sheet_score(player)
        team = {'players': [name],
                'rating': 2 * rating,
                'sheet_value': sheet_value}
        day_teams.append(team)
    day_teams.sort(key=lambda x: x['rating'])

    # Round 2-4 draft: Each skip selects best player available
    # Then reorder teams so that weakest picks first next round
    factor = [1] * n_teams
    factor[n_full:] = [1.5] * (n_teams - n_full)
    for pos in ['Vice', 'Second', 'Lead']:
        noise = np.random.rand(len(players))
        players['sortcol'] = players[pos] + noise
        players.sort_values(by='sortcol', ascending=False, inplace=True)
        players.index = range(len(players))

        def to_player(row):
            name = row['First Name'] + ' ' + row['Last Name']
            rating = row[pos]
            sheet_value = sheet_score(player)
            return (name, rating, sheet_value)
        for i in range(min(n_teams, len(players))):
            p_name, p_rating, p_sheet_value = to_player(players.loc[i])
            team = day_teams[i]
            rating = team['rating'] + factor[i]*p_rating
            sheet_value = team['sheet_value'] + p_sheet_value
            names = team['players']
            names.append(p_name)
            day_teams[i] = {'players': names,
                            'rating': rating,
                            'sheet_value': sheet_value}
        players = players[n_teams:].copy()
        day_teams.sort(key=lambda x: x['rating'])
    team_df = assign_sheets(day_teams)
    return team_df


def assign_sheets(day_teams):

    def sval(i):
        k = i - i % 2
        a = day_teams[k]
        b = day_teams[k+1]
        return a['sheet_value'] + a['rating']/100.0 \
            + b['sheet_value'] + b['rating']/100.0

    sheet_val = map(sval, range(len(day_teams)))
    teams = [b for a, b in sorted(zip(sheet_val, day_teams))]

    n = len(day_teams)/2
    sheets = range(n / 2 + n % 2)
    sheets.reverse()
    backs = range(n / 2 + n % 2, n)

    def next_sheet(i):
        return 1 + (backs[i / 2] if i % 2 else sheets[i / 2])
    asgn = [next_sheet(i) for i in range(n) for _ in (0, 1)]

    def player_column():
        retval = []
        for t in teams:
            retval.append(", ".join(t['players']))
        return retval
    df = pd.DataFrame({'Sheet': asgn,
                        'Players': player_column()})
    df.sort_values('Sheet', inplace=True)
    return df


if __name__ == "__main__":
    ratings = pd.read_csv('ratings.csv')
    roster = pd.read_csv('roster.csv')
    make_matching_teams(roster, ratings, 2)
