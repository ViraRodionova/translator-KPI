class CustomException(Exception):
    def __init__(self, position, value):
        self.position = position
        self.value = value


class UnexpectedSymbolException(CustomException):
    def __str__(self):
        return "Unexpected symbol: {0}. Line: {1}:{2}".format(self.value, self.position[0], self.position[1])


class EndOfFileException(CustomException):
    def __str__(self):
        return "End of File. Line: {0}:{1}".format(self.position[0], self.position[1])
