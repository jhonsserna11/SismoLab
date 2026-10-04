# Project Architecture

## Purpose

SismoLab models a geographic scenario containing seismic events. It is an in-memory Python application with a Tkinter desktop interface and JSON-based scenario persistence, not a web application or database-backed service.

The project combines an AVL tree for balanced active-event operations with an unbalanced BST that supports structural comparison and consistency checks.

## Layers

### Domain

`src/domain/` contains the entities and their input rules:

- `Evento`: seismic-event data, priority calculation, candidate checks, and review state.
- `Zona`: rectangular geographic bounds and a populated flag.
- `Estacion`: station identity and name.
- `Reporte`: a station-submitted event revision.

### Data structures

`src/structures/` contains the composite `Key`, tree `Nodo`, the self-balancing `Avl`, and the comparison `Bst`. Both trees use the same ordering: priority, magnitude, then event ID.

### Application logic

`src/logic/Escenario.py` coordinates domain objects and trees. It creates and corrects events, processes reports, performs queries, maintains active/archive/deleted collections, and exposes metrics and undo. `src/logic/Persistencia.py` serializes and validates scenario JSON, insertion inputs, topologies, and saved versions.

### Desktop interface

`src/main.py` creates the Tkinter application, loads `data/estado_inicial.json`, and wires screens to the scenario. Screen responsibilities are described in the [interface guide](interfaz.md). The summary screen embeds the map renderer from `src/gui/mapa.py`.

## Typical data flow

1. `main.py` loads the initial JSON and constructs an `Escenario`.
2. The user works through Tkinter screens, or tests call scenario methods directly.
3. `Escenario` validates operations and updates the AVL and BST where appropriate.
4. Domain objects apply event rules; `Persistencia` handles JSON serialization and validation.
5. Screens render scenario data and structural indicators.

## State ownership

The scenario owns the AVL and BST, zones, stations, archived events, deleted IDs, report queue, simulation clock, parameters `W`, `R`, `L`, and `T`, cumulative metrics, and the undo stack. Active events are stored in the trees; archived events are stored in `historico`. JSON snapshots include the scenario state and tree topology.

## Design considerations

- Domain validation prevents malformed event values from entering the trees.
- The composite key makes tree ordering deterministic across equal priorities and magnitudes.
- AVL/BST comparison illustrates the effect of insertion order on an unbalanced search tree.
- Structural and query counters expose algorithm behavior independently of wall-clock timing.
- JSON loading verifies consistency rather than trusting stored keys, links, heights, and factors.
