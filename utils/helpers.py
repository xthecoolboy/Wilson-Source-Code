import sys
import time
import datetime


def open_file(file):
    with open(file, 'r') as f_open:
        return f_open.read()


def convert_time(duration):
    sec = datetime.timedelta(seconds = duration)
    d = datetime.datetime(1, 1, 1) + sec
    return ("%dd %dh %dm %ds" % (d.day - 1, d.hour, d.minute, d.second))


def date(target, clock=True):
    if clock is False:
        target = time.strftime("%x %X")
    else:
        target = time.strftime("%x %X %Z")
    return target

class StringManipulator:
    def __init__(self, value : str = None, capacity : int = sys.maxsize):
        if value is None:
            value = ""
        self.value = value
        self.capacity = capacity
        if(self.capacity < 0):
            self.capacity /= -1
        if (len(self.value) > self.capacity):
            self.value = self.value[:-(len(self.value) - self.capacity)]

    def __str__(self):
        return  self.value

    def setter(self):
        if (len(self.value) > self.capacity):
            self.value = self.value[:-(len(self.value) - self.capacity)]

    def build_array(self, array, separator=" "):
        value = ""
        index = 0
        for item in array:
            value += item
            index += 1
            if (index != len(array)):
                value += separator
        self.value += value
        self.setter()
        return value