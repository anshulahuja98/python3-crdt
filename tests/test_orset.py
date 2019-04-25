import unittest
import uuid
import py3crdt
from py3crdt.orset import ORSet


class TestORSet(unittest.TestCase):
    def setUp(self):
        # Create a ORSet
        self.orset1 = ORSet(uuid.uuid4())

        # Create another ORSet
        self.orset2 = ORSet(uuid.uuid4())

        # Add elements to orset1
        self.orset1.add('a', uuid.uuid4())
        self.orset1.add('b', uuid.uuid4())

        # Add elements to orset1
        self.orset2.add('b', uuid.uuid4())
        self.orset2.add('c', uuid.uuid4())
        self.orset2.add('d', uuid.uuid4())

    def test_elements_add_correctly_orset(self):
        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.orset1.R], [])
        self.assertEqual([_['elem'] for _ in self.orset2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset2.R], [])

    def test_querying_orset_without_removal_and_merging(self):
        # Check orset1 querying
        self.assertTrue(self.orset1.query('a'))
        self.assertTrue(self.orset1.query('b'))
        self.assertFalse(self.orset1.query('c'))
        self.assertFalse(self.orset1.query('d'))

        # Check orset2 querying
        self.assertFalse(self.orset2.query('a'))
        self.assertTrue(self.orset2.query('b'))
        self.assertTrue(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))

    def test_merging_orset_without_removal(self):
        # Check orset1 merging
        self.orset1.merge(self.orset2)
        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b', 'c', 'd'])
        for _ in self.orset1.A:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break
        self.assertEqual([_['elem'] for _ in self.orset1.R], [])

        # Check orset2 merging
        self.orset2.merge(self.orset1)
        self.assertEqual([_['elem'] for _ in self.orset2.A], ['a', 'b', 'c', 'd'])
        for _ in self.orset2.A:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break
        self.assertEqual([_['elem'] for _ in self.orset2.R], [])

        # Check if they are both equal
        self.assertEqual([_['elem'] for _ in self.orset1.A], [_['elem'] for _ in self.orset2.A])
        self.assertEqual([_['elem'] for _ in self.orset1.R], [_['elem'] for _ in self.orset2.R])

    def test_querying_orset_with_merging_without_removal(self):
        # Check orset2 merging
        self.orset2.merge(self.orset1)
        self.assertTrue(self.orset2.query('a'))
        self.assertTrue(self.orset2.query('b'))
        self.assertTrue(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))

        # Check orset1 merging
        self.orset1.merge(self.orset2)
        self.assertTrue(self.orset1.query('a'))
        self.assertTrue(self.orset1.query('b'))
        self.assertTrue(self.orset1.query('c'))
        self.assertTrue(self.orset1.query('d'))

    def test_elements_remove_correctly_orset(self):
        # Remove elements from orset1
        self.orset1.remove('b')

        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.orset1.R], ['b'])

        # Remove elements from orset2
        self.orset2.remove('b')
        self.orset2.remove('c')

        self.assertEqual([_['elem'] for _ in self.orset2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset2.R], ['b', 'c'])

    def test_querying_orset_without_merging_with_removal(self):
        # Remove elements from orset1
        self.orset1.remove('b')

        # Check orset1 querying
        self.assertTrue(self.orset1.query('a'))
        self.assertFalse(self.orset1.query('b'))
        self.assertFalse(self.orset1.query('c'))
        self.assertFalse(self.orset1.query('d'))

        # Remove elements from orset2
        self.orset2.remove('b')
        self.orset2.remove('c')

        # Check orset2 querying
        self.assertFalse(self.orset2.query('a'))
        self.assertFalse(self.orset2.query('b'))
        self.assertFalse(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))

    def test_merging_orset_with_removal(self):
        # Remove elements from orset1
        self.orset1.remove('b')

        # Remove elements from orset2
        self.orset2.remove('b')
        self.orset2.remove('c')

        # Check orset1 merging
        self.orset1.merge(self.orset2)
        self.assertEqual([_['elem'] for _ in self.orset1.A], ['a', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset1.R], ['b', 'c'])
        for _ in self.orset1.R:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break

        # Check orset2 merging
        self.orset2.merge(self.orset1)
        self.assertEqual([_['elem'] for _ in self.orset2.A], ['a', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.orset2.R], ['b', 'c'])
        for _ in self.orset2.R:
            if _['elem'] == 'b':
                self.assertEqual(len(_['tags']), 2)
                break

        # Check if they are both equal
        self.assertEqual([_['elem'] for _ in self.orset1.A], [_['elem'] for _ in self.orset2.A])
        self.assertEqual([_['elem'] for _ in self.orset1.R], [_['elem'] for _ in self.orset2.R])

    def test_querying_orset_with_merging_with_removal(self):
        # Remove elements from orset1
        self.orset1.remove('b')

        # Remove elements from orset2
        self.orset2.remove('b')
        self.orset2.remove('c')

        # Merge orset2 to orset1
        self.orset1.merge(self.orset2)

        # Merge orset1 to orset2
        self.orset2.merge(self.orset1)

        # Check orset1 querying
        self.assertTrue(self.orset1.query('a'))
        self.assertFalse(self.orset1.query('b'))
        self.assertFalse(self.orset1.query('c'))
        self.assertTrue(self.orset1.query('d'))

        # Check orset2 querying
        self.assertTrue(self.orset2.query('a'))
        self.assertFalse(self.orset2.query('b'))
        self.assertFalse(self.orset2.query('c'))
        self.assertTrue(self.orset2.query('d'))


if __name__ == '__main__':
    unittest.main()
