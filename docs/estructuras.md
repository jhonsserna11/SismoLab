# Data Structures

SismoLab stores active events in an AVL tree and mirrors them in a regular binary search tree (BST) for comparison. Implementations are in `src/structures/`.

## `Key`

File: `src/structures/Nodo.py`

A `Key` orders an event by the tuple `(priority, magnitude, event_id)`. Priority is compared first, magnitude second, and the ID breaks ties, producing deterministic ordering.

## `Nodo`

File: `src/structures/Nodo.py`

A node contains its `key`, the associated `evento`, left and right child references (`izq`, `der`), and stored `altura`. `esHoja()` identifies nodes with no children. Empty children have height -1, so a leaf has height 0.

## `Avl`

File: `src/structures/Avl.py`

`Avl` is the main active-event index. It recalculates heights and balance factors after insertions and deletions. When a node becomes unbalanced, it applies one of the standard rotations:

- LL: right rotation.
- RR: left rotation.
- LR: left rotation on the left child, then right rotation.
- RL: right rotation on the right child, then left rotation.

Important operations include `insertar`, `eliminar`, `encontrarNodo`, range and counted searches, traversals, `verificarEstructura`, and `recuperar`. `verificarEstructura` checks keys, event references, duplicate/cyclic nodes, stored heights, and balance.

The AVL also records rotation and case counters such as `casos_LL`, `casos_RR`, `casos_LR`, `casos_RL`, `giros_izquierda`, and `giros_derecha`. Query methods may return `nodos_avl_examinados` or related visit counts; see [performance queries](consultas_desempeno.md) for what those counts include.

## `Bst`

File: `src/structures/Bst.py`

`Bst` follows the same key ordering but does not rebalance. It supports insertion, lookup, deletion, traversals, height, node count, and depth queries. Ordered insertions can produce a tree with height proportional to the number of events, whereas the AVL maintains logarithmic height.

## Shared use

When a new event is created, `Escenario` builds one key and inserts the event into both trees. Corrections that change the key remove the previous key and insert the updated one in both structures. The AVL is authoritative for operational queries; the BST is used for comparison and synchronization checks.
