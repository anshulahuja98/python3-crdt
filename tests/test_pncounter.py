import unittest
import uuid
import py3crdt
from py3crdt.pncounter import PNCounter
from py3crdt.node import Node


class TestPNCounter(unittest.TestCase):
    def setUp(self):
        # Create nodes
        self.node1 = Node(uuid.uuid4())
        self.node2 = Node(uuid.uuid4())

        # Create a PNCounter
        self.pn1 = PNCounter(uuid.uuid4())

        # Add nodes to pn1
        self.pn1.add_new_node(self.node1.id)
        self.pn1.add_new_node(self.node2.id)

        # Increment pn1 values for each node
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node1.id)
        self.pn1.inc(self.node2.id)
        self.pn1.inc(self.node2.id)
        self.pn1.inc(self.node2.id)

        # Decrement pn1 values for each node
        self.pn1.dec(self.node1.id)
        self.pn1.dec(self.node1.id)
        self.pn1.dec(self.node1.id)
        self.pn1.dec(self.node2.id)

        # Create another PNCounter
        self.pn2 = PNCounter(uuid.uuid4())

        # Add nodes to pn2
        self.pn2.add_new_node(self.node1.id)
        self.pn2.add_new_node(self.node2.id)

        # Increment pn2 values for each node
        self.pn2.inc(self.node1.id)
        self.pn2.inc(self.node2.id)
        self.pn2.inc(self.node2.id)
        self.pn2.inc(self.node2.id)

        # Decrement self.pn2 values for each node
        self.pn2.dec(self.node1.id)
        self.pn2.dec(self.node2.id)
        self.pn2.dec(self.node2.id)

    def test_merge(self):
        self.pn1.display("pn1")
        self.pn2.display("pn2")

        # Merge pn2 with pn1
        self.pn2.merge(self.pn1)
        # Merge pn1 with pn2
        self.pn1.merge(self.pn2)

        self.assertEqual(self.pn1.query(), self.pn2.query())


if __name__ == '__main__':
    unittest.main()
