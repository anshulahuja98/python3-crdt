class GSet:
    def __init__(self, id):
        self.payload = []
        self.id = id

    def add(self, elem):
        self.payload.append(elem)
        self.payload.sort()

    def query(self, elem):
        return elem in self.payload

    def compare(self, gs2):
        for elem in self.payload:
            if elem not in gs2.payload:
                return False
        return True

    def merge(self, gs2):
        for elem in gs2.payload:
            if elem not in self.payload:
                self.payload.append(elem)
        self.payload.sort()

    def display(self):
        print(self.payload)
