import unittest
import uuid
import py3crdt
from py3crdt.gcounter import GCounter
from py3crdt.node import Node


class TestGCounter(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(uuid.uuid4())
        self.node2 = Node(uuid.uuid4())

        # Create a GCounter
        self.gc1 = GCounter(uuid.uuid4())

        # Add nodes to gc1
        self.gc1.add_new_node(self.node1.id)
        self.gc1.add_new_node(self.node2.id)

        # Create another GCounter
        self.gc2 = GCounter(uuid.uuid4())
        # Add nodes to gc2
        self.gc2.add_new_node(self.node1.id)
        self.gc2.add_new_node(self.node2.id)

        # Increment gc1 values for each node
        self.gc1.inc(self.node1.id)
        self.gc1.inc(self.node1.id)
        self.gc1.inc(self.node2.id)
        # Increment gc2 values for each node
        self.gc2.inc(self.node1.id)
        self.gc2.inc(self.node2.id)
        self.gc2.inc(self.node2.id)
        self.gc2.inc(self.node2.id)

    def test_check_increment(self):
        self.assertEqual(self.gc1.payload[self.node1.id], 2)
        self.assertEqual(self.gc1.payload[self.node2.id], 1)
        self.assertEqual(self.gc2.payload[self.node1.id], 1)
        self.assertEqual(self.gc2.payload[self.node2.id], 3)

    def test_merging_gcounters(self):
        # Check gc2 merging
        self.gc2.merge(self.gc1)
        self.assertEqual(self.gc2.payload[self.node1.id], 2)
        self.assertEqual(self.gc2.payload[self.node2.id], 3)
        # Check gc1 merging
        self.gc1.merge(self.gc2)
        self.assertEqual(self.gc1.payload[self.node1.id], 2)
        self.assertEqual(self.gc1.payload[self.node2.id], 3)
        # Check if they are both equal
        self.assertEqual(self.gc1.payload, self.gc2.payload)

if __name__ == '__main__':
    unittest.main()
