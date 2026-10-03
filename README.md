# SismoLab

SismoLab es un proyecto de análisis y gestión de eventos sísmicos basado en árboles AVL y BST. El sistema permite crear eventos, procesar reportes, consultar asociaciones y comparar el rendimiento estructural de distintas operaciones.

## Índice de documentación

- [Documentación general](docs/README.md)
- [Arquitectura del proyecto](docs/arquitectura.md)
- [Dominio del problema](docs/dominio.md)
- [Estructuras de datos](docs/estructuras.md)
- [Lógica del escenario](docs/logica.md)
- [Pruebas](docs/pruebas.md)

## Componentes principales

- `src/domain/`: entidades del dominio.
- `src/structures/`: AVL, BST y nodos.
- `src/logic/`: lógica del escenario y consultas.
- `tests/`: suite de validación.
- `docs/`: documentación técnica del proyecto.

## Objetivo del proyecto

El sistema está diseñado para:

- mantener activos los eventos más relevantes,
- validar reportes y actualizaciones,
- analizar relaciones entre eventos,
- medir rendimiento y complejidad de las estructuras,
- comparar AVL y BST bajo distintas inserciones.

## Recomendación de lectura

Para entender el proyecto de forma ordenada, empieza por [docs/README.md](docs/README.md) y luego revisa cada módulo por capas.