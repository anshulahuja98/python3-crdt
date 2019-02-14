import sys

sys.path.insert(0, sys.argv[1])

import uuid
from lww import LWWElementSet

# Create a LWWElementSet
lww1 = LWWElementSet(uuid.uuid4())

# Add nodes to lww1
lww1.add('a')
lww1.add('b')

# Create another LWWElementSet
lww2 = LWWElementSet(uuid.uuid4())

# Add nodes to lww2
lww2.add('b')
lww2.add('c')
lww2.add('d')

# Display counters
print("LWW1->")
lww1.display()
print("LWW2->")
lww2.display()

# Add nodes to lww1
lww1.remove('b')

# Add nodes to lww2
lww2.remove('b')
lww2.remove('c')

# Display counters
print("LWW1->")
lww1.display()
print("LWW2->")
lww2.display()

# Merge lww2 with lww1
print("Merging LWW2 with LWW1...")
lww2.merge(lww1)

# Display lww1
print("LWW2->")
lww2.display()

# Query lww1
print("Is 'a' in lww1: ", lww1.query('a'))
print("Is 'b' in lww1: ", lww1.query('b'))
print("Is 'e' in lww1: ", lww1.query('e'))

# Display counters
print("LWW1->")
lww1.display()
print("LWW2->")
lww2.display()

# Compare lww1 and lww2
print("Comparison: ", lww1.compare(lww2))
