# Project Tests

The test suite covers domain validation, tree behavior, scenario workflows, persistence, undo, stress mode, and query/structure metrics.

## Test groups

- `test_Avl.py`, `test_Bst.py`, and `test_key.py`: tree operations, ordering, balance, rotations, and key behavior.
- `test_Evento.py`, `test_Zonas.py`, and `test_reportes.py`: domain rules and report/zone behavior.
- `test_persistencia.py` and `test_preparar_estado_inicial.py`: JSON loading and initial-state preparation.
- `tests/tests_Escenario/`: scenario behavior, file loading, undo, stress-mode behavior, and metrics.

## Covered behavior

Functional checks exercise event creation, duplicate IDs, priority calculation, report processing, event association, archival/reactivation, and active/history synchronization. Structural checks validate tree ordering, AVL heights and balance, BST behavior under ordered insertions, and AVL/BST synchronization. Persistence checks include insertion and topology inputs, malformed or duplicate data, state restoration, and undo after loading. Metric tests check query outputs, visit counts, rotation counters, and insertion-order comparisons.

## Run the tests

From the repository root:

```powershell
python -m pytest
```

To run one test module, pass its path, for example:

```powershell
python -m pytest tests/test_Avl.py
```

Some test modules also contain direct invocation code, so running a module directly may execute checks during import. Pytest is the recommended suite runner.
