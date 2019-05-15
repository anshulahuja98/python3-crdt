from datetime import datetime


class LWWFunctions:
    """
    A class to provide static methods to LWWElementSet Class
    """

    @staticmethod
    def update(payload, elem):
        """
        The function to add an element to Payload.

        Args:
            payload (list): payloads in which element has to be addeds.
            elem (any_type): The element to be added.

        Returns:
            payload (list): payloads in which element is added.
        """

        payload.append({'elem': elem, 'timestamp': datetime.now()})
        payload.sort(key=lambda i: i['timestamp'])
        return payload

    @staticmethod
    def compare(payload1, payload2):
        """
        The function to compare two LWW objects' payloads.

        Args:
            payload1 (list): payloads to be compared withs.
            payload2 (list): payloads to be compared tos.

        Returns:
            bool: True if payloads of both objects are same, False otherwise.
        """

        # Bool value to test equality
        item = False

        for item_1 in payload1:
            for item_2 in payload2:
                if item_2['elem'] == item_1['elem']:
                    item = True
                    break
            if item:
                break
        return item

    @staticmethod
    def merge(payload1, payload2):
        """
        The function to merge the payload2 to payload1.

        Args:
            payload1 (list): payloads to be merged tos.
            payload2 (list): payloads to be merged froms.

        Returns:
            payload1 (list): payloads merged tos.
        """

        # Append the elements of argument's payload to the object's payload.
        for item in payload2:
            if item not in payload1:
                payload1.append(item)

        # Sort the payload.
        payload1.sort(key=lambda i: i['timestamp'])

        return payload1

    @staticmethod
    def display(name, payload):
        """
        The function to print the object.

        Args:
            name (string): payloads types.
            payload (list): payloads to displays.
        """

        # Prints the type name of the payload
        print("{}: ".format(name), end="")

        # Prints elements with timestamps in microseconds
        for item in payload:
            print("{}:{}".format(item["elem"], item["timestamp"].microsecond), end=", ")

        # Prints a new line
        print()


class LWWElementSet():
    """
    Last-Writer-Wins Element Set CRDT Implementation.

    Notes:
        Similar to 2P-Set except each element is added/removed with a timestamp.
        An element is a member of the set if it is in the “add” set but not in the “remove” set,
        or if it is in both the “add” and “remove” set
        then timestamp in “remove” set should be less than that of the latest timestamp in “add” set.
        “Bias” comes into play, if timestamps are equal which can be towards “add” or “remove”.
        In this set, an element can be reinserted after being removed and thus, it has an advantage over 2P-Set.

    Attributes:
        A (list): List of elements added.
        R (list): List of elements removed.
        id (any_type): ID of the class object.
        lwf (LWWFunctions): LWWFunctions object to access the static methods.
    """

    def __init__(self, id):
        self.A = []
        self.R = []
        self.id = id
        self.lwwf = LWWFunctions()

    def add(self, elem):
        """
        The function to add the element.

        Args:
            elem (any_type): The element to be added.

        Note:
            'elem' is added to payload 'A'
        """

        self.A = self.lwwf.update(self.A, elem)

    def remove(self, elem):
        """
        The function to remove the element.

        Args:
            elem (any_type): The element to be removed.

        Note:
            'elem' is added to payload 'R'
        """

        self.R = self.lwwf.update(self.R, elem)

    def query(self, elem):
        """
        The function to return True if element is present in the payload.

        Args:
            elem (any_type): The element to be searched for.

        Returns:
            bool: True if element present in the payload 'A' with latest timestamp than in payload 'R', False otherwise.
        """

        elem_in_a = [item for item in self.A if item['elem'] == elem]
        if len(elem_in_a) != 0:
            elem_in_r = [item for item in self.R if item['elem'] == elem]
            if len(elem_in_r) == 0 or elem_in_r[-1]["timestamp"] < elem_in_a[-1]["timestamp"]:
                return True
        return False

    def compare(self, lww):
        """
        The function to compare the payloads with the argument's payloads.

        Args:
            lww (LWWElementSet): Object to be compared to.

        Note:
            Compares payload 'A' and payload 'R' of the objects

        Returns:
            bool: True if payloads of both objects are same, False otherwise.
        """

        return self.lwwf.compare(self.A, lww.A) and self.lwwf.compare(self.R, lww.R)

    def merge(self, lww):
        """
        The function to merge the payloads with the argument's payloads.

        Args:
            lww (LWWElementSet): Object to be merged from.
        """

        # Merge payload 'A'
        self.A = self.lwwf.merge(self.A, lww.A)

        # Merge payload 'R'
        self.R = self.lwwf.merge(self.R, lww.R)

    def display(self):
        """
        The function to print the object's payloads.
        """

        # Display payload 'A'
        self.lwwf.display('A', self.A)

        # Display payload 'R'
        self.lwwf.display('R', self.R)
