import sys

sys.path.insert(0, sys.argv[1])

import uuid
from gset import GSet

# Create a GSet
gs1 = GSet(uuid.uuid4())

# Add nodes to gs1
gs1.add('a')
gs1.add('b')

# Create another GSet
gs2 = GSet(uuid.uuid4())

# Add nodes to gs2
gs2.add('b')
gs2.add('c')
gs2.add('d')

# Display counters
print("GS1: ", end="")
gs1.display()
print("GS2: ", end="")
gs2.display()

# Merge gs2 with gs1
gs1.merge(gs2)

# Display gs1
print("GS1: ", end="")
gs1.display()

# Query gs1
print("Is 'a' in gs1: ", gs1.query('a'))
print("Is 'e' in gs1: ", gs1.query('e'))

# Compare gs1 and gs2
print(gs1.compare(gs2))
gs2.add('a')
gs1.display()
gs2.display()
print(gs1.compare(gs2))
