# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 16:11:33 2016

@author: johngalt
"""
import web


class StoplightRadioButton(web.form.Radio):

    def classes(self, i):
        is_checked = self.args[i % 3] == self.value
        color = 'primary'
        active = ' active'*is_checked
        return '<label class="btn btn-' + color + active + '">\n'

    def render(self):
        x = '<div class="btn-group" data-toggle="buttons">\n'
        for i, arg in enumerate(self.args):
            if isinstance(arg, (tuple, list)):
                value, desc = arg
            else:
                value, desc = arg, arg
            attrs = self.attrs.copy()
            attrs['name'] = self.name
            attrs['type'] = 'radio'
            attrs['value'] = value
            attrs['autocomplete'] = "off"
            if value == self.value:
                attrs['checked'] = None
            x += self.classes(i)
            x += '<input %s/> %s' % (attrs, web.net.websafe(desc))
            x += '\n</label>\n'
        x += '</div>\n'
        return x

if __name__ == "__main__":
    srb = StoplightRadioButton('test', ['a', 'Unknown', 'c'])
    srb.value = "Unknown"
    with open('./test_files/test.html', 'w') as outf:
        with open('./test_files/head.html', 'r') as head:
            outf.write(head.read())
        outf.write(srb.render())
        with open('./test_files/foot.html', 'r') as foot:
            outf.write(foot.read())
        srb.classes(0)
