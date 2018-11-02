class DataSet(object):
    def __init__(self, start_id, max_id):
        self.id = start_id
        self.max = max_id
        self.set = {}

    def add(self, value):
        new_id = self.get_id_by_value(value)

        if not new_id:
            self.id += 1
            new_id = self.id

            if new_id >= self.max:
                raise Exception('TableOfStrings overflow')

            self.set.__setitem__(new_id, value)
        return new_id

    def get_id_by_value(self, value):
        for key, val in self.set.items():
            if val == value:
                return key

        return False
