class CircularList(list):
    size = None
    filled = None

    def __init__(self, size, *args, **kw):
        self.size = size
        self.filled = False
        super(CircularList, self).__init__(*args, **kw)

    def append(self, item):
        if len(self) == self.size:
            self.pop(0)
        elif len(self) == (self.size - 1):
            self.filled = True
        super(CircularList, self).append(item)

    def get_snapshot(self):
        return list(self)
