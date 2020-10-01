import unittest
import uuid
import py3crdt
from py3crdt.gset import GSet


class TestLWW(unittest.TestCase):
    def setUp(self):
        # Create a GSet
        self.gset1 = GSet(uuid.uuid4())

        # Create another GSet
        self.gset2 = GSet(uuid.uuid4())

        # Add elements to gset1
        self.gset1.add('a')
        self.gset1.add('b')

        # Add elements to gset1
        self.gset2.add('b')
        self.gset2.add('c')
        self.gset2.add('d')

    def test_elements_add_correctly_gset(self):
        self.assertEqual(self.gset1.payload, ['a', 'b'])
        self.assertEqual(self.gset2.payload, ['b', 'c', 'd'])

    def test_querying_gset_without_merging(self):
        # Check gset1 querying
        self.assertTrue(self.gset1.query('a'))
        self.assertTrue(self.gset1.query('b'))
        self.assertFalse(self.gset1.query('c'))
        self.assertFalse(self.gset1.query('d'))

        # Check gset2 querying
        self.assertFalse(self.gset2.query('a'))
        self.assertTrue(self.gset2.query('b'))
        self.assertTrue(self.gset2.query('c'))
        self.assertTrue(self.gset2.query('d'))

    def test_merging_gset(self):
        # Check gset1 merging
        self.gset1.merge(self.gset2)
        self.assertEqual(self.gset1.payload, ['a', 'b', 'c', 'd'])

        # Check gset2 merging
        self.gset2.merge(self.gset1)
        self.assertEqual(self.gset2.payload, ['a', 'b', 'c', 'd'])

        # Check if they are both equal
        self.assertEqual(self.gset1.payload, self.gset2.payload)

    def test_querying_gset_with_merging(self):
        # Check gset2 merging
        self.gset2.merge(self.gset1)
        self.assertTrue(self.gset2.query('a'))
        self.assertTrue(self.gset2.query('b'))
        self.assertTrue(self.gset2.query('c'))
        self.assertTrue(self.gset2.query('d'))

        # Check gset1 merging
        self.gset1.merge(self.gset2)
        self.assertTrue(self.gset1.query('a'))
        self.assertTrue(self.gset1.query('b'))
        self.assertTrue(self.gset1.query('c'))
        self.assertTrue(self.gset1.query('d'))


if __name__ == '__main__':
    unittest.main()
