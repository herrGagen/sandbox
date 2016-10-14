# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 16:32:01 2016

@author: johngalt
"""
import pandas as pd
import time
import web
from AttendanceForm import AttendanceForm
from find_teams import make_matching_teams

render = web.template.render('templates/')

urls = (
    '/', 'CurlingRedirect',
    '/curling', 'CurlingRedirect',
    '/curling/(.*)', 'CurlingAttendance',
    '/schedule/(.*)', 'ScheduleOutput'
)

app = web.application(urls, globals())
if __name__ != "__main__":
    app = app.wsgifunc()

def read_roster():
    df = pd.read_csv('roster.csv')
    df.fillna(0, inplace=True)
    for col in df.columns[2:]:
        df[col] = map(int, df[col])
    return df


def read_ratings():
    df = pd.read_csv('ratings.csv')
    return df


def read_sheet_count():
    df = pd.read_csv('sheet_count.csv')
    return df


def write_roster(df):
    df.to_csv('roster.csv', index=False)


class ScheduleOutput:

    def GET(self, arg=[]):
        teams = make_matching_teams(read_roster(),
                                    read_ratings(),
                                    read_sheet_count(),
                                    int(arg))
        return teams[['Sheet', 'Players']].to_html(index=False)


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
        except:
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
        drop = web.form.Dropdown('week_drop',
                                 dates,
                                 value=arg)
        date = web.form.Form(drop)
        return render.twoForms(date(), roster())

    def POST(self, arg=[]):
        i = web.input(week_drop={})
        if i.week_drop:
            raise web.seeother('{0}'.format(i.week_drop))
        else:
            df = read_roster()
            self.update_attendance(df, int(arg), i)
            raise web.seeother('/schedule/{0}'.format(int(arg)))
        return ", ".join(x for x in i.keys())


if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 8123))
