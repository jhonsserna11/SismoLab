# SismoLab Documentation

This documentation describes the project architecture, seismic-event rules, tree implementations, scenario workflows, desktop interface, persistence formats, and tests.

## Project overview

SismoLab manages seismic events in a simulated geographic area. It validates incoming data, assigns event priorities, finds possible associations, processes corrections, archives eligible events, and exposes structural and query metrics. Active events are indexed in an AVL tree; a parallel BST provides a comparison structure.

## Repository layout

- `src/domain/`: `Evento`, `Zona`, `Estacion`, and `Reporte` domain models.
- `src/structures/`: `Key`, `Nodo`, `Avl`, and `Bst` implementations.
- `src/logic/`: the `Escenario` coordinator and `Persistencia` JSON operations.
- `src/gui/`: Tkinter screens, including the event summary, seismic map, audit, history, and version list.
- `data/`: initial state, sample insertion/topology files, and saved JSON versions.
- `tests/`: tests for domain rules, data structures, persistence, scenario behavior, undo, stress mode, and metrics.

## Documentation pages

1. [Architecture](arquitectura.md): layers, data flow, and component responsibilities.
2. [Domain model](dominio.md): entities, validation, priorities, and event association rules.
3. [Data structures](estructuras.md): composite keys, AVL balancing, and BST comparison.
4. [Scenario logic and persistence](logica.md): event workflows, reports, history, undo, JSON loads, and saved versions.
5. [Desktop interface](interfaz.md): navigation and the responsibilities and limits of each screen.
6. [Performance queries](consultas_desempeno.md): query behavior, counters, and complexity.
7. [Tests](pruebas.md): test coverage and commands.

## Key system rules

- The tree key is `(priority, magnitude, event_id)`.
- Priority depends on magnitude, depth, and whether the epicenter lies in a populated zone.
- Active events are kept in both the AVL and BST; the AVL is the operational tree.
- Reports may confirm or correct an event, be rejected, conflict with current data, or reactivate an archived event.
- Archived and deleted events are tracked separately from active tree entries.
- JSON scenario loading validates structure and event data before restoring the state.
