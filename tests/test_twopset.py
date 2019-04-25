import unittest
import uuid
import py3crdt
from py3crdt.twopset import TwoPSet


class TestLWW(unittest.TestCase):
    def setUp(self):
        # Create a TwoPSet
        self.twopset1 = TwoPSet(uuid.uuid4())

        # Create another TwoPSet
        self.twopset2 = TwoPSet(uuid.uuid4())

        # Add elements to twopset1
        self.twopset1.add('a')
        self.twopset1.add('b')

        # Add elements to twopset1
        self.twopset2.add('b')
        self.twopset2.add('c')
        self.twopset2.add('d')

    def test_elements_add_correctly_twopset(self):
        self.assertEqual(self.twopset1.A.payload, ['a', 'b'])
        self.assertEqual(self.twopset1.R.payload, [])
        self.assertEqual(self.twopset2.A.payload, ['b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, [])

    def test_querying_twopset_without_removal_and_merging(self):
        # Check twopset1 querying
        self.assertTrue(self.twopset1.query('a'))
        self.assertTrue(self.twopset1.query('b'))
        self.assertFalse(self.twopset1.query('c'))
        self.assertFalse(self.twopset1.query('d'))

        # Check twopset2 querying
        self.assertFalse(self.twopset2.query('a'))
        self.assertTrue(self.twopset2.query('b'))
        self.assertTrue(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))

    def test_merging_twopset_without_removal(self):
        # Check twopset1 merging
        self.twopset1.merge(self.twopset2)
        self.assertEqual(self.twopset1.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset1.R.payload, [])

        # Check twopset2 merging
        self.twopset2.merge(self.twopset1)
        self.assertEqual(self.twopset2.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, [])

        # Check if they are both equal
        self.assertEqual(self.twopset1.A.payload, self.twopset2.A.payload)
        self.assertEqual(self.twopset1.R.payload, self.twopset2.R.payload)

    def test_querying_twopset_with_merging_without_removal(self):
        # Check twopset2 merging
        self.twopset2.merge(self.twopset1)
        self.assertTrue(self.twopset2.query('a'))
        self.assertTrue(self.twopset2.query('b'))
        self.assertTrue(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))

        # Check twopset1 merging
        self.twopset1.merge(self.twopset2)
        self.assertTrue(self.twopset1.query('a'))
        self.assertTrue(self.twopset1.query('b'))
        self.assertTrue(self.twopset1.query('c'))
        self.assertTrue(self.twopset1.query('d'))

    def test_elements_remove_correctly_twopset(self):
        # Remove elements from twopset1
        self.twopset1.remove('b')

        self.assertEqual(self.twopset1.A.payload, ['a', 'b'])
        self.assertEqual(self.twopset1.R.payload, ['b'])

        # Remove elements from twopset2
        self.twopset2.remove('b')
        self.twopset2.remove('c')

        self.assertEqual(self.twopset2.A.payload, ['b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, ['b', 'c'])

    def test_querying_twopset_without_merging_with_removal(self):
        # Remove elements from twopset1
        self.twopset1.remove('b')

        # Check twopset1 querying
        self.assertTrue(self.twopset1.query('a'))
        self.assertFalse(self.twopset1.query('b'))
        self.assertFalse(self.twopset1.query('c'))
        self.assertFalse(self.twopset1.query('d'))

        # Remove elements from twopset2
        self.twopset2.remove('b')
        self.twopset2.remove('c')

        # Check twopset2 querying
        self.assertFalse(self.twopset2.query('a'))
        self.assertFalse(self.twopset2.query('b'))
        self.assertFalse(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))

    def test_merging_twopset_with_removal(self):
        # Remove elements from twopset1
        self.twopset1.remove('b')

        # Remove elements from twopset2
        self.twopset2.remove('b')
        self.twopset2.remove('c')

        # Check twopset1 merging
        self.twopset1.merge(self.twopset2)
        self.assertEqual(self.twopset1.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset1.R.payload, ['b', 'c'])

        # Check twopset2 merging
        self.twopset2.merge(self.twopset1)
        self.assertEqual(self.twopset2.A.payload, ['a', 'b', 'c', 'd'])
        self.assertEqual(self.twopset2.R.payload, ['b', 'c'])

        # Check if they are both equal
        self.assertEqual(self.twopset1.A.payload, self.twopset2.A.payload)
        self.assertEqual(self.twopset1.R.payload, self.twopset2.R.payload)

    def test_querying_twopset_with_merging_with_removal(self):
        # Remove elements from twopset1
        self.twopset1.remove('b')

        # Remove elements from twopset2
        self.twopset2.remove('b')
        self.twopset2.remove('c')

        # Merge twopset2 to twopset1
        self.twopset1.merge(self.twopset2)

        # Merge twopset1 to twopset2
        self.twopset2.merge(self.twopset1)

        # Check twopset1 querying
        self.assertTrue(self.twopset1.query('a'))
        self.assertFalse(self.twopset1.query('b'))
        self.assertFalse(self.twopset1.query('c'))
        self.assertTrue(self.twopset1.query('d'))

        # Check twopset2 querying
        self.assertTrue(self.twopset2.query('a'))
        self.assertFalse(self.twopset2.query('b'))
        self.assertFalse(self.twopset2.query('c'))
        self.assertTrue(self.twopset2.query('d'))


if __name__ == '__main__':
    unittest.main()
