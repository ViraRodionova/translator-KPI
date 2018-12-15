class Scanner:
    def __init__(self, filename):
        self.line = 1
        self.column = 1
        self.lineP = 1 # remember start 
        self.columnP = 1
        self.f = open(filename, 'r')
        self.out = []
        self.positions = [] # array of two elements (row and column)
        self.c = '' # current symbol

    def decreaseCol(self):
        self.columnP -=1

    def read(self, flag=False):
        c = self.f.read(1)

        self.c = c

        if c:
            if flag:
                self.lineP = self.line
                self.columnP = self.column

            if ord(c) == 10:
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return c

    def append(self, code, res='none'):
        print(self.lineP, '\t', self.columnP, '\t', code, '\t', res)
        self.out.append(code)
        self.positions.append([self.lineP, self.columnP])

        self.lineP = self.line
        self.columnP = self.column

    def exception(self, ExceptionClass, c=''):
        raise ExceptionClass([self.lineP, self.columnP], c)

    def handleEndOfReading(self):
        self.f.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()
