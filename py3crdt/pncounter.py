# Import PNCounter
from .gcounter import GCounter


class PNCounter:
    """
    Positive-Negative Counter CRDT Implementation.

    Notes:
        This counter supports both increment and decrement operations.
        It combines two G-Counters namely “P” (for incrementing) and “N” (for decrementing) counter.
        The value of the counter is the value of the P counter minus the value of the N counter.
        Merging involves merging the P and N counter independently.

    Attributes:
        P (PNCounter): PNCounter object to increment counter.
        N (PNCounter): PNCounter object to deceremnt counter.
        id (any_type): ID of the class object.
    """

    def __init__(self, id):
        self.P = PNCounter(id)
        self.N = PNCounter(id)
        self.id = id

    def add_new_node(self, key):
        """
        The function to add the key to the payload.

        Args:
            key (any_type): The key of the node to be added.

        Note:
            Adds the key to both gcounter objects P and N.
        """

        self.P.add_new_node(key)
        self.N.add_new_node(key)

    def inc(self, key):
        """
        The function to increment the key's value in payload.

        Args:
            key (any_type): The key of the node to be added.

        Note:
            Increments the value of gcounter object P.
        """

        self.P.inc(key)

    def dec(self, key):
        """
        The function to decrement the key's value in payload.

        Args:
            key (any_type): The key of the node to be added.

        Note:
            Increments the value of gcounter object N.
        """

        self.N.inc(key)

    def query(self):
        """
        The function to return the effective counter value.

        Note:
            Returns the difference between gcounter object P and N.
        """

        return self.P.query() - self.N.query()

    def compare(self, pnc2):
        """
        The function to compare the payload value with argument's object's payload value.

        Args:
            pnc2 (PNCounter): The PNCounter object to be compared.

        Returns:
            bool: True if effective payload value is greater than that of argument's object, False otherwise.
        """

        return self.P.compare(pnc2.P) and self.N.compare(pnc2.N)

    def merge(self, pnc2):
        """
        The function to merge the PNCounter object's payload with the argument's payload.

        Args:
            pnc2 (PNCounter): The PNCounter object to be compared.

        Note:
            Merging occurs on the basis of the max value from the payloads for each key.
            Merges both objects P and N.
        """

        self.P.merge(pnc2.P)
        self.N.merge(pnc2.N)

    def display(self, name):
        """
        The function to print the object's payloads.
        """

        # Display object P
        print("{}.P: ".format(name), end="")
        self.P.display()

        # Display object N
        print("{}.N: ".format(name), end="")
        self.N.display()
