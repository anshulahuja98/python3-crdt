# Import GSet
from .gset import GSet


class TwoPSet:
    """
    Two-Phase Set CRDT Implementation.

    Notes:
        A set in which elements can be added as well as removed. It combines two G-Sets namely “add” and “remove” set.
        For adding/removing an element, it is inserted in the “add”/“remove” set.
        An element is a member of the set if it is in the “add” set but not in the “remove” set.
        Query function returns whether the element is a member of the set or not.
        Hence, if an element is removed, query will never return True for that element, so it cannot be re-added.
        Merging involves union of the “add”/“remove” sets.

    Attributes:
        A (list): List of elements added.
        R (list): List of elements removed.
        id (any_type): ID of the class object.
    """

    def __init__(self, id):
        self.A = GSet(id)
        self.R = GSet(id)
        self.id = id

    def add(self, elem):
        """
        The function to add the element.

        Args:
            elem (any_type): The element to be added.

        Note:
            'elem' is added to payload 'A'
        """

        self.A.add(elem)

    def remove(self, elem):
        """
        The function to remove the element.

        Args:
            elem (any_type): The element to be removed.

        Note:
            'elem' is added to payload 'R'
        """

        self.R.add(elem)

    def query(self, elem):
        """
        The function to return True if element is present in the payload.

        Args:
            elem (any_type): The element to be searched for.

        Returns:
            bool: True if element's tags present in the payload 'A' but not in payload 'R', False otherwise.
        """

        return self.A.query(elem) and not self.R.query(elem)

    def compare(self, tps2):
        """
        The function to compare the payloads with the argument's payloads.

        Args:
            tps2 (TwoPSet): Object to be compared to.

        Note:
            Compares payload 'A' and payload 'R' of the objects

        Returns:
            bool: True if payloads of both objects are same, False otherwise.
        """

        return self.A.compare(tps2.A) and self.R.compare(tps2.R)

    def merge(self, tps2):
        """
        The function to merge the payloads with the argument's payloads.

        Args:
            tps2 (TwoPSet): Object to be merged from.
        """

        # Merge payload 'A'
        self.A.merge(tps2.A)

        # Merge payload 'R'
        self.R.merge(tps2.R)

    def display(self):
        """
        The function to print the object's payloads.
        """

        # Display payload 'A'
        print("A: ", end="")
        self.A.display()

        # Display payload 'R'
        print("R: ", end="")
        self.R.display()
