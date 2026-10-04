# Scenario Logic and Persistence

`src/logic/Escenario.py` coordinates the domain models, tree structures, event workflows, queries, and undo behavior. `src/logic/Persistencia.py` implements JSON serialization and validation.

## Scenario state

An `Escenario` owns the active-event AVL and BST, zones, stations, archived events (`historico`), deleted IDs (`eliminados`), queued reports, simulation clock, parameters `W`, `R`, `L`, and `T`, stress-mode flag, cumulative metrics, and undo stack.

- `W`: maximum time interval used for candidate association, in hours.
- `R`: maximum epicenter distance for candidate association.
- `L`: node-depth threshold used by the costly-event indicator.
- `T`: minimum event age used to determine archive eligibility, in hours.

The scenario clock can be advanced with `avanzarReloj(horas)`. Parameter-update methods validate positive values and save the previous state before changing a parameter.

## Creating and correcting events

`crearEvento(...)` checks ID uniqueness and station references, creates a validated `Evento`, saves an undo snapshot, calculates priority, builds a `Key`, and inserts the event into both trees. IDs are checked against active, archived, and deleted records.

A correction creates a new event revision and recalculates its key. If the key changes, the previous entry is removed and the corrected event is reinserted in both trees; otherwise, the existing tree nodes are updated. Event state changes and other mutations can be undone through `deshacer()`.

## Associations and reports

Candidate search compares events against the `W` and `R` limits and the magnitude/time rules in `Evento.esCandidato()`. Candidate selection prefers greater magnitude, then the closer preceding event in time, then the smaller ID. Archived events may participate in association checks.

Reports can be queued in `cola_reportes` and consumed in order. `procesarReporte()` validates report data and station references, then handles confirmations, accepted corrections, outdated or invalid reports, conflicts, new events, and archived-event reactivation. Scenario metrics track accepted corrections, discarded reports, conflicts, mass archives, and archived-event counts.

## Queries and metrics

The scenario exposes event lookup, the first `k` pending events, magnitude ranges, depth/date filtering, association details, costly-event indicators, and AVL/BST insertion-order comparisons. `obtenerIndicadores()` combines active/archive totals, AVL height and traversals, priority groups, pending events, costly events, and cumulative tree/scenario metrics.

All query implementations return the fields defined by their contracts, including visit counts where available. A visit counter only covers the AVL traversal or search explicitly instrumented by that query; it does not necessarily include historical scans, nested event comparisons, or every auxiliary operation. See [performance queries](consultas_desempeno.md).

## Archiving and recovery

A subtree is eligible for archiving only when every event in it has priority 1 and an age strictly greater than `T` hours. `obtenerRamaArchivable()` selects the best eligible subtree by size, then depth, then root ID. `archivarRama()` removes its events from both trees, appends them to history, and updates archive metrics.

`recuperarArbol()` asks the AVL to rebuild/recover, verifies its structure and balance, and restores the previous state if validation fails.

## Undo

Before supported mutations, `_guardar_estado()` pushes a deep copy of the mutable scenario state, including both trees, zones, stations, history, deleted IDs, parameters, clock, metrics, and report queue. `deshacer()` restores the most recent snapshot and returns `False` when there is no saved state.

## JSON loading and saved versions

`Persistencia` provides three scenario-input paths:

- `cargarInserciones(...)` validates an `inserciones` document and builds a balanced AVL and an unbalanced BST by inserting the listed events.
- `cargarTopologia(...)` validates a `topologia` document, including node references, connectivity, global key ordering, heights, and balance factors. `Escenario` rejects an unbalanced topology outside stress mode.
- `cargarEscenario(...)` restores a full `escenario` snapshot containing configuration, AVL/BST topology, zones, stations, archived/deleted events, queued reports, and metrics.

`guardarEscenario()` returns the full serializable scenario dictionary. `guardarVersion(escenario, nombre)` writes it under `data/versiones/` as JSON and adds a numeric suffix if the requested name already exists. `listarVersiones()` returns saved names, and `cargarVersion(nombre)` reads a saved JSON document; the returned data can then be passed to the scenario loader. The current Versions GUI screen lists JSON files but does not expose save/load actions.

The application starts by loading `data/estado_inicial.json`. Sample insertion and topology inputs are stored under `data/`.
