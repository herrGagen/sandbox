# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 00:16:25 2016

@author: johngalt
"""
import web
import pandas as pd

from StoplightRadioButton import StoplightRadioButton as srb

class AttendanceForm(web.form.Form):

    class states:
         sick='Called In'
         default='?'
         here='Here'
         reverse = {sick: 0, default: 1, here:2}
         as_list = [sick, default, here]

    def __init__(self, df, week_num=1, **kw):
        self.df = df
        self.week_num = week_num
        buttons = []
        for i, _ in df.iterrows():
            buttons.append(srb(str(i),
                           AttendanceForm.states.as_list))
        web.form.Form.__init__(self, *buttons, **kw)

    def render(self):
        this_week = 2+self.week_num
        df = self.df
        out = ''
        out += self.rendernote(self.note)
        out += '<table class="table table-striped"><tr>\n'
        out += '<th>First</th>\t'
        out += '<th>Last</th>\t'
        out += '<th>Here?</th></tr>\n'
        for i in range(len(self.inputs)):
            radio = self.inputs[i]
            if df.iloc[i, this_week] == 0:
                radio.value = self.states.sick
            else:
                radio.value = self.states.here
            out += '    <tr>'
            out += '<td>{0}</td>\t'.format(df.loc[i, 'First Name'])
            out += '<td>{0}</td>\n'.format(df.loc[i, 'Last Name'])

            html = web.utils.safeunicode(radio.pre) \
                    + radio.render() \
                    + self.rendernote(radio.note) \
                    + web.utils.safeunicode(radio.post)
            out += '<td>{0}</td>\n'.format(html)
            out += '</tr>\n'
        out += "</table>\n"
        return out


if __name__ == "__main__":
    df = pd.read_csv('roster.csv')
    df.fillna(0, inplace=True)
    for col in df.columns[2:]:
        df[col] = map(int, df[col])
    fm = AttendanceForm(df,1)
    print fm.render()
