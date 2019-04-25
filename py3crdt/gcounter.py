class GCounter:
    def __init__(self, id):
        self.payload = {}
        self.id = id

    def add_new_node(self, key):
        self.payload[key] = 0

    def inc(self, key):
        try:
            self.payload[key] += 1
        except Exception as e:
            print("{}".format(e))

    def query(self):
        return sum(self.payload.values())

    def compare(self, gc2):
        for key in self.payload:
            if self.payload[key] > gc2.payload[key]:
                return False

    def merge(self, gc2):
        new_payload = {key: 0 for key in self.payload}
        for key in self.payload:
            new_payload[key] = max(self.payload[key], gc2.payload[key])
        self.payload = new_payload
        # self.display()

    def display(self):
        print(self.payload.values())
