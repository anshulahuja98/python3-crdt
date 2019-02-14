import set_sys_path
import uuid
from pncounter import PNCounter
from node import Node

# Create nodes
node1 = Node(uuid.uuid4())
node2 = Node(uuid.uuid4())

# Create a PNCounter
pn1 = PNCounter(uuid.uuid4())

# Add nodes to pn1
pn1.add_new_node(node1.id)
pn1.add_new_node(node2.id)

# Increment pn1 values for each node
pn1.inc(node1.id)
pn1.inc(node1.id)
pn1.inc(node1.id)
pn1.inc(node1.id)
pn1.inc(node2.id)
pn1.inc(node2.id)
pn1.inc(node2.id)

# Decrement pn1 values for each node
pn1.dec(node1.id)
pn1.dec(node1.id)
pn1.dec(node1.id)
pn1.dec(node2.id)

# Create another PNCounter
pn2 = PNCounter(uuid.uuid4())

# Add nodes to pn2
pn2.add_new_node(node1.id)
pn2.add_new_node(node2.id)

# Increment pn2 values for each node
pn2.inc(node1.id)
pn2.inc(node2.id)
pn2.inc(node2.id)
pn2.inc(node2.id)

# Decrement pn2 values for each node
pn2.dec(node1.id)
pn2.dec(node2.id)
pn2.dec(node2.id)

# Display counters
pn1.display("pn1")
pn2.display("pn2")

# Query Values
print("pn1 Value: ", pn1.query())
print("pn2 Value: ", pn2.query())

# Merge pn2 with pn1
pn2.merge(pn1)

# Display counter2
pn2.display("pn2")

# Query Value
print("pn2 Value: ", pn2.query())
