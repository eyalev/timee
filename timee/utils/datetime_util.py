

class Datetime(object):

    def __init__(self, datetime):
        self._datetime = datetime

    @property
    def datetime(self):
        return self._datetime

    @property
    def time(self):
        string = self.datetime.strftime('%H:%M')
        return string
