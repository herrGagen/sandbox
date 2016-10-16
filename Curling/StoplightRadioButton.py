# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 16:11:33 2016

@author: johngalt
"""
import web

class StoplightRadioButton(web.form.Radio):

    def classes(self, i):
        is_checked = self.args[i%3] == self.value
        retval = '<label class="btn btn-'
#        if i%3 == 0:
#            retval += 'danger'
#        elif i%3 == 1:
#            retval += 'warning'
#        else:
#            retval += 'success'
        retval += 'primary'
        if is_checked:
            retval += ' active">\n'
        else:
            retval += '">\n'
        return retval


    def render(self):
        x = '<div class="btn-group" data-toggle="buttons">\n'
        for i,arg in zip(range(len(self.args)),self.args):
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

if __name__=="__main__":
    srb = StoplightRadioButton('test',['a','Unknown','c'])
    srb.value="Unknown"
    with open('d:/code/curling/templates/test.html', 'w') as outf:
        outf.write("""
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <!-- Required meta tags always come first -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <meta http-equiv="x-ua-compatible" content="ie=edge">

                <!-- Bootstrap CSS -->
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.4/css/bootstrap.min.css" integrity="2hfp1SzUoho7/TsGGGDaFdsuuDL0LX2hnUp6VkX3CUQ2K4K+xjboZdsXyp4oUHZj" crossorigin="anonymous">
              </head>
              <body>
        """)
        outf.write(srb.render())
        outf.write("""
                        <!-- jQuery first, then Tether, then Bootstrap JS. -->
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js" integrity="sha384-THPy051/pYDQGanwU6poAc/hOdQxjnOEXzbT+OuUAFqNqFjL+4IGLBgCJC3ZOShY" crossorigin="anonymous"></script>
                        <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.2.0/js/tether.min.js" integrity="sha384-Plbmg8JY28KFelvJVai01l8WyZzrYWG825m+cZ0eDDS1f7d/js6ikvy1+X+guPIB" crossorigin="anonymous"></script>
                        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.4/js/bootstrap.min.js" integrity="VjEeINv9OSwtWFLAtmc4JCtEJXXBub00gtSnszmspDLCtC0I4z4nqz7rEFbIZLLU" crossorigin="anonymous"></script>
                        </body>
                    </html>
        """)
        srb.classes(0)
