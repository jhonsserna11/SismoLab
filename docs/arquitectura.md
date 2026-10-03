# Arquitectura del proyecto

## 1. Objetivo general

SismoLab modela un escenario de eventos sísmicos donde cada sismo puede ser validado, priorizado, relacionado con otros eventos y corregido mediante reportes. La arquitectura no es una aplicación web ni una base de datos; es un sistema de lógica en memoria que usa árboles para ordenar y buscar la información.

La parte más importante es que el proyecto mezcla dos ideas:

- un árbol equilibrado (`AVL`) para operar con eficiencia y control,
- un árbol de comparación (`BST`) para estudiar diferencias de comportamiento y detectar inconsistencias.

## 2. Capas del sistema

### 2.1 Capa de dominio

Esta capa representa la realidad del problema. Aquí van las clases que describen entidades y validaciones del dominio:

- `Evento`: representa un sismo con magnitud, profundidad, coordenadas y estado.
- `Zona`: representa una región geográfica con límites y marca si es poblada.
- `Estacion`: identifica una estación que reporta o observa el fenómeno.
- `Reporte`: encapsula la información de actualización enviada por una estación.

Estas clases validan tipos, rangos y formatos de entrada antes de aceptar un dato. Por ejemplo, `Evento` rechaza fechas sin UTC o magnitudes fuera del rango permitido. Esa validación evita que el resto del sistema trabaje con información inconsistente.

### 2.2 Capa de estructuras

Aquí se guarda la información de forma ordenada. Las clases principales son:

- `Key`: define la clave de comparación del árbol.
- `Nodo`: guarda el dato del evento y sus punteros a hijos.
- `Avl`: estructura principal que mantiene el árbol equilibrado.
- `Bst`: estructura secundaria para comparar las decisiones del AVL en escenarios de prueba.

La clave ordena los eventos por:

1. prioridad,
2. magnitud,
3. id del evento.

Es decir, la estructura no ordena solo por un campo; usa una clave compuesta para jerarquizar distintos criterios de relevancia.

### 2.3 Capa de lógica

La lógica del negocio se concentra en `Escenario`, que coordina todas las operaciones del sistema. Su trabajo es:

- crear eventos con validaciones,
- insertar o actualizar elementos en el AVL y BST,
- analizar candidatos asociados entre eventos,
- procesar reportes de corrección,
- mantener históricos y eliminados,
- devolver consultas y métricas para análisis de desempeño.

## 3. Flujo principal del sistema

El flujo típico es el siguiente:

1. se define una zona y una estación,
2. se crea un evento con validación de rango y unicidad,
3. se calcula su prioridad según magnitud, profundidad y zona poblada,
4. el evento se inserta en el AVL y en el BST,
5. el sistema recibe reportes y decide si actualiza, confirma, rechaza o reacciona,
6. se ejecutan consultas para extraer pendientes, costosos, candidatos o métricas,
7. se documentan indicadores como altura, hojas, rotaciones y nodos examinados.

## 4. Relación entre componentes

```text
Usuario / pruebas
      |
      v
Escenario
  |-- AVL (estructura principal, orden y equilibrio)
  |-- BST (comparación y sincronización)
  |-- Zonas / estaciones / reportes
  |-- histórico de eventos y eliminados
  |-- métricas y consultas
```

## 5. Qué hace que esta arquitectura sea útil

### 5.1 Encapsulamiento

Cada clase tiene una responsabilidad muy definida. Por ejemplo, `Evento` no conoce cómo se inserta en el árbol; eso lo resuelve `Escenario` y `Avl`.

### 5.2 Validación temprana

Antes de aceptar datos, el sistema verifica si son coherentes. De ese modo, se evita que un dato inválido se propague por todo el árbol.

### 5.3 Sincronización

El AVL y el BST se mantienen en paralelo para que el sistema pueda comparar estructuras y detectar desalineaciones.

### 5.4 Análisis de desempeño

El proyecto no solo entrega resultados, sino que mide cómo se obtienen. Esto es útil para entender la complejidad de cada consulta y la tasa de rotaciones o nodos revisados.

## 6. Consideraciones de diseño

La arquitectura prioriza claridad sobre optimización extrema. El sistema es ideal para estudiar estructura de datos y lógica de negocio porque expone las decisiones en cada capa. Esto facilita el análisis de rendimiento, la depuración y la extensión funcional.
