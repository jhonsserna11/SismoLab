# Domain Model

The domain layer models seismic events and the geographic and observational data used to assess them. The principal rules live in `src/domain/Evento.py`; scenario-level operations are coordinated by `Escenario`.

## `Evento`

File: `src/domain/Evento.py`

An event stores an ID, magnitude, depth, epicenter coordinates, UTC timestamp, revision number, associated station IDs, and review state. New events start with state `Pendiente`.

### Validation

- The ID must be an integer from 1 through 999999.
- Magnitude must be between -2.0 and 10.0; depth between 0.0 and 700.0.
- Both coordinates must be between 0.0 and 1000.0.
- Magnitude, depth, and coordinates are normalized to one decimal place.
- The revision must be a positive integer.
- Stations must be supplied as a list of non-empty strings. `Escenario` additionally verifies that referenced station IDs are registered.
- The timestamp must be a `datetime` in UTC with zero microseconds.

Invalid constructor data raises `ValueError` (or `TypeError` for an invalid decimal representation).

### Priority

`calcularPrioridad(poblada)` returns:

```python
if self.magnitud >= 6.0 or (self.magnitud >= 4.5 and self.profundidad <= 30.0 and poblada):
    return 3
elif self.magnitud >= 4.5:
    return 2
else:
    return 1
```

Priority 3 is assigned to magnitude 6.0 or greater, or to an event of at least 4.5 magnitude that is no deeper than 30.0 and lies in a populated zone. Other events of at least 4.5 receive priority 2; the rest receive priority 1.

### Candidate association

`esCandidato(eventoB, w, r)` treats the current event as a possible predecessor of `eventoB`. Its magnitude must be strictly greater; `eventoB` must occur after it by more than zero and no more than `w` hours; and the Euclidean distance between the two epicenters must be no greater than `r`.

`marcarRevisado()` changes the review state to `Revisado`.

## `Zona`

File: `src/domain/Zona.py`

A zone describes a rectangular geographic area and whether it is populated. `contiene(x, y)` checks whether a coordinate lies in its bounds, `es_poblada()` returns its populated flag, and `obtener_datos()` provides its serialized fields. `Escenario` uses zones to determine whether an event receives the populated-area priority rule.

## `Estacion`

File: `src/domain/Estacion.py`

An observation station has an ID and a descriptive name. The scenario uses registered station IDs to validate event provenance and incoming reports.

## `Reporte`

File: `src/domain/Reporte.py`

A report carries an event ID, revision, proposed magnitude/depth/coordinates, timestamp, and reporting station. `Escenario.procesarReporte()` decides whether the report confirms current values, corrects an active event, is rejected as invalid or outdated, creates a new event, conflicts with existing data, or reactivates an archived event.

## Entity workflow

1. Register zones and stations in a scenario.
2. Create an event with validated measurements and station references.
3. Calculate its priority and construct its tree key.
4. Process later reports according to revision and event status.
5. Keep archived events in the history rather than the active trees.
