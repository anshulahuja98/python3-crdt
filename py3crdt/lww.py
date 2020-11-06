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
            payload (list): payload in which element has to be added.
            elem (any_type): The element to be added.

        Returns:
            payload (list): payload in which element is added.
        """

        # Boolean to keep track if elem present in the payload
        elem_present = False

        for i in range(len(payload)):
            # If elem is present update the timestamp
            if payload[i]['elem'] == elem:
                payload[i]['timestamp'] = datetime.now()
                elem_present = True
        
        # If elem is not present add the elem
        if not elem_present:
            payload.append({'elem': elem, 'timestamp': datetime.now()})

        payload.sort(key=lambda i: i['elem'])

        return payload

    @staticmethod
    def compare(payload1, payload2):
        """
        The function to compare two LWW objects' payload.

        Args:
            payload1 (list): payload to be compared with.
            payload2 (list): payload to be compared to.

        Returns:
            bool: True if payload of both objects are same, False otherwise.
        """

        for item_1 in payload1:
            if item_1 not in payload2:
                return False
        return True

    @staticmethod
    def merge(payload1, payload2):
        """
        The function to merge the payload2 to payload1.

        Args:
            payload1 (list): payload to be merged to.
            payload2 (list): payload to be merged from.

        Returns:
            payload1 (list): payload merged to.
        """

        # Append the elements of argument's payload to the object's payload.
        for item2 in payload2:
            
            # Boolean to keep track if item2 present in the payload1            
            elem_found = False
            
            for i, item1 in enumerate(payload1):
                # If item2's elem is present and its timestamp is greater than that of item1,
                # update the timestamp
                if item1['elem'] == item2['elem']:
                    elem_found = True
                
                    if item1['timestamp'] < item2['timestamp']:
                        payload1[i]['timestamp'] = item2['timestamp']

            # If item2 is not present, add it to the payload1
            if not elem_found:
                payload1.append(item2)

        payload1.sort(key=lambda i: i['elem'])
        return payload1

    @staticmethod
    def display(name, payload):
        """
        The function to print the object.

        Args:
            name (string): payload type.
            payload (list): payload to display.
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
        The function to compare the payload with the argument's payload.

        Args:
            lww (LWWElementSet): Object to be compared to.

        Note:
            Compares payload 'A' and payload 'R' of the objects

        Returns:
            bool: True if payload of both objects are same, False otherwise.
        """

        return self.lwwf.compare(self.A, lww.A) and self.lwwf.compare(self.R, lww.R)

    def merge(self, lww):
        """
        The function to merge the payload with the argument's payload.

        Args:
            lww (LWWElementSet): Object to be merged from.
        """

        # Merge payload 'A'
        self.A = self.lwwf.merge(self.A, lww.A)

        # Merge payload 'R'
        self.R = self.lwwf.merge(self.R, lww.R)

    def display(self):
        """
        The function to print the object's payload.
        """

        # Display payload 'A'
        self.lwwf.display('A', self.A)

        # Display payload 'R'
        self.lwwf.display('R', self.R)
