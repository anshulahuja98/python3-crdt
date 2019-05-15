class GCounter:
    """
    Grow Only Counter CRDT Implementation.

    Notes:
        It implements an array of nodes where the value of array works as a counter.
        The value of array is sum of the values of the nodes in the array.
        Each node is assigned an ID equivalent to the index of the node in the array.
        The array is an equivalent for a cluster of nodes.
        Updating involves each node incrementing its own index value in the array.
        Merging occurs by taking the maximum of every node value in the cluster.
        Comparison function is included to verify the increments.
        Internal state is monotonically increased by application of each update function according to compare function.

    Attributes:
        payload (dict): Dict of node_key : node_value.
        id (any_type): ID of the class object.
    """

    def __init__(self, id):
        self.payload = {}
        self.id = id

    def add_new_node(self, key):
        """
        The function to add the key to the payload.

        Args:
            key (any_type): The key of the node to be added.

        Note:
            Initialize the key's value to 0
        """

        self.payload[key] = 0

    def inc(self, key):
        """
        The function to increment the key's value in payload.

        Args:
            key (any_type): The key of the node to be added.
        """

        try:
            self.payload[key] += 1
        except Exception as e:
            print("{}".format(e))

    def query(self):
        """
        The function to return sum of the payload values.

        Returns:
            int: Sum of the payload values.
        """

        return sum(self.payload.values())

    def compare(self, gc2):
        """
        The function to compare the payload value with argument's object's payload value.

        Args:
            gc2 (GCounter): The GCounter object to be compared.

        Returns:
            bool: True if sum of payload values is greater than that of argument's object, False otherwise.
        """

        for key in self.payload:
            if self.payload[key] > gc2.payload[key]:
                return False

    def merge(self, gc2):
        """
        The function to merge the GCounter object's payload with the argument's payload.

        Args:
            gc2 (GCounter): The GCounter object to be compared.

        Note:
            Merging occurs on the basis of the max value from the payloads for each key.
        """

        new_payload = {key: 0 for key in self.payload}
        for key in self.payload:
            new_payload[key] = max(self.payload[key], gc2.payload[key])
        self.payload = new_payload

    def display(self):
        """
        The function to print the object's payload.
        """

        print(self.payload.values())
