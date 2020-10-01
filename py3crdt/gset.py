class GSet:
    """
    Grow Only Set CRDT Implementation.

    Notes:
        A set of elements where elements can only be added and once an element is added, it cannot be removed.
        Merging returns union of the two G-Sets.

    Attributes:
        payload (list): List of elements.
        id (any_type): ID of the class object.
    """

    def __init__(self, id):
        self.payload = []
        self.id = id

    def add(self, elem):
        """
        The function to add the element to the payload.

        Args:
            elem (any_type): The element to be added.
        """

        # Append the element to the payload.
        self.payload.append(elem)

        # Sort the payload.
        self.payload.sort()

    def query(self, elem):
        """
        The function to return True if element is present in the payload.

        Args:
            elem (any_type): The element to be searched for.

        Returns:
            bool: True if element is present in the payload, False otherwise.
        """

        return elem in self.payload

    def compare(self, gs2):
        """
        The function to compare two GSet objects.

        Args:
            gs2 (GSet): The GSet object to be compared.

        Returns:
            bool: True if payloads of both objects are same, False otherwise.
        """

        for elem in self.payload:
            if elem not in gs2.payload:
                return False
        return True

    def merge(self, gs2):
        """
        The function to merge the GSet object's payload with the argument's payload.

        Args:
            gs2 (GSet): The GSet object to be compared.
        """

        # Append the elements of argument's payload to the object's payload.
        for elem in gs2.payload:
            if elem not in self.payload:
                self.payload.append(elem)

        # Sort the payload.
        self.payload.sort()

    def display(self):
        """
        The function to print the object's payload.
        """

        print(self.payload)
