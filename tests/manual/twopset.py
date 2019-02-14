import sys

sys.path.insert(0, sys.argv[1])

import uuid
from twopset import TwoPSet

# Create a TwoPSet
tps1 = TwoPSet(uuid.uuid4())

# Add nodes to tps1
tps1.add('a')
tps1.add('b')

# Create another TwoPSet
tps2 = TwoPSet(uuid.uuid4())

# Add nodes to tps2
tps2.add('b')
tps2.add('c')
tps2.add('d')

# Display counters
print("TPS1->")
tps1.display()
print("TPS2->")
tps2.display()

# Add nodes to tps1
tps1.remove('b')

# Add nodes to tps2
tps2.remove('b')
tps2.remove('c')

# Display counters
print("TPS1->")
tps1.display()
print("TPS2->")
tps2.display()

# Merge tps2 with tps1
print("Merging TPS2 with TPS1...")
tps2.merge(tps1)

# Display tps1
print("TPS2->")
tps2.display()

# Query tps1
print("Is 'a' in tps1: ", tps1.query('a'))
print("Is 'b' in tps1: ", tps1.query('b'))
print("Is 'e' in tps1: ", tps1.query('e'))

# Compare tps1 and tps2
print("Comparison: ", tps1.compare(tps2))
# Display counters
print("TPS1->")
tps1.display()
print("TPS2->")
tps2.display()
print("Comparison: ", tps1.compare(tps2))
