# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:32:01 2016

@author: johngalt
"""
import time
import web

import pandas as pd

from AddPlayer import AddPlayer
from AttendanceForm import AttendanceForm

from find_teams import make_matching_teams
from curling_data import read_roster, read_ratings, read_sheet_count
from curling_data import write_roster

render = web.template.render('templates/')

urls = (
    '/', 'CurlingRedirect',
    '/curling', 'CurlingRedirect',
    '/curling/(.*)', 'CurlingAttendance',
    '/schedule/(.*)', 'ScheduleOutput',
    '/addPlayer', 'AddPlayer'
)

app = web.application(urls, globals()).wsgifunc()


class ScheduleOutput:

    def GET(self, arg=[]):
        teams = make_matching_teams(read_roster(),
                                    read_ratings(),
                                    read_sheet_count(),
                                    int(arg))
        old_width = pd.get_option('display.max_colwidth')
        pd.set_option('display.max_colwidth', -1)
        html = teams[['Sheet', 'Players']].to_html(index=False)
        pd.set_option('display.max_colwidth', old_width)
        return html


class CurlingRedirect:
    """
    Jumps to today's attendance sheet.
    If we don't curl today, jumps to week 1
    """
    def GET(self):
        df = read_roster()
        days = list(df.columns[2:])
        today = time.strftime("%m/%d/%y")
        try:
            week_num = days.index(today)
        except ValueError:
            week_num = 0
        raise web.seeother('curling/{0}'.format(week_num))


class CurlingAttendance:

    def update_attendance(self, df, week_num, status_dict):
        """
        Write attendance states to df.
        """
        def to_status(x):
            stat_string = status_dict[str(x)]
            return AttendanceForm.states.reverse[stat_string]
        stat_vect = map(to_status, range(len(df)))
        df.iloc[:, 2+week_num] = stat_vect
        write_roster(df)
        return

    def GET(self, arg=[]):
        df = read_roster()
        roster = AttendanceForm(df, int(arg))
        dates = zip(map(str, range(len(df.columns) - 2)), df.columns[2:])
        drop = web.form.Dropdown('Today\'s Date',
                                 dates,
                                 value=arg)
        date = web.form.Form(drop)
        return render.attendance(date(), roster())

    def POST(self, arg=[]):
        i = web.input()
        if i.get('Today\'s Date', False):
            raise web.seeother('{0}'.format(['Today\'s Date']))
        else:
            df = read_roster()
            self.update_attendance(df, int(arg), i)
            raise web.seeother('/schedule/{0}'.format(int(arg)))
        return ", ".join(x for x in i.keys())


if __name__ == "__main__":
    web.httpserver.runsimple(app, ("0.0.0.0", 8123))
