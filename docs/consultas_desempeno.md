# Performance Queries

This page describes the query implementations in `Escenario` and the scope of their counters. Let `n` be the number of active AVL events, `a` the number of archived events, `V = n + a`, `h` the AVL height, and `k` the number of results or matched costly events as applicable.

## Query behavior

- `consultarPrimerosPendientes(k)` requires a positive integer and visits keys in descending order (right, node, left), stopping when it finds `k` pending events or exhausts the tree. Since review state is not part of the key, the search cannot prune a subtree based on state. Worst case: `O(n)` time and up to `O(h + k)` stack/result space.
- `consultarPorMagnitud(minimo, maximo)` uses inclusive bounds. It performs a key-range search for each of the three priority values. Within a fixed priority, magnitude is ordered by the composite key, so ranges can use tree bounds. Across all priorities, the worst case is `O(n)` time and `O(n)` result space.
- `consultarPorProfundidadYFechas(limite, inicio, fin)` uses inclusive depth and UTC date bounds. Neither attribute is in the key, so it scans all active nodes: `O(n)` time and up to `O(n)` result space.
- `consultarAsociaciones(id)` checks active and archived events against each other to build candidate and selected-reference mappings, then finds events that selected the queried event. Its nested comparisons take `O(V^2)` time in the worst case and the temporary candidate mappings can use `O(V^2)` space. The returned `nodos_avl_examinados` counts the initial active-AVL traversal, not the pairwise comparisons.
- `consultarEventosCostosos()` first traverses the AVL to find priority-3 events below the `L` depth threshold, then searches by key for each match. Its worst-case time is `O(n + kh)` and its result space is `O(k)`. The reported traversal counter and per-result search counters are separate; the traversal total does not sum all later key searches.

## AVL/BST insertion-order comparison

`compararOrdenesInsercion()` rebuilds both trees from the same active events for each supplied order. If no orders are supplied, it compares ascending and descending key order. It reports each tree's height and leaf count and counts node visits when searching every existing key. A BST built from sorted keys can degrade to `O(n)` height and `O(n^2)` aggregate search visits; the AVL maintains `O(log n)` height and `O(n log n)` aggregate search visits.

## Interpreting counters

The counter names describe visits recorded by a specific traversal or search, not elapsed time and not necessarily every operation performed by a high-level query. Historical list scans, candidate-pair comparisons, sorting, and other uninstrumented work are excluded unless a query explicitly returns a separate counter for them. This keeps structural counts useful, but they should not be treated as complete operation counts or wall-clock benchmarks.
