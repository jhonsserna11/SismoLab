# SismoLab

SismoLab is a Python application for managing and analyzing seismic events. It combines a Tkinter desktop interface, an in-memory AVL tree for active events, a BST for comparison, and JSON persistence for scenario data.

## Documentation

- [Documentation index](docs/README.md)
- [Architecture](docs/arquitectura.md)
- [Domain model](docs/dominio.md)
- [Data structures](docs/estructuras.md)
- [Scenario logic and persistence](docs/logica.md)
- [Desktop interface](docs/interfaz.md)
- [Performance queries](docs/consultas_desempeno.md)
- [Tests](docs/pruebas.md)

## Main components

- `src/domain/`: seismic-event, zone, station, and report models.
- `src/structures/`: AVL/BST implementations, keys, and tree nodes.
- `src/logic/`: scenario orchestration and JSON persistence.
- `src/gui/`: Tkinter screens for the operational workflows and metrics.
- `data/`: initial scenario, sample inputs, and saved versions.
- `tests/`: functional, structural, persistence, and performance-related checks.

## Run

Start the desktop application from the repository root:

```powershell
python -m src.main
```

Run the test suite with:

```powershell
python -m pytest
```

The application loads its initial scenario from `data/estado_inicial.json`.
