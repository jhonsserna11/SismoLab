# Documentación de SismoLab

Esta documentación describe qué hace cada parte del proyecto, para qué sirve y cómo funciona internamente la lógica principal.

## 1. Visión general

SismoLab es un sistema para gestionar y analizar eventos sísmicos en un escenario geográfico. El núcleo del problema no es solo guardar datos, sino decidir:

- qué eventos tienen mayor prioridad,
- cuál es la relación entre un sismo y otros que ocurrieron cerca de él,
- qué eventos deben ser revisados, corregidos o archivados,
- cómo se comporta la estructura del árbol bajo distintos volúmenes de información.

La solución combina tres capas bien diferenciadas:

- capa de dominio: entidades del problema real,
- capa de estructuras: árboles y nodos que administran los eventos,
- capa de lógica: validaciones, consultas, reportes y análisis de desempeño.

## 2. Estructura del repositorio

- `src/domain/`: modelos del dominio (`Evento`, `Zona`, `Estacion`, `Reporte`).
- `src/structures/`: estructuras que guardan eventos en memoria (`Nodo`, `Key`, `AVL`, `BST`).
- `src/logic/`: orquestación del sistema (`Escenario`, `Persistencia`).
- `src/main.py`: entrada principal del programa.
- `tests/`: pruebas de funcionamiento y validación.
- `docs/`: documentación técnica del proyecto.

## 3. Qué resuelve cada capa

### 3.1 Capa de dominio

Define la entidad del negocio. En este proyecto, la entidad principal es `Evento`, que valida los datos del sismo y decide su prioridad. Tambien existen `Zona`, `Estacion` y `Reporte`, que aportan contexto geográfico, estaciones de observación y actualizaciones del sistema.

### 3.2 Capa de estructuras

Se encarga de almacenar eventos de forma ordenada, rápida y balanceada. El `AVL` es la estructura principal porque equilibran los niveles para evitar árboles muy desbalanceados. El `BST` se usa como comparación y validación adicional.

### 3.3 Capa de lógica

`Escenario` es el coordinador del sistema. Aquí se crean eventos, se procesan reportes, se validan asociaciones, se consultan, se archivan y se calculan indicadores de rendimiento.

## 4. Reglas clave del sistema

- cada Evento tiene una clave ordenada por prioridad, magnitud e id,
- la prioridad no depende solo de la magnitud, sino también de la profundidad y si el epicentro cae en una zona poblada,
- el AVL es la estructura principal para consultas y mantenimiento balanceado,
- el BST sirve como referencia para comparar el comportamiento frente a una estrategia no balanceada,
- los reportes pueden actualizar, confirmar, rechazar o reactivar eventos,
- cada operación relevante registra métricas para evaluar el costo de ejecución.

## 5. Cómo se leen estas páginas

Se recomienda seguir este orden:

1. [arquitectura.md](arquitectura.md): visión general del sistema.
2. [dominio.md](dominio.md): entidades y reglas del problema.
3. [estructuras.md](estructuras.md): modelos de almacenamiento.
4. [logica.md](logica.md): flujo operativo y lógica del negocio.
5. [pruebas.md](pruebas.md): validación del sistema.

## 6. Objetivo práctico

La documentación tiene como fin explicar no sólo qué existe, sino también por qué se diseñó así. El sistema está construido para que cada evento pueda ser consultado, validado y comparado bajo reglas reales de riesgo sísmico, y además para permitir medir el costo de cada operación sobre los árboles.
