import tkinter
import threading
import time
import string


class OnTopTextBox(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.root = tkinter.Tk()
        self.data = tkinter.StringVar()
        self.data.set(data)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        label = tkinter.Label(self.root, textvariable=self.data)
        label.config(width = 40)
        label.config(justify=tkinter.LEFT)
        label.config(anchor=tkinter.NW)
        label.config(wraplength = 280)
        label.pack()
        self.root.wm_attributes("-topmost", 1)
        self.root.mainloop()

    def append(self, add, delim ='\t'):
        assert isinstance(add, str)
        assert isinstance(delim, str)
        temp_string = self.data.get() + delim + add
        self.data.set(temp_string)

    def set_text(self,msg):
        assert isinstance(msg, str)
        self.data.set(msg)

    def destroy(self):
        self.root.destroy()

if __name__ == "__main__":
    tb = OnTopTextBox("nope")
    time.sleep(1)
    tb.append("boo")
    time.sleep(1)
    tb.append("too",'\n')
    time.sleep(1)
    tb.append("three",", ")
    time.sleep(1)
    tb.set_text("Job's done")
    time.sleep(1)
    tb.destroy()


