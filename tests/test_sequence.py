import unittest
import uuid
import py3crdt
from py3crdt.sequence import Sequence
from datetime import datetime


class TestSequence(unittest.TestCase):
    def setUp(self):
        # Create a Sequence
        self.seq1 = Sequence(uuid.uuid4())

        # Create another Sequence
        self.seq2 = Sequence(uuid.uuid4())

        # Add elements to seq1
        self.id1a = datetime.timestamp(datetime.now())
        self.seq1.add('a', self.id1a)
        self.id1b = datetime.timestamp(datetime.now())
        self.seq1.add('b', self.id1b)

        # Add elements to seq2
        self.id2c = datetime.timestamp(datetime.now())
        self.seq2.add('c', self.id2c)
        self.id2b = datetime.timestamp(datetime.now())
        self.seq2.add('b', self.id2b)
        self.id2d = datetime.timestamp(datetime.now())
        self.seq2.add('d', self.id2d)

    def test_elements_add_correctly_sequence(self):
        self.assertEqual(self.seq1.get_seq(), "ab")
        self.assertEqual(self.seq2.get_seq(), "cbd")

    def test_querying_sequence_without_removal_and_merging(self):
        # Check seq1 querying
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertTrue(self.seq1.query(self.id1b))
        self.assertFalse(self.seq1.query(self.id2b))
        self.assertFalse(self.seq1.query(self.id2c))
        self.assertFalse(self.seq1.query(self.id2d))

        # Check seq2 querying
        self.assertFalse(self.seq2.query(self.id1a))
        self.assertFalse(self.seq2.query(self.id1b))
        self.assertTrue(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2b))
        self.assertTrue(self.seq2.query(self.id2d))

    def test_merging_sequence_without_removal(self):
        # Check seq1 merging
        self.seq1.merge(self.seq2)
        self.assertEqual(self.seq1.get_seq(), "abcbd")

        # Check seq2 merging
        self.seq2.merge(self.seq1)
        self.assertEqual(self.seq2.get_seq(), "abcbd")

        # Check if they are both equal
        self.assertEqual(self.seq1.get_seq(), self.seq2.get_seq())

    def test_querying_sequence_with_merging_without_removal(self):
        # Check seq2 merging
        self.seq2.merge(self.seq1)
        self.assertTrue(self.seq2.query(self.id1a))
        self.assertTrue(self.seq2.query(self.id1b))
        self.assertTrue(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2b))
        self.assertTrue(self.seq2.query(self.id2d))

        # Check seq1 merging
        self.seq1.merge(self.seq2)
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertTrue(self.seq1.query(self.id1b))
        self.assertTrue(self.seq1.query(self.id2b))
        self.assertTrue(self.seq1.query(self.id2c))
        self.assertTrue(self.seq1.query(self.id2d))

    def test_elements_remove_correctly_sequence(self):
        # Remove elements from seq1
        self.seq1.remove(self.id1b)

        self.assertEqual(self.seq1.get_seq(), "a")

        # Remove elements from seq2
        self.seq2.remove(self.id2b)
        self.seq2.remove(self.id2c)

        self.assertEqual(self.seq2.get_seq(), "d")

    def test_querying_sequence_without_merging_with_removal(self):
        # Remove elements from seq1
        self.seq1.remove(self.id1b)

        # Check seq1 querying
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertFalse(self.seq1.query(self.id1b))
        self.assertFalse(self.seq1.query(self.id2b))
        self.assertFalse(self.seq1.query(self.id2c))
        self.assertFalse(self.seq1.query(self.id2d))

        # Remove elements from seq2
        self.seq2.remove(self.id2b)
        self.seq2.remove(self.id2c)

        # Check seq2 querying
        self.assertFalse(self.seq2.query(self.id1a))
        self.assertFalse(self.seq2.query(self.id1b))
        self.assertFalse(self.seq2.query(self.id2b))
        self.assertFalse(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2d))

    def test_merging_sequence_with_removal(self):
        # Remove elements from seq1
        self.seq1.remove(self.id1b)

        # Remove elements from seq2
        self.seq2.remove(self.id2c)

        # Check seq1 merging
        self.seq1.merge(self.seq2)
        self.assertEqual(self.seq1.get_seq(), "abd")

        # Check seq2 merging
        self.seq2.merge(self.seq1)
        self.assertEqual(self.seq2.get_seq(), "abd")

        # Check if they are both equal
        self.assertEqual(self.seq2.get_seq(), self.seq2.get_seq())

    def test_querying_sequence_with_merging_with_removal(self):
        # Remove elements from seq1
        self.seq1.remove(self.id1b)

        # Remove elements from seq2
        self.seq2.remove(self.id2c)

        # Merge seq2 to seq1
        self.seq1.merge(self.seq2)

        # Merge seq1 to seq2
        self.seq2.merge(self.seq1)

        # Check seq1 querying
        self.assertTrue(self.seq1.query(self.id1a))
        self.assertFalse(self.seq1.query(self.id1b))
        self.assertTrue(self.seq1.query(self.id2b))
        self.assertFalse(self.seq1.query(self.id2c))
        self.assertTrue(self.seq1.query(self.id2d))

        # Check seq2 querying
        self.assertTrue(self.seq2.query(self.id1a))
        self.assertFalse(self.seq2.query(self.id1b))
        self.assertTrue(self.seq2.query(self.id2b))
        self.assertFalse(self.seq2.query(self.id2c))
        self.assertTrue(self.seq2.query(self.id2d))


if __name__ == '__main__':
    unittest.main()
