# Desktop Interface

The Tkinter interface is assembled by `src/main.py`. It loads the initial scenario, creates the screens, and routes navigation actions to the shared `Escenario` instance. Screens are presentation layers; the scenario and persistence modules own business rules and data operations.

## Shared controls

The window includes a left navigation menu, a status bar, the current scenario parameters, a stress-mode toggle, a UTC simulation clock, and a control to advance that clock. The `Deshacer` action restores the last scenario snapshot when one is available.

## Screens

- `resumen.py`: displays active and archived totals, AVL height, leaf count, pending and costly-event totals, and embeds the seismic map.
- `mapa.py`: `MapaSismologico` draws the scenario coordinate bounds and registered zone rectangles with their names. It currently does not plot event epicenters.
- `eventos.py`: event operations and event details/corrections.
- `reportes.py`: report-related workflows.
- `estaciones.py`: station records.
- `zonas.py`: geographic zone records.
- `historico.py`: read-only display of archived events.
- `arboles.py`: tree structure views.
- `metricas.py`: scenario and tree indicators.
- `auditoria.py`: AVL node count, height, stress-mode state, and a text listing of node keys and balance factors.
- `configuracion.py`: read-only display of `W`, `R`, `L`, `T`, and the current operating mode.
- `versiones.py`: lists JSON filenames found in `data/versiones/`; it does not currently save or restore a version from the screen.

## Launch

From the repository root, run:

```powershell
python -m src.main
```

The initial scenario is loaded from `data/estado_inicial.json` before the Tkinter window opens.
