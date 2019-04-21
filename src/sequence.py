from datetime import datetime


class SeqFunctions:
    @staticmethod
    def add(payload, elem, id):
        payload.append((elem, id))
        payload.sort(key=lambda i: i[1])
        return payload

    @staticmethod
    def remove(payload, id):
        payload.append(id)
        payload.sort()
        return payload

    @staticmethod
    def merge(payload1, payload2):
        for item in payload2:
            if item not in payload1:
                payload1.append(item)
        return payload1

    @staticmethod
    def display(name, payload):
        print("{}: ".format(name), payload)

    @staticmethod
    def get_seq(payload):
        seq = ""
        for elem in payload:
            seq += elem
        return seq


class Sequence():
    def __init__(self, id):
        self.elem_list = []
        self.id_remv_list = []
        self.id_seq = []
        self.elem_seq = []
        self.id = id
        self.seqf = SeqFunctions()

    def update_seq(self, func):
        if func == "r":
            for id in self.id_remv_list:
                if id in self.id_seq:
                    del self.elem_seq[self.id_seq.index(id)]
                    self.id_seq.remove(id)
            self.id_seq.sort()
        if func == "a":
            for item in self.elem_list:
                if item[1] not in self.id_remv_list and item[1] not in self.id_seq:
                    self.id_seq.append(item[1])
            self.id_seq.sort()
            for id in self.id_seq:
                for item in self.elem_list:
                    if item[1] == id:
                        if len(self.elem_seq) > self.id_seq.index(id):
                            if item[0] != self.elem_seq[self.id_seq.index(id)]:
                                self.elem_seq.insert(self.id_seq.index(id), item[0])
                        else:
                            self.elem_seq.append(item[0])

    def add(self, elem, id):
        self.elem_list = self.seqf.add(self.elem_list, elem, id)
        self.update_seq("a")

    def remove(self, id):
        self.id_remv_list = self.seqf.remove(self.id_remv_list, id)
        self.update_seq("r")

    def query(self, id):
        for item in self.elem_list:
            if item[1] == id:
                if id not in self.id_remv_list:
                    return True
                else:
                    return False
        return False

    def merge(self, seq):
        self.elem_list = self.seqf.merge(self.elem_list, seq.elem_list)
        self.id_remv_list = self.seqf.merge(self.id_remv_list, seq.id_remv_list)
        self.update_seq("a")

    def display(self):
        self.seqf.display("Elem List", self.elem_list)
        self.seqf.display("ID Removed List", self.id_remv_list)
        self.seqf.display("ID Seq", self.id_seq)
        self.seqf.display("Elem Seq", self.elem_seq)

    def get_seq(self):
        return self.seqf.get_seq(self.elem_seq)
