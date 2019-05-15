class ORSetFunctions:
    """
    A class to provide static methods to ORSet Class
    """

    @staticmethod
    def add(payload, elem, unique_tag):
        """
        The function to add an element with it's unique tag to ORSet object's payload.

        Args:
            payload (list): Payload in which element has to be added.
            elem (any_type): The element to be added.
            unique_tag (any_type): Tag to identify element.

        Returns:
            payload (list): Payload in which element is added.
        """

        # Bool value to check if element already in payload
        found = False
        for item in payload:

            # If element already in payload, add unique_tag to it's tag_list
            if elem == item["elem"]:
                item["tags"].append(unique_tag)
                found = True
                break

        # If element not in payload, add element with unique tag
        if not found:
            payload.append({"elem": elem, "tags": [unique_tag]})

        # Sort the payload
        payload.sort(key=lambda i: i['elem'])

        return payload

    @staticmethod
    def remove(payloadA, payloadR, elem):
        """
        The function to remove an element from ORSet object's payload.

        Args:
            payloadA (list): Payload in which elements to be added are added.
            payloadR (list): Payload in which elements to be removed are added.
            elem (any_type): The element to be removed.

        Note:
            It searches for element in payloadA,
            and copies it's tags to payloadR

        Returns:
            payloadR (list): Payload in which elements to be removed are added.
        """

        # Search for element in payloadA and collect it's tags
        elem_tags = []
        if len(payloadA):
            for item in payloadA:
                if elem == item["elem"]:
                    elem_tags += item["tags"]
                    break
        else:
            return

        # Bool value to check if element already in payloadR
        found = False
        for item in payloadR:

            # If element already in payloadR, merge tags from elem_tags list.
            if elem == item["elem"]:
                item["tags"] = item["tags"] + list(set(elem_tags) - set(item["tags"]))
                found = True
                break

        # If element not in payloadR, add element with elem_tags list
        if not found:
            payloadR.append({"elem": elem, "tags": elem_tags})

        # Sort the payload
        payloadR.sort(key=lambda i: i['elem'])

        return payloadR

    @staticmethod
    def compare(payload1, payload2):
        """
        The function to compare two ORSet objects' payloads.

        Args:
            payload1 (list): Payload to be compared with.
            payload2 (list): Payload to be compared to.

        Returns:
            bool: True if payloads of both objects are same, False otherwise.
        """

        if len(payload1):
            for item1 in payload1:
                for item2 in payload2:
                    if item1 != item2:
                        return False
        else:
            # print("No elements added")
            return False
        return True

    @staticmethod
    def merge(payload1, payload2):
        """
        The function to merge the payload2 to payload1.

        Args:
            payload1 (list): Payload to be merged to.
            payload2 (list): Payload to be merged from.

        Returns:
            payload1 (list): Payload merged to.
        """

        for item2 in payload2:
            found = False
            for item1 in payload1:
                if item1['elem'] == item2['elem']:
                    item1["tags"] = item1["tags"] + list(set(item2["tags"]) - set(item1["tags"]))
                    found = True
                    break
            if not found:
                payload1.append({"elem": item2["elem"], "tags": item2["tags"]})

        # Sort the payload.
        payload1.sort(key=lambda i: i['elem'])

        return payload1

    @staticmethod
    def display(name, payload):
        """
        The function to print the object.

        Args:
            name (string): Payload type.
            payload (list): Payload to display.

        Returns:
            -1: If no element in the payload
        """

        # Prints the type name of the payload
        print("{}: ".format(name))

        # Prints elements with timestamps in microseconds
        if len(payload):
            for item in payload:
                print("{}:{}".format(item["elem"], item["tags"]))
                pass
        else:
            # print("No elements to show")
            return -1

    @staticmethod
    def query(elem, payload):
        """
        The function to return tags list if element is present in the payload.

        Args:
            elem (any_type): The element to be searched for.
            payload (list): Payload to query from.

        Returns:
            list: Tags list if element is present in the payload, Empty list otherwise.
        """

        if len(payload):
            for item in payload:
                if elem == item["elem"]:
                    return item["tags"]
            return []
        else:
            # print("No elements to query")
            return []


class ORSet():
    """
    Observed-Removed Set CRDT Implementation.

    Notes:
        Similar to LWW-Element-Set, except that it unique tags are used instead of timestamps.
        For each element, a list of add/remove tags are maintained.
        An element is added by adding a newly generated unique tag to the add-tag list for the element.
        Removing an element involves copying all the tags in it’s add-tag list to it's remove-tag list.
        An element is a member of the set iff there exists a tag in add-tag list which is not in remove-tag list.

    Attributes:
        A (list): List of elements added.
        R (list): List of elements removed.
        id (any_type): ID of the class object.
        orsetf (ORSetFunctions): ORSetFunctions object to access the static methods.
    """

    def __init__(self, id):
        self.A = []
        self.R = []
        self.id = id
        self.orsetf = ORSetFunctions()

    def add(self, elem, unique_tag):
        """
        The function to add the element.

        Args:
            elem (any_type): The element to be added.
            unique_tag (any_type): Tag to identify element.

        Note:
            'elem' is added to payload 'A'
        """

        self.A = self.orsetf.add(self.A, elem, unique_tag)

    def remove(self, elem):
        """
        The function to remove the element.

        Args:
            elem (any_type): The element to be removed.

        Note:
            'elem' is added to payload 'R'
        """

        self.R = self.orsetf.remove(self.A, self.R, elem)

    def query(self, elem):
        """
        The function to return True if element is present in the payload.

        Args:
            elem (any_type): The element to be searched for.

        Returns:
            bool: True if element's tags present in the payload 'A' but not in payload 'R', False otherwise.
        """

        if set(self.orsetf.query(elem, self.A)) - set(self.orsetf.query(elem, self.R)):
            return True
        return False

    def compare(self, orset):
        """
        The function to compare the payloads with the argument's payloads.

        Args:
            orset (ORSet): Object to be compared to.

        Note:
            Compares payload 'A' and payload 'R' of the objects

        Returns:
            bool: True if payloads of both objects are same, False otherwise.
        """

        return self.orsetf.compare(self.A, orset.A) and self.orsetf.compare(self.A, orset.A)

    def merge(self, orset):
        """
        The function to merge the payloads with the argument's payloads.

        Args:
            orset (ORSet): Object to be merged from.
        """

        # Merge payload 'A'
        self.A = self.orsetf.merge(self.A, orset.A)

        # Merge payload 'R'
        self.R = self.orsetf.merge(self.R, orset.R)

    def display(self):
        """
        The function to print the object's payloads.
        """

        # Display payload 'A'
        self.orsetf.display('A', self.A)

        # Display payload 'R'
        self.orsetf.display('R', self.R)
