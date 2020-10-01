import unittest
import uuid
import py3crdt
from py3crdt.lww import LWWElementSet as LWWSet


class TestLWW(unittest.TestCase):
    def setUp(self):
        # Create a LWWSet
        self.lww1 = LWWSet(uuid.uuid4())

        # Create another LWWSet
        self.lww2 = LWWSet(uuid.uuid4())

        # Add elements to lww1
        self.lww1.add('a')
        self.lww1.add('b')

        # Add elements to lww1
        self.lww2.add('b')
        self.lww2.add('c')
        self.lww2.add('d')

    def test_elements_add_correctly_lww_set(self):
        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [])
        self.assertEqual([_['elem'] for _ in self.lww2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], [])

    def test_querying_lww_set_without_removal_and_merging(self):
        # Check lww1 querying
        self.assertTrue(self.lww1.query('a'))
        self.assertTrue(self.lww1.query('b'))
        self.assertFalse(self.lww1.query('c'))
        self.assertFalse(self.lww1.query('d'))

        # Check lww2 querying
        self.assertFalse(self.lww2.query('a'))
        self.assertTrue(self.lww2.query('b'))
        self.assertTrue(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))

    def test_merging_lww_set_without_removal(self):
        # Check lww1 merging
        self.lww1.merge(self.lww2)
        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [])

        # Check lww2 merging
        self.lww2.merge(self.lww1)
        self.assertEqual([_['elem'] for _ in self.lww2.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], [])

        # Check if they are both equal
        self.assertEqual([_['elem'] for _ in self.lww1.A], [_['elem'] for _ in self.lww2.A])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [_['elem'] for _ in self.lww2.R])

    def test_querying_lww_set_with_merging_without_removal(self):
        # Check lww2 merging
        self.lww2.merge(self.lww1)
        self.assertTrue(self.lww2.query('a'))
        self.assertTrue(self.lww2.query('b'))
        self.assertTrue(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))

        # Check lww1 merging
        self.lww1.merge(self.lww2)
        self.assertTrue(self.lww1.query('a'))
        self.assertTrue(self.lww1.query('b'))
        self.assertTrue(self.lww1.query('c'))
        self.assertTrue(self.lww1.query('d'))

    def test_elements_remove_correctly_lww_set(self):
        # Remove elements from lww1
        self.lww1.remove('b')

        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], ['b'])

        # Remove elements from lww2
        self.lww2.remove('b')
        self.lww2.remove('c')

        self.assertEqual([_['elem'] for _ in self.lww2.A], ['b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], ['b', 'c'])

    def test_querying_lww_set_without_merging_with_removal(self):
        # Remove elements from lww1
        self.lww1.remove('b')

        # Check lww1 querying
        self.assertTrue(self.lww1.query('a'))
        self.assertFalse(self.lww1.query('b'))
        self.assertFalse(self.lww1.query('c'))
        self.assertFalse(self.lww1.query('d'))

        # Remove elements from lww2
        self.lww2.remove('b')
        self.lww2.remove('c')

        # Check lww2 querying
        self.assertFalse(self.lww2.query('a'))
        self.assertFalse(self.lww2.query('b'))
        self.assertFalse(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))

    def test_merging_lww_set_with_removal(self):
        # Remove elements from lww1
        self.lww1.remove('b')

        # Remove elements from lww2
        self.lww2.remove('b')
        self.lww2.remove('c')

        # Check lww1 merging
        self.lww1.merge(self.lww2)
        self.assertEqual([_['elem'] for _ in self.lww1.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww1.R], ['b', 'b', 'c'])

        # Check lww2 merging
        self.lww2.merge(self.lww1)
        self.assertEqual([_['elem'] for _ in self.lww2.A], ['a', 'b', 'b', 'c', 'd'])
        self.assertEqual([_['elem'] for _ in self.lww2.R], ['b', 'b', 'c'])

        # Check if they are both equal
        self.assertEqual([_['elem'] for _ in self.lww1.A], [_['elem'] for _ in self.lww2.A])
        self.assertEqual([_['elem'] for _ in self.lww1.R], [_['elem'] for _ in self.lww2.R])

    def test_querying_lww_set_with_merging_with_removal(self):
        # Remove elements from lww1
        self.lww1.remove('b')

        # Remove elements from lww2
        self.lww2.remove('b')
        self.lww2.remove('c')

        # Merge lww2 to lww1
        self.lww1.merge(self.lww2)

        # Merge lww1 to lww2
        self.lww2.merge(self.lww1)

        # Check lww1 querying
        self.assertTrue(self.lww1.query('a'))
        self.assertFalse(self.lww1.query('b'))
        self.assertFalse(self.lww1.query('c'))
        self.assertTrue(self.lww1.query('d'))

        # Check lww2 querying
        self.assertTrue(self.lww2.query('a'))
        self.assertFalse(self.lww2.query('b'))
        self.assertFalse(self.lww2.query('c'))
        self.assertTrue(self.lww2.query('d'))


if __name__ == '__main__':
    unittest.main()
