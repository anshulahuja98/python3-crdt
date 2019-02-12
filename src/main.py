from gcounter import GCounter
from node import Node
import uuid

# Create nodes
node1 = Node(uuid.uuid4())
node2 = Node(uuid.uuid4())

# Create a GCounter
gc1 = GCounter(uuid.uuid4())

# Add nodes to gc1
gc1.add_new_node(node1.id)
gc1.add_new_node(node2.id)

# Increment gc1 values for each node
gc1.inc(node1.id)
gc1.inc(node1.id)
gc1.inc(node2.id)

# Create another GCounter
gc2 = GCounter(uuid.uuid4())

# Add nodes to gc2
gc2.add_new_node(node1.id)
gc2.add_new_node(node2.id)

# Increment gc2 values for each node
gc2.inc(node1.id)
gc2.inc(node2.id)
gc2.inc(node2.id)
gc2.inc(node2.id)

# Display counters
gc1.display()
gc2.display()

# Merge gc2 with gc1
gc2.merge(gc1)
