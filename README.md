# python3-crdt
A python library for CRDTs (Conflict-free Replicated Data types)

## Installation
You can get the library directly from PyPI:

```python
pip install python3-crdt
```

## Usage
If you have installed the python3-crdt package you can start using the crdts right away:
```python
from py3crdt.gset import GSet
gset1 = GSet(id=1)
gset2 = GSet(id=2)
gset1.add('a')
gset1.add('b')
gset1.display()
# ['a', 'b']   ----- Output
gset2.add('b')
gset2.add('c')
gset2.display()
# ['b', 'c']   ----- Output
gset1.merge(gset2)   
gset1.display()
# ['a', 'b', 'c']   ----- Output
gset2.merge(gset1)
gset2.display()
# ['a', 'b', 'c']   ----- Output
```

#### CRDTs deployed:-
- gcounter.GCounter
- pncounter.PNCounter
- gset.GSet
- twopset.TwoPSet
- lww.LWWElementSet
- orest.ORSet
- sequence.Sequence

## API
- add()
- remove()
- merge()
- display()
- query()
  
## Testing
Use following command to test packages
```python
python -m unittest tests.test_<package_name>
```  
## Intro to CRDTs
#### What are CRDTS?
CRDTs or Conflict-Free Replicated Data Types are data structures which eases the replication of data across multiple devices in a network. Any change/update is applied locally and then transmitted to other replicas. Each replica merges it’s local replica with the incoming change/update. Inconsistencies might arise during merging but CRDTs mathematically guarantees that the replicas will converge eventually if all the changes/updates are executed by each replica. 

#### Types of CRDTs

##### Operation-based CRDTs
In these CRDTs, change/update operations are transmitted to other replicas. Each replica receives the operations and apply the operations to its local state. These are also known as CmRDT (Commutative Replicated Data Type) because the operations are commutative hence, order of sending operations does not matter. The resulting state will eventually be the same. But the operations are not idempotent hence, it must be ensured that no operation is duplicated during transmission.

##### State-based CRDTs
In these CRDTs, full state is transmitted to other replicas. Replicas receive the state and merge it with the local state. Merge function is commutative as CmRDTs but is also idempotent and associative. These are also known as CvRDT (Convergent Replicated Data Type) because in  every transmission merging of states occur, which eventually results in all replicas converging to the same state.

##### Delta-state CRDTs
In these CRDTs, instead of full state, only recently applied changes are transmitted to other replicas. It is just an optimised State-based CRDT.

#### Comparison between CmRDTs & CvRDTs
CmRDTs increases transmission mechanism workload but consumes less bandwidth than CvRDTs when number of transactions is small compared to size of the internal state. However, since the CvRDT merge function is associative merging the state produces all previous updates to that replica and since it is idempotent, the states can be transmitted multiple number of times but resulting into the same state.

## CRDTs deployed in this library

#### G-Counter (Grow-only Counter)
It implements an array of nodes where the value of array works as a counter. The value of array is sum of the values of the nodes in the array. Each node is assigned an ID equivalent to the index of the node in the array. The array is an equivalent for a cluster of nodes. Updating involves each node incrementing its own index value in the array. Merging occurs by taking the maximum of every node value in the cluster. Comparison function is included to verify the increments. Internal state is monotonically increased by application of each update function according to the compare function.

#### PN-Counter (Positive-Negative Counter)
This counter supports both increment and decrement operations. It combines two G-Counters namely “P” (for incrementing) and “N” (for decrementing) counter. The value of the counter is the value of the P counter minus the value of the N counter. Merging involves merging the P and N counter independently.

#### G-Set (Grow-only Set)
This involves creating a set of elements where elements can only be added and once and element is added, it cannot be removed. Merging returns union of the two G-Sets.

#### 2P-Set (Two-Phase Set)
It involves creating a set in which elements can be added as well as removed. Similar to PN-Counter, it combines two G-Sets namely “add” and “remove” set. For adding/removing an element, it is inserted in the “add”/“remove” set. An element is a member of the set if it is in the “add” set but not in the “remove” set. Query function returns whether the element is a member of the set or not. Hence, if an element is removed, query will never return True for that element, so it cannot be re-added. Merging involves union of the “add”/“remove” sets.

#### LWW-Element-Set (Last-Write-Wins-Element-Set)
Similar to 2P-Set except each element is added/removed with a timestamp. An element is a member of the set if it is in the “add” set but not in the “remove” set, or if it is in both the “add” and “remove” set then timestamp in “remove” set should be less than that of the latest timestamp in “add” set. “Bias” comes into play, if timestamps are equal which can be towards “add” or “remove”. In this set, an element can be reinserted after being removed and thus, it has an advantage over 2P-Set.

#### OR-Set (Observed-Removed Set)
Similar to LWW-Element-Set, except that it unique tags are used instead of timestamps. For each element, a list of add/remove tags are maintained. An element is added by adding a newly generated unique tag to the add-tag list for the element. Removing an element involves copying all the tags in it’s add-tag list to it's remove-tag list. An element is a member of the set iff there exists a tag in add-tag list which is not in remove-tag list.

#### Sequence CRDTs
It involves an ordered set, list or a sequence of elements. This CRDT can be build on top of other Set based CRDTs by sorting them on some basis. 
We have used this CRDT to build a Collaborative Code/Text Editor.
